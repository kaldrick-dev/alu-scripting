#!/usr/bin/python3
"""Reddit recursive keyword counting module."""
from collections import Counter
import re

import requests


USER_AGENT = {
    "User-Agent": (
        "python:alu-scripting.api_advanced:1.0 "
        "(by /u/reddit_api_bot)"
    )
}
WORD_RE = re.compile(r"[A-Za-z0-9]+")


def _fetch_titles(subreddit, titles=None, after=None):
    """Recursively fetch all hot post titles for a subreddit."""
    if titles is None:
        titles = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 100}
    if after is not None:
        params["after"] = after

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
    titles.extend(post.get("data", {}).get("title", "") for post in posts)

    next_after = data.get("after")
    if next_after is None:
        return titles

    return _fetch_titles(subreddit, titles, next_after)


def _count_words_in_titles(titles, counts, multipliers, idx=0):
    """Recursively count matching keywords across all titles."""
    if idx >= len(titles):
        return

    words = WORD_RE.findall(titles[idx].lower())
    for word in words:
        if word in counts:
            counts[word] += multipliers[word]

    _count_words_in_titles(titles, counts, multipliers, idx + 1)


def count_words(subreddit, word_list):
    """Print sorted keyword counts for hot posts in a subreddit."""
    if not word_list:
        return

    lowered = [word.lower() for word in word_list]
    multipliers = Counter(lowered)
    counts = {word: 0 for word in multipliers}

    try:
        titles = _fetch_titles(subreddit)
    except requests.RequestException:
        return

    if titles is None:
        return

    _count_words_in_titles(titles, counts, multipliers)

    sorted_counts = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0]),
    )
    for word, count in sorted_counts:
        if count > 0:
            print("{}: {}".format(word, count))
