#!/usr/bin/python3
"""Query Reddit API and print top 10 hot post titles for a subreddit."""
import requests


USER_AGENT = {"User-Agent": "alu-scripting-reddit-api/1.0"}


def top_ten(subreddit):
    """Print the first 10 hot post titles for `subreddit`, or None if invalid."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": 10}

    try:
        response = requests.get(
            url,
            headers=USER_AGENT,
            params=params,
            allow_redirects=False,
            timeout=10,
        )
        if response.status_code != 200:
            print("None")
            return

        posts = response.json().get("data", {}).get("children", [])
        for post in posts:
            print(post.get("data", {}).get("title", ""))
    except (requests.RequestException, ValueError):
        print("None")
