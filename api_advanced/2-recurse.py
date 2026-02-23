#!/usr/bin/python3
"""Reddit recursive listing module.

This module exposes `recurse`, which recursively retrieves all hot post
titles from a subreddit using Reddit API pagination.
"""
import requests


USER_AGENT = {"User-Agent": "alu-scripting-reddit-api/1.0"}


def recurse(subreddit, hot_list=None, after=None):
    """Return list of all hot post titles for `subreddit`, or None if invalid."""
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(
            url,
            headers=USER_AGENT,
            params=params,
            allow_redirects=False,
            timeout=10,
        )
        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        posts = data.get("children", [])
        hot_list.extend([post.get("data", {}).get("title", "") for post in posts])

        next_after = data.get("after")
        if next_after is None:
            return hot_list
        return recurse(subreddit, hot_list, next_after)
    except (requests.RequestException, ValueError):
        return None
