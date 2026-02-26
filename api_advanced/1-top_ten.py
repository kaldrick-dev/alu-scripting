#!/usr/bin/python3
"""Prints the title of the first 10 hot posts listed for a given subreddit"""

import requests


def top_ten(subreddit):
    """Print the titles of up to 10 hot posts for a subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "python:top_ten:v1.0 (by /u/reddit_api_script)"}

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"limit": 10},
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException:
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
