"""
X Post Formatting Module

Reads plain-English bill summaries from data/summaries.json
and formats them into concise, readable posts suitable for X.

Phase: 5 — X Formatting (No Posting Yet)
"""

import json
import os
from datetime import datetime


SUMMARY_DATA_PATH = "data/summaries.json"
X_POSTS_PATH = "data/x_posts.json"

MAX_LENGTH = 260  # Leave buffer for safety


def load_summaries():
    if not os.path.exists(SUMMARY_DATA_PATH):
        raise FileNotFoundError(f"{SUMMARY_DATA_PATH} not found")

    with open(SUMMARY_DATA_PATH, "r") as f:
        return json.load(f)


def truncate(text, max_length):
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + "..."


def format_post(summary_item):
    bill_number = summary_item.get("bill_number", "This bill")
    topic = summary_item.get("topic", "Policy")
    summary = summary_item.get("summary", "")

    post = (
        f"{bill_number} | {topic}\n\n"
        f"{summary}"
    )

    return truncate(post, MAX_LENGTH)


def generate_posts(summary_data):
    summaries = summary_data.get("summaries", [])
    posts = []

    for item in summaries:
        posts.append({
            "bill_number": item.get("bill_number"),
            "topic": item.get("topic"),
            "post": format_post(item)
        })

    return posts


def save_posts(posts):
    payload = {
        "generated_at": datetime.utcnow().isoformat(),
        "count": len(posts),
        "posts": posts
    }

    with open(X_POSTS_PATH, "w") as f:
        json.dump(payload, f, indent=2)


def main():
    print("Loading summaries...")
    summary_data = load_summaries()

    print("Formatting posts for X...")
    posts = generate_posts(summary_data)

    save_posts(posts)

    print(f"Saved {len(posts)} X-ready posts to {X_POSTS_PATH}\n")

    for p in posts:
        print(p["post"])
        print("-" * 60)


if __name__ == "__main__":
    main()