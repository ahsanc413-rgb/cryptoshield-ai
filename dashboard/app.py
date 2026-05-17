
import os
import sys
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit_authenticator as stauth

# =====================================
# PYTHON PATH FIX
# =====================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# =====================================
# OPTIONAL AUTO REFRESH
# =====================================

try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH = True
except:
    AUTO_REFRESH = False

# =====================================
# STREAMLIT CONFIG
# =====================================

st.set_page_config(
    page_title="CryptoShield AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM UI
# =====================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #050816;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    .metric-card {
        background: #111827;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1f2937;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# LOGIN SYSTEM
# =====================================

names = ["Ahsan"]
usernames = ["admin"]
passwords = ["admin123"]

credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "cryptoshield_cookie",
    "cryptoshield_ai_secure_key_2026_super_secret",
    cookie_expiry_days=30
)

# =====================================
# LOGIN UI
# =====================================

authenticator.login(location="main")

name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

# =====================================
# LOGIN VALIDATION
# =====================================

if authentication_status is False:

    st.error("Incorrect username/password")

elif authentication_status is None:

    st.warning("Please login to continue")

elif authentication_status:

    authenticator.logout(
        "Logout",
        "sidebar"
    )

    st.sidebar.success(
        f"Welcome {name}"
    )

    st.sidebar.title("CryptoShield AI")

    st.sidebar.markdown("---")

    st.sidebar.info(
        "AI-powered crypto risk monitoring SaaS"
    )

    # =====================================
    # AUTO REFRESH
    # =====================================

    if AUTO_REFRESH:

        st_autorefresh(
            interval=5000,
            key="dashboard_refresh"
        )

    # =====================================
    # HEADER
    # =====================================

    st.title("🚨 CryptoShield AI")

    st.subheader(
        "Real-Time Crypto Risk Intelligence Platform"
    )

    # =====================================
    # BACKEND API
    # =====================================

    API_BASE_URL = (
        "https://cryptoshield-ai-9sak.onrender.com"
    )

    # =====================================
    # FETCH DATA
    # =====================================

    try:

        trades_response = requests.get(
            f"{API_BASE_URL}/api/trades"
        )

        alerts_response = requests.get(
            f"{API_BASE_URL}/api/alerts"
        )

        metrics_response = requests.get(
            f"{API_BASE_URL}/api/metrics"
        )

        trades = trades_response.json()
        alerts = alerts_response.json()
        metrics = metrics_response.json()

    except Exception:

        st.error(
            "Backend API not reachable"
        )

        st.stop()

    # =====================================
    # DATAFRAMES
    # =====================================

    trades_df = pd.DataFrame(trades)
    alerts_df = pd.DataFrame(alerts)

    # =====================================
    # METRICS ROW
    # =====================================

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Total Trades",
        metrics.get("total_trades", 0)
    )

    metric2.metric(
        "Risk Alerts",
        metrics.get("total_alerts", 0)
    )

    metric3.metric(
        "Most Active Asset",
        metrics.get("most_active_asset", "N/A")
    )

    metric4.metric(
        "System Status",
        "LIVE"
    )

    st.divider()

    # =====================================
    # ALERTS TABLE
    # =====================================

    st.subheader("🚨 Recent Risk Alerts")

    if not alerts_df.empty:

        st.dataframe(
            alerts_df,
            use_container_width=True,
            height=320
        )

    else:

        st.info("No alerts detected")

    # =====================================
    # LIVE MARKET TABLE
    # =====================================

    st.subheader("📈 Live Market Trades")

    if not trades_df.empty:

        st.dataframe(
            trades_df,
            use_container_width=True,
            height=400
        )

    else:

        st.warning("No market data available")

    # =====================================
    # CHARTS ROW
    # =====================================

    chart_left, chart_right = st.columns(2)

    # =====================================
    # PIE CHART
    # =====================================

    with chart_left:

        if not trades_df.empty:

            st.subheader("📊 Asset Distribution")

            symbol_counts = (
                trades_df["symbol"]
                .value_counts()
                .reset_index()
            )

            symbol_counts.columns = [
                "symbol",
                "count"
            ]

            pie_fig = px.pie(
                symbol_counts,
                names="symbol",
                values="count",
                title="Trading Activity"
            )

            st.plotly_chart(
                pie_fig,
                use_container_width=True
            )

    # =====================================
    # RISK CHART
    # =====================================

    with chart_right:

        if not alerts_df.empty:

            st.subheader("⚠️ Risk Distribution")

            risk_counts = (
                alerts_df["risk_level"]
                .value_counts()
                .reset_index()
            )

            risk_counts.columns = [
                "risk_level",
                "count"
            ]

            risk_fig = px.bar(
                risk_counts,
                x="risk_level",
                y="count",
                title="Detected Risk Levels"
            )

            st.plotly_chart(
                risk_fig,
                use_container_width=True
            )

    # =====================================
    # CANDLESTICK CHART
    # =====================================

    if not trades_df.empty:

        st.subheader("📉 Live Candlestick Chart")

        symbols = trades_df["symbol"].unique()

        selected_symbol = st.selectbox(
            "Select Asset",
            symbols
        )

        filtered_df = trades_df[
            trades_df["symbol"] == selected_symbol
        ]

        if not filtered_df.empty:

            filtered_df["trade_time"] = pd.to_datetime(
                filtered_df["trade_time"]
            )

            candle_data = (
                filtered_df
                .groupby(
                    pd.Grouper(
                        key="trade_time",
                        freq="1min"
                    )
                )
                .agg({
                    "price": [
                        "first",
                        "max",
                        "min",
                        "last"
                    ]
                })
            )

            candle_data.columns = [
                "open",
                "high",
                "low",
                "close"
            ]

            candle_data = (
                candle_data
                .dropna()
                .reset_index()
            )

            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=candle_data["trade_time"],
                        open=candle_data["open"],
                        high=candle_data["high"],
                        low=candle_data["low"],
                        close=candle_data["close"]
                    )
                ]
            )

            fig.update_layout(
                title=f"{selected_symbol} Live Chart",
                height=550
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # =====================================
    # AI SUMMARY SECTION
    # =====================================

    st.subheader("🧠 AI Market Intelligence")

    if not alerts_df.empty:

        high_risk = alerts_df[
            alerts_df["risk_level"] == "HIGH"
        ]

        st.info(
            f"Detected {len(high_risk)} high-risk market events in live trading streams."
        )

    # =====================================
    # FOOTER
    # =====================================

    st.divider()

    st.caption(
        "CryptoShield AI © 2026 • Enterprise Crypto Intelligence SaaS"
    )
