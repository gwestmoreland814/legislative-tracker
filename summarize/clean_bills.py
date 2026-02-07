"""
Bill Cleaning, Normalization, and Topic Classification Module

Reads raw congressional bill data from data/raw_bills.json,
normalizes fields, assigns a policy topic, and saves clean output.

Phase: 3.3 — Topic Classification
"""

import json
import os
from datetime import datetime


RAW_DATA_PATH = "data/raw_bills.json"
CLEAN_DATA_PATH = "data/clean_bills.json"


TOPIC_KEYWORDS = {
    "Education": ["education", "school", "student", "college", "university"],
    "Healthcare": ["health", "medical", "medicare", "medicaid"],
    "Economy": ["tax", "budget", "economic", "trade", "tariff"],
    "Defense": ["defense", "military", "armed forces", "veteran"],
    "Judiciary": ["court", "judge", "judicial", "law"],
    "Energy": ["energy", "oil", "gas", "electric", "climate"],
    "Foreign Policy": ["foreign", "international", "treaty", "alliance"],
}


def load_raw_data():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"{RAW_DATA_PATH} not found")

    with open(RAW_DATA_PATH, "r") as f:
        return json.load(f)


def classify_topic(title):
    if not title:
        return "Other"

    title_lower = title.lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return topic

    return "Other"


def normalize_bill(bill):
    title = bill.get("title")

    return {
        "bill_number": bill.get("number"),
        "title": title,
        "introduced_date": bill.get("introducedDate"),
        "congress": bill.get("congress"),
        "bill_type": bill.get("type"),
        "origin_chamber": bill.get("originChamber"),
        "topic": classify_topic(title),
        "last_updated": bill.get("updateDate"),
    }


def clean_bills(raw_data):
    bills = raw_data.get("data", {}).get("bills", [])
    cleaned = []

    for bill in bills:
        cleaned.append(normalize_bill(bill))

    return cleaned


def save_clean_data(cleaned_bills):
    payload = {
        "cleaned_at": datetime.utcnow().isoformat(),
        "count": len(cleaned_bills),
        "bills": cleaned_bills,
    }

    with open(CLEAN_DATA_PATH, "w") as f:
        json.dump(payload, f, indent=2)


def main():
    print("Loading raw bill data...")
    raw_data = load_raw_data()

    print("Cleaning and classifying bills...")
    cleaned_bills = clean_bills(raw_data)

    save_clean_data(cleaned_bills)

    print(f"Saved {len(cleaned_bills)} classified bills to {CLEAN_DATA_PATH}")


if __name__ == "__main__":
    main()