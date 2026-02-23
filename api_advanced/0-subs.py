#!/usr/bin/python3
"""
0-main
"""
import requests


USER_AGENT = {"User-Agent": "alu-scripting-reddit-api/1.0"}


def number_of_subscribers(subreddit):
    """Return total subscribers for `subreddit`, or 0 if invalid."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    try:
        response = requests.get(
            url,
            headers=USER_AGENT,
            allow_redirects=False,
            timeout=10,
        )
        if response.status_code != 200:
            return 0
        return response.json().get("data", {}).get("subscribers", 0)
    except (requests.RequestException, ValueError):
        return 0
