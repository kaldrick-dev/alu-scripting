#!/usr/bin/python3
"""Reddit recursive listing module."""
import requests


USER_AGENT = {
    "User-Agent": (
        "python:alu-scripting.api_advanced:1.0 "
        "(by /u/reddit_api_bot)"
    )
}


def recurse(subreddit, hot_list=None, after=None):
    """Return titles of all hot posts, or None for an invalid subreddit."""
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 100}
    if after is not None:
        params["after"] = after

    try:
        response = requests.get(
            url,
            headers=USER_AGENT,
            params=params,
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json().get("data", {})
    posts = data.get("children", [])
    hot_list.extend(
        post.get("data", {}).get("title", "")
        for post in posts
    )

    next_after = data.get("after")
    if next_after is None:
        return hot_list

    return recurse(subreddit, hot_list, next_after)
