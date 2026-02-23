#!/usr/bin/python3
"""Reddit hot posts module."""
import requests


USER_AGENT = {
    "User-Agent": (
        "python:alu-scripting.api_advanced:1.0 "
        "(by /u/reddit_api_bot)"
    )
}


def top_ten(subreddit):
    """Print the first 10 hot post titles or None if invalid."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 10}

    try:
        response = requests.get(
            url,
            headers=USER_AGENT,
            params=params,
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException:
        print(None)
        return

    if response.status_code != 200:
        print(None)
        return

    posts = response.json().get("data", {}).get("children", [])
    for post in posts:
        title = post.get("data", {}).get("title")
        if title:
            print(title)
