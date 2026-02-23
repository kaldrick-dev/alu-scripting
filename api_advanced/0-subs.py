#!/usr/bin/python3
"""Reddit subscriber module."""
import requests


USER_AGENT = {
    "User-Agent": (
        "python:alu-scripting.api_advanced:1.0 "
        "(by /u/reddit_api_bot)"
    )
}


def number_of_subscribers(subreddit):
    """Return subscriber count for a subreddit, or 0 if invalid."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    try:
        response = requests.get(
            url,
            headers=USER_AGENT,
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException:
        return 0

    if response.status_code != 200:
        return 0

    return response.json().get("data", {}).get("subscribers", 0)
