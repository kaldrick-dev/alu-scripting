#!/usr/bin/python3
"""Prints the title of the first 10 hot posts listed for a given subreddit"""

import requests


def top_ten(subreddit):
    """Main function"""
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "python:top_ten:v1.0 (by /u/reddit_api_script)"}

    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        print(None)
        return

    hot_posts = response.json().get("data", {}).get("children", [])
    for post in hot_posts:
        print(post.get("data", {}).get("title"))
