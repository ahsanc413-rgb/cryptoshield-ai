from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.mongo_client import (
    trades_collection,
    alerts_collection
)

# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="CryptoShield AI API"
)

# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =========================
# HOME ROUTE
# =========================

@app.get("/")

def home():

    return {

        "message":
            "CryptoShield AI API Running"
    }

# =========================
# GET TRADES
# =========================

@app.get("/api/trades")

def get_trades():

    trades = list(

        trades_collection.find(
            {},
            {"_id": 0}
        )

        .sort(
            "trade_time",
            -1
        )

        .limit(100)
    )

    return trades

# =========================
# GET ALERTS
# =========================

@app.get("/api/alerts")

def get_alerts():

    alerts = list(

        alerts_collection.find(
            {},
            {"_id": 0}
        )

        .sort(
            "timestamp",
            -1
        )

        .limit(100)
    )

    return alerts

# =========================
# GET METRICS
# =========================

@app.get("/api/metrics")

def get_metrics():

    total_trades = (
        trades_collection.count_documents({})
    )

    total_alerts = (
        alerts_collection.count_documents({})
    )

    pipeline = [

        {
            "$group": {

                "_id": "$symbol",

                "count": {
                    "$sum": 1
                }
            }
        },

        {
            "$sort": {
                "count": -1
            }
        },

        {
            "$limit": 1
        }
    ]

    most_active = list(

        trades_collection.aggregate(
            pipeline
        )
    )

    if most_active:

        asset = most_active[0]["_id"]

    else:

        asset = "N/A"

    return {

        "total_trades":
            total_trades,

        "total_alerts":
            total_alerts,

        "most_active_asset":
            asset
    }