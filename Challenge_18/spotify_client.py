from flask import Flask, request, redirect, session, jsonify, render_template
import requests
import random
import string

# Flask app setup
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key in production

# Spotify API credentials
CLIENT_ID = "your client id"
CLIENT_SECRET = "your client secret"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

# Scopes for accessing user data and playback features
SCOPES = (
    "user-read-private "
    "user-read-email "
    "user-read-playback-state "
    "user-modify-playback-state "  # Required to control playback
    "streaming "
    "playlist-read-private "
    "playlist-read-collaborative"
)

# Helper function to generate a random state for OAuth
def generate_state(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/")
def login():
    """
    Redirects the user to Spotify's login page for authentication.
    """
    state = generate_state()
    session["oauth_state"] = state  # Store state for validation
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={REDIRECT_URI}&state={state}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """
    Handles the redirection after Spotify login and exchanges code for access tokens.
    """
    code = request.args.get("code")
    state = request.args.get("state")

    if state != session.get("oauth_state"):
        return "State mismatch. Authentication failed.", 400

    # Exchange authorization code for access token
    auth_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=auth_data)
    if response.status_code != 200:
        return f"Failed to get access token: {response.content}", 400

    tokens = response.json()
    session["access_token"] = tokens["access_token"]
    session["refresh_token"] = tokens["refresh_token"]

    return redirect("/playlists")
@app.route("/playlists")
def playlists():
    """
    Fetches and displays the user's playlists with options to select one for playback.
    """
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.get(f"{SPOTIFY_API_URL}/me/playlists", headers=headers)
    if response.status_code != 200:
        return f"Failed to fetch playlists: {response.content}", 400

    playlists = response.json()
    return render_template("playlists.html", playlists=playlists["items"])


@app.route("/start_playlist", methods=["POST"])
def start_playlist():
    """
    Starts playback of the selected playlist on the active device.
    """
    playlist_uri = request.form.get("playlist_uri")
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    data = {"context_uri": playlist_uri}

    response = requests.put(f"{SPOTIFY_API_URL}/me/player/play", headers=headers, json=data)
    if response.status_code != 204:
        return f"Failed to start playlist: {response.content}", 400

    return redirect("/playback")

@app.route("/playback")
def playback():
    """
    Displays the playback interface, showing the currently playing track and playback controls.
    """
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.get(f"{SPOTIFY_API_URL}/me/player", headers=headers)

    if response.status_code == 204 or response.status_code == 404:
        # No active playback or device
        playback_info = None
    elif response.status_code != 200:
        return f"Failed to fetch playback state: {response.content}", 400
    else:
        playback_info = response.json()

    return render_template("playback.html", playback=playback_info)


@app.route("/play", methods=["POST"])
def play():
    """
    Resumes playback on the current device.
    """
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.put(f"{SPOTIFY_API_URL}/me/player/play", headers=headers)

    if response.status_code != 204:
        return f"Failed to resume playback: {response.content}", 400

    return jsonify({"message": "Playback resumed"}), 200

@app.route("/pause", methods=["POST"])
def pause():
    """
    Pauses playback on the current device.
    """
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.put(f"{SPOTIFY_API_URL}/me/player/pause", headers=headers)

    if response.status_code != 204:
        return f"Failed to pause playback: {response.content}", 400

    return jsonify({"message": "Playback paused"}), 200

if __name__ == "__main__":
    app.run(debug=True)
