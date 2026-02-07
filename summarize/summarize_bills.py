"""
Plain-English Bill Summarization Module

Reads cleaned and classified bills from data/clean_bills.json
and generates neutral, plain-English summaries suitable for
public consumption and social posting.

Phase: 4 — Plain-English Summarization
"""

import json
import os
from datetime import datetime


CLEAN_DATA_PATH = "data/clean_bills.json"
SUMMARY_DATA_PATH = "data/summaries.json"


def load_clean_data():
    if not os.path.exists(CLEAN_DATA_PATH):
        raise FileNotFoundError(f"{CLEAN_DATA_PATH} not found")

    with open(CLEAN_DATA_PATH, "r") as f:
        return json.load(f)


def summarize_bill(bill):
    """
    Generate a plain-English summary for a single bill.
    """
    bill_number = bill.get("bill_number", "This bill")
    title = bill.get("title", "").strip()
    topic = bill.get("topic", "policy")
    introduced = bill.get("introduced_date", "an unknown date")

    summary_lines = []

    summary_lines.append(
        f"{bill_number} is a {topic.lower()} bill introduced on {introduced}."
    )

    if title:
        summary_lines.append(
            f"It focuses on the following issue: {title}"
        )

    summary_lines.append(
        "The bill has been introduced and is awaiting further legislative action."
    )

    return " ".join(summary_lines)


def generate_summaries(clean_data):
    bills = clean_data.get("bills", [])
    summaries = []

    for bill in bills:
        summaries.append({
            "bill_number": bill.get("bill_number"),
            "topic": bill.get("topic"),
            "summary": summarize_bill(bill)
        })

    return summaries


def save_summaries(summaries):
    payload = {
        "generated_at": datetime.utcnow().isoformat(),
        "count": len(summaries),
        "summaries": summaries
    }

    with open(SUMMARY_DATA_PATH, "w") as f:
        json.dump(payload, f, indent=2)


def main():
    print("Loading cleaned bill data...")
    clean_data = load_clean_data()

    print("Generating plain-English summaries...")
    summaries = generate_summaries(clean_data)

    save_summaries(summaries)

    print(f"Saved {len(summaries)} summaries to {SUMMARY_DATA_PATH}\n")

    for item in summaries:
        print(f"{item['bill_number']}:")
        print(item["summary"])
        print("-" * 60)


if __name__ == "__main__":
    main()