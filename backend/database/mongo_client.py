from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI
)

db = client["cryptoshield_ai"]

users_collection = db["users"]

trades_collection = db["live_trades"]

alerts_collection = db["risk_alerts"]

print("✅ MongoDB Connected")