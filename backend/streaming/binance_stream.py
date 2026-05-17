import json
import time
from datetime import datetime
from websocket import WebSocketApp

from backend.database.mongo_client import (
    trades_collection,
    alerts_collection
)

from backend.analytics.live_metrics import (
    LiveMetrics
)

from backend.analytics.volatility_tracker import (
    VolatilityTracker
)

from backend.risk_engine.anomaly_detector import (
    AnomalyDetector
)

from backend.risk_engine.risk_scorer import (
    RiskScorer
)

from backend.risk_engine.pump_detector import (
    PumpDetector
)

from backend.utils.whatsapp_alert import (
    send_whatsapp_alert
)


# =========================
# STREAM CONFIGURATION
# =========================

STREAMS = [
    "btcusdt@trade",
    "ethusdt@trade",
    "solusdt@trade",
    "dogeusdt@trade"
]

SOCKET = (
    "wss://stream.binance.com:9443/stream?streams="
    + "/".join(STREAMS)
)


# =========================
# ANALYTICS ENGINES
# =========================

metrics = LiveMetrics()

detector = AnomalyDetector()

scorer = RiskScorer()

pump_detector = PumpDetector()

volatility_tracker = VolatilityTracker()

last_print_time = time.time()

# =========================
# WHATSAPP ALERT COOLDOWN
# =========================

last_whatsapp_alert = {}


# =========================
# FORMAT TRADE DATA
# =========================

def format_trade_data(raw_data):

    data = raw_data["data"]

    return {

        "symbol": data["s"],

        "price": float(data["p"]),

        "quantity": float(data["q"]),

        "trade_time": datetime.fromtimestamp(
            data["T"] / 1000
        ).strftime("%Y-%m-%d %H:%M:%S"),

        "is_buyer_maker": data["m"]
    }


# =========================
# PRINT LIVE SUMMARY
# =========================

def print_summary():

    summary = metrics.get_summary()

    print("\n===== LIVE MARKET METRICS =====\n")

    for item in summary:

        print(
            f"{item['symbol']} | "
            f"Trades: {item['trades']} | "
            f"Volume: {item['volume']} | "
            f"Price Δ: {item['price_change_percent']}%"
        )

    print("\n===============================\n")


# =========================
# WEBSOCKET EVENTS
# =========================

def on_open(ws):

    print(
        "\nConnected to Binance Multi-Stream\n"
    )


def on_message(ws, message):

    global last_print_time

    raw_data = json.loads(message)

    formatted_data = format_trade_data(
        raw_data
    )

    # =========================
    # STORE LIVE TRADE
    # =========================

    trades_collection.insert_one(
        formatted_data
    )

    # =========================
    # UPDATE LIVE METRICS
    # =========================

    metrics.update_metrics(
        formatted_data
    )

    # =========================
    # ANOMALY DETECTION
    # =========================

    alert = detector.analyze_trade(
        formatted_data
    )

    # =========================
    # RISK SCORING
    # =========================

    risk = scorer.calculate_risk(
        formatted_data,
        alert
    )

    # =========================
    # PUMP DETECTION
    # =========================

    pump_alert = pump_detector.detect_pump(
        formatted_data
    )

    # =========================
    # VOLATILITY TRACKING
    # =========================

    volatility_data = (
        volatility_tracker.update(
            formatted_data
        )
    )

    # =========================
    # STORE ALERTS
    # =========================

    if alert:

        alert_document = {

            "symbol":
                formatted_data["symbol"],

            "trade_quantity":
                formatted_data["quantity"],

            "risk_score":
                risk["score"],

            "risk_level":
                risk["level"],

            "alert_type":
                alert["alert_type"],

            "timestamp":
                formatted_data["trade_time"]
        }

        alerts_collection.insert_one(
            alert_document
        )

        print("\n🚨 MARKET RISK ALERT 🚨")

        print(
            f"Symbol: "
            f"{formatted_data['symbol']}"
        )

        print(
            f"Trade Quantity: "
            f"{formatted_data['quantity']}"
        )

        print(
            f"Risk Score: "
            f"{risk['score']}/100"
        )

        print(
            f"Risk Level: "
            f"{risk['level']}"
        )

        # =========================
        # SMART WHATSAPP ALERTS
        # =========================

        current_time = time.time()

        symbol = formatted_data["symbol"]

        last_sent = (
            last_whatsapp_alert.get(
                symbol,
                0
            )
        )

        cooldown = 300  # 5 minutes

        if (

            risk["score"] >= 70

            and

            current_time - last_sent
            > cooldown
        ):

            try:

                whatsapp_message = (

                    f"🚨 CryptoShield AI Alert 🚨\n\n"

                    f"Symbol: "
                    f"{formatted_data['symbol']}\n"

                    f"Risk Level: "
                    f"{risk['level']}\n"

                    f"Risk Score: "
                    f"{risk['score']}/100\n"

                    f"Trade Quantity: "
                    f"{formatted_data['quantity']}"
                )

                send_whatsapp_alert(
                    whatsapp_message
                )

                last_whatsapp_alert[
                    symbol
                ] = current_time

                print(
                    "✅ WhatsApp Alert Sent"
                )

            except Exception as e:

                print(
                    "❌ WhatsApp Error:"
                )

                print(e)

    # =========================
    # PUMP DETECTION ALERT
    # =========================

    if pump_alert:

        print("\n🔥 POSSIBLE PUMP DETECTED 🔥")

        print(
            f"Symbol: "
            f"{pump_alert['symbol']}"
        )

        print(
            f"Pump Score: "
            f"{pump_alert['pump_score']}x"
        )

        print(
            f"Current Volume: "
            f"{pump_alert['current_volume']}"
        )

        print(
            f"Average Volume: "
            f"{pump_alert['average_volume']}"
        )

    # =========================
    # VOLATILITY ALERT
    # =========================

    if volatility_data:

        volatility = (
            volatility_data["volatility"]
        )

        if volatility > 50:

            print(
                f"\n⚠️ HIGH VOLATILITY: "
                f"{formatted_data['symbol']} | "
                f"Volatility: {volatility}"
            )

    # =========================
    # PRINT SUMMARY EVERY 10s
    # =========================

    current_time = time.time()

    if current_time - last_print_time >= 10:

        print_summary()

        last_print_time = current_time


def on_error(ws, error):

    print("Error:", error)


def on_close(ws, close_status_code, close_msg):

    print("\nWebSocket Closed")


# =========================
# START WEBSOCKET
# =========================

ws = WebSocketApp(
    SOCKET,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)


# =========================
# AUTO RECONNECT LOOP
# =========================

while True:

    try:

        ws.run_forever()

    except Exception as e:

        print(f"\nConnection Error: {e}")

        print(
            "Reconnecting in 5 seconds...\n"
        )

        time.sleep(5)