import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
APPWRITE_PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")

# IMPORTANT: These are IDs, not names
DATABASE_ID = "6948d5240015a19ea05a"
COLLECTION_ID = "events"

OUTPUT_FILE = "data/events.json"

URL = f"{APPWRITE_ENDPOINT}/databases/{DATABASE_ID}/collections/{COLLECTION_ID}/documents"

HEADERS = {
    "X-Appwrite-Project": APPWRITE_PROJECT_ID,
    "X-Appwrite-Key": APPWRITE_API_KEY
}


def sync_events_from_appwrite():
    print("Fetching events from Appwrite (REST API)...")

    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    data = response.json()
    documents = data.get("documents", [])

    events = []

    events = []

    for doc in documents:
        events.append({
            "event_name": doc.get("event_name"),
            "venue": doc.get("venue"),
            "time": doc.get("time"),
            "date": doc.get("date"),
            "details": doc.get("details"),
            "coordinator": doc.get("coordinator"),
            "fest": doc.get("fest"),
            "slots": doc.get("slots"),
            "poster": doc.get("poster"),
            "amount": doc.get("amount"),
            "category": doc.get("category")
        })


    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

    print(f"✅ Synced {len(events)} events into {OUTPUT_FILE}")


if __name__ == "__main__":
    sync_events_from_appwrite()
