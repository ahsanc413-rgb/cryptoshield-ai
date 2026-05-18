from fastapi import FastAPI
from bson import json_util
import json

from backend.database.mongo_client import (
    trades_collection,
    alerts_collection
)

app = FastAPI(
    title="CryptoShield AI API"
)

# ======================================================
# HOME
# ======================================================

@app.get("/")
def home():

    return {
        "message": "CryptoShield API Running"
    }

# ======================================================
# TRADES
# ======================================================

@app.get("/api/trades")
def get_trades():

    trades = list(
        trades_collection.find().limit(100)
    )

    return json.loads(
        json_util.dumps(trades)
    )

# ======================================================
# ALERTS
# ======================================================

@app.get("/api/alerts")
def get_alerts():

    alerts = list(
        alerts_collection.find().limit(100)
    )

    return json.loads(
        json_util.dumps(alerts)
    )

# ======================================================
# METRICS
# ======================================================

@app.get("/api/metrics")
def get_metrics():

    return {

        "total_trades":
        trades_collection.count_documents({}),

        "total_alerts":
        alerts_collection.count_documents({})
    }