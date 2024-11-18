import discord
from discord.ext import commands
import requests
import random  
import json
from bs4 import BeautifulSoup
TOKEN = 'token here'
# Intents setup
intents = discord.Intents.default()
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Load challenges from JSON file
def load_challenges():
    try:
        with open("challenges.json", "r") as file:
            data = json.load(file)
            return data.get("challenges", [])
    except FileNotFoundError:
        print("challenges.json file not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

# Save challenges to JSON file
def save_challenges(challenges):
    try:
        with open("challenges.json", "w") as file:
            json.dump({"challenges": challenges}, file, indent=4)
    except Exception as e:
        print(f"Error saving challenges: {e}")


challenges = load_challenges()



@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')


@bot.command()
async def list(ctx):
    """
    Lists all available challenges.
    """
    if not challenges:
        await ctx.send("No challenges available.")
        return

    challenge_list = "\n".join(
        [f"{idx + 1}. **{c['name']}** - {c['url']}" for idx, c in enumerate(challenges)]
    )
    await ctx.send(f"Here are the available challenges:\n\n{challenge_list}")

@bot.command()
async def add(ctx, url: str):
    """
    Adds a new challenge if the URL is valid and points to a coding challenge.
    """
    if not url.startswith("https://codingchallenges.fyi/challenges/"):
        await ctx.send("Invalid URL. Please provide a valid challenge URL.")
        return

    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        if response.status_code != 200:
            await ctx.send("Failed to fetch the challenge. The URL might be invalid.")
            return

        # Parse the HTML to extract the title
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "Unknown Challenge"

        # Check if the challenge already exists
        if any(c['url'] == url for c in challenges):
            await ctx.send("This challenge is already in the list.")
            return

        # Add the new challenge
        new_challenge = {"name": title, "url": url}
        challenges.append(new_challenge)
        save_challenges(challenges)

        await ctx.send(f"Challenge added successfully:\n\n**{title}** - {url}")
    except Exception as e:
        print(f"Error adding challenge: {e}")
        await ctx.send("An error occurred while trying to add the challenge.")


@bot.command()
async def quote(ctx):
    """
    Responds with a random quote fetched from the DummyJSON API.
    """
    try:
        response = requests.get("https://dummyjson.com/quotes/random")
        if response.status_code == 200:
            data = response.json()
            quote = data.get("quote", "No quote found.")
            author = data.get("author", "Unknown")
            await ctx.send(f"Here's a random quote:\n\n'{quote}'\n\n— {author}")
        else:
            await ctx.send("Sorry, I couldn't fetch a quote at the moment. Please try again later.")
    except Exception as e:
        print(f"Error fetching quote: {e}")
        await ctx.send("Oops! Something went wrong while fetching the quote.")

@bot.command()
async def challenge(ctx):
    """
    Responds with a random challenge from the JSON file.
    """
    if not challenges:
        await ctx.send("No challenges available at the moment. Please check back later!")
        return
    challenge = random.choice(challenges)
    name = challenge.get("name", "Unknown Challenge")
    url = challenge.get("url", "No URL available")
    await ctx.send(f"Here's a random coding challenge for you:\n\n**{name}**\n{url}")

# Run the bot
bot.run(TOKEN)