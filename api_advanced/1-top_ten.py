#!/usr/bin/python3
"""Prints the title of the first 10 hot posts listed for a given subreddit"""

import requests


def top_ten(subreddit):
    """Print the titles of up to 10 posts for a subreddit."""
    url = "https://www.reddit.com/r/{}.json?limit=10".format(subreddit)
    headers = {"User-Agent": "MyAPI/0.0.1"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
    except Exception:
        print(None)
        return

    if response.status_code != 200:
        print(None)
        return

    try:
        hot_posts = response.json().get("data", {}).get("children", [])
    except ValueError:
        print(None)
        return

    for post in hot_posts:
        print(post.get("data", {}).get("title", ""))
