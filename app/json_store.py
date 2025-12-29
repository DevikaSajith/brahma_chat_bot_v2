import json

def load_events_from_json(filepath: str = "data/events.json"):
    """Load events with error handling"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Handle both dict with 'events' key and direct list
            if isinstance(data, dict):
                events = data.get("events", [])
            elif isinstance(data, list):
                events = data
            else:
                events = []
            print(f"📄 Loaded {len(events)} events from JSON")
            return events
    except FileNotFoundError:
        print(f"⚠️ Events file not found: {filepath}")
        return []
    except Exception as e:
        print(f"❌ Error loading events: {e}")
        return []
