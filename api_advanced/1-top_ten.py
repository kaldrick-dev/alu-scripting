#!/usr/bin/python3
"""Reddit hot posts module."""
import requests


USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (compatible; alu-api-advanced/1.0)"
}


def top_ten(subreddit):
    """Print the first 10 hot post titles or None if invalid."""
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    params = {"limit": 10, "raw_json": 1}

    response = requests.get(
        url,
        headers=USER_AGENT,
        params=params,
        allow_redirects=False,
    )

    if response.status_code != 200:
        print(None)
        return

    posts = response.json().get("data", {}).get("children", [])
    for post in posts:
        title = post.get("data", {}).get("title")
        if title:
            print(title)
