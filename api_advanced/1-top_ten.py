#!/usr/bin/python3
"""Prints the titles of the first 10 hot posts listed for a given subreddit."""
import requests


def top_ten(subreddit):
    """Queries Reddit API and prints titles of first 10 hot posts."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "mozilla/5.0"}
    params = {"limit": 10}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
        )
    except Exception:
        return

    if response.status_code != 200:
        print(None)
        return

    data = response.json()
    posts = data.get("data", {}).get("children", [])

    if not posts:
        return

    for post in posts:
        title = post.get("data", {}).get("title")
        if title:
            print(title)