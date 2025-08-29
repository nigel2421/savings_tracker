import json
import os

DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "platforms.json")

def save_platforms(platforms):
    """Saves a list of platform objects to a JSON file."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    data_to_save = [p.to_dict() for p in platforms.values()]
    with open(FILE_PATH, 'w') as f:
        json.dump(data_to_save, f, indent=4)
    print("Data saved successfully!")

def load_platforms():
    """Loads platform objects from a JSON file."""
    from models import InvestmentPlatform  # Import here to avoid circular dependency

    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, 'r') as f:
        try:
            data = json.load(f)
            platforms = {item['name']: InvestmentPlatform.from_dict(item) for item in data}
            print("Data loaded successfully!")
            return platforms
        except json.JSONDecodeError:
            return {} # Return empty dict if file is empty or corrupted