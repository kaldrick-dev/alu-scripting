#!/usr/bin/python3
"""Reddit API module."""

import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "python:api_advanced:v1.0 (by /u/L-nsamba)"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
    except requests.RequestException:
        print(None)
        return

    if response.status_code != 200:
        print(None)
        return

    try:
        posts = response.json().get("data", {}).get("children", [])
    except ValueError:
        print(None)
        return

    for post in posts:
        print(post.get("data", {}).get("title", ""))
