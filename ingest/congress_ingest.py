"""
Congress.gov Ingestion Script

Pulls recent U.S. House bills from Congress.gov using
an official API key stored in a .env file and saves
the raw JSON response to disk.

Phase: 2.3 — Save Raw Data
"""

import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CONGRESS_API_BASE = "https://api.congress.gov/v3"
CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")

if not CONGRESS_API_KEY:
    raise RuntimeError("CONGRESS_API_KEY not found in .env file")


def fetch_recent_house_bills(limit=5):
    """
    Fetch recent House bills from Congress.gov.
    Returns the full JSON response.
    """
    url = f"{CONGRESS_API_BASE}/bill"
    params = {
        "chamber": "house",
        "limit": limit,
        "format": "json",
        "api_key": CONGRESS_API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise RuntimeError(
            f"Congress API request failed "
            f"({response.status_code}): {response.text}"
        )

    return response.json()


def save_raw_data(data):
    """
    Save raw JSON data to data/raw_bills.json
    """
    os.makedirs("data", exist_ok=True)

    payload = {
        "fetched_at": datetime.utcnow().isoformat(),
        "source": "Congress.gov",
        "data": data,
    }

    with open("data/raw_bills.json", "w") as f:
        json.dump(payload, f, indent=2)


def main():
    print("Fetching recent House bills...")
    raw_response = fetch_recent_house_bills(limit=5)

    bills = raw_response.get("bills", [])
    print(f"Retrieved {len(bills)} bills\n")

    save_raw_data(raw_response)
    print("Raw data saved to data/raw_bills.json\n")

    for bill in bills:
        bill_number = bill.get("number", "N/A")
        title = bill.get("title", "No title available")
        introduced = bill.get("introducedDate", "Unknown date")

        print(f"Bill: {bill_number}")
        print(f"Title: {title}")
        print(f"Introduced: {introduced}")
        print("-" * 40)


if __name__ == "__main__":
    main()