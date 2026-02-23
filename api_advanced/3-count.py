#!/usr/bin/python3
"""Recursively count keyword occurrences in subreddit hot post titles."""
import re
import requests
from collections import Counter


USER_AGENT = {"User-Agent": "alu-scripting-reddit-api/1.0"}
WORD_RE = re.compile(r"[A-Za-z0-9]+")


def _fetch_titles(subreddit, titles=None, after=None):
    """Recursively fetch all hot post titles for a subreddit."""
    if titles is None:
        titles = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": 100}
    if after:
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
    children = data.get("children", [])
    titles.extend([child.get("data", {}).get("title", "") for child in children])

    next_after = data.get("after")
    if next_after is None:
        return titles
    return _fetch_titles(subreddit, titles, next_after)


def _count_in_titles(titles, counts, multipliers, idx=0):
    """Recursively count tracked words in each title."""
    if idx >= len(titles):
        return

    words = WORD_RE.findall(titles[idx].lower())
    for word in words:
        if word in counts:
            counts[word] += multipliers[word]

    _count_in_titles(titles, counts, multipliers, idx + 1)


def count_words(subreddit, word_list):
    """Print sorted keyword counts from hot article titles."""
    if not word_list:
        return

    lowered_words = [word.lower() for word in word_list]
    multipliers = Counter(lowered_words)
    counts = {word: 0 for word in multipliers}

    try:
        titles = _fetch_titles(subreddit)
        if titles is None:
            return

        _count_in_titles(titles, counts, multipliers)

        for word, count in sorted(
            counts.items(), key=lambda item: (-item[1], item[0])
        ):
            if count > 0:
                print(f"{word}: {count}")
    except (requests.RequestException, ValueError):
        return
