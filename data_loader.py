"""Loads the courier data from the JSON file."""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "parcels.json"

def load_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def load_parcels():
    return load_data()["parcels"]

def load_capacity():
    return load_data()["vehicle_capacity"]

def load_warehouse():
    return load_data()["warehouse"]

def load_graph():
    return load_data()["graph"]
