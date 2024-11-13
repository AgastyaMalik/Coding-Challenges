import requests

# Step 1: POST request to shorten the URL
post_url = "http://localhost:5000/shorten"
data = {"url": "www.godaddy.com/faq/what-is-my-domain-name"}
post_response = requests.post(post_url, json=data)

# Check if POST request was successful
if post_response.status_code == 201:
    print("POST Response Status Code:", post_response.status_code)
    print("POST Response Text:", post_response.text)

    # Parse JSON to get the short key
    response_json = post_response.json()
    short_key = response_json.get("key")

    # Step 2: GET request to verify redirection works
    get_url = f"http://localhost:5000/{short_key}"
    get_response = requests.get(get_url, allow_redirects=False)

    # Check if the GET request is a redirection (302 status code)
    if get_response.status_code == 302:
        print("GET Response Status Code:", get_response.status_code)
        print("Redirection URL:", get_response.headers['Location'])

        # Step 3: DELETE request to remove the shortened URL
        delete_url = f"http://localhost:5000/{short_key}"
        delete_response = requests.delete(delete_url)
        print("DELETE Response Status Code:", delete_response.status_code)

        # Step 4: Verification GET request to check if deletion was successful
        verify_response = requests.get(get_url, allow_redirects=False)
        print("Verification GET Status Code (after deletion):", verify_response.status_code)
    else:
        print("GET request failed or did not redirect.")
else:
    print("POST request failed.")
