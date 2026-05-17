import os

from dotenv import load_dotenv

from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI"
)

client = MongoClient(
    MONGO_URI
)

db = client["cryptoshield_ai"]

trades_collection = db[
    "live_trades"
]

alerts_collection = db[
    "risk_alerts"
]