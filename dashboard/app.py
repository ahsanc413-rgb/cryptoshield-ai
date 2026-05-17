import os
import sys
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# PYTHON PATH FIX
# ==========================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# ==========================================
# OPTIONAL AUTO REFRESH
# ==========================================

AUTO_REFRESH = False

try:

    from streamlit_autorefresh import st_autorefresh

    AUTO_REFRESH = True

except:

    AUTO_REFRESH = False

# ==========================================
# STREAMLIT CONFIG
# ==========================================

st.set_page_config(

    page_title="CryptoShield AI",

    page_icon="🚨",

    layout="wide",

    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.metric-card {

    background-color: #111827;

    padding: 20px;

    border-radius: 15px;

    border: 1px solid #1f2937;
}

div[data-testid="metric-container"] {

    background-color: #111827;

    border: 1px solid #1f2937;

    padding: 15px;

    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🚨 CryptoShield AI")

st.sidebar.markdown("---")

# ==========================================
# LOGIN PAGE
# ==========================================

if not st.session_state.logged_in:

    st.title("🚨 CryptoShield AI")

    st.subheader(
        "Real-Time Crypto Risk Intelligence Platform"
    )

    st.markdown("---")

    login_tab, signup_tab = st.tabs([
        "Login",
        "Signup"
    ])

    # ======================================
    # LOGIN
    # ======================================

    with login_tab:

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True

                st.session_state.username = username

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "Invalid credentials"
                )

    # ======================================
    # SIGNUP
    # ======================================

    with signup_tab:

        new_username = st.text_input(
            "Create Username"
        )

        new_email = st.text_input(
            "Email"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Create Account"):

            st.success(
                "Account created successfully."
            )

            st.info(
                "You can now login."
            )

    st.stop()

# ==========================================
# LOGGED IN SIDEBAR
# ==========================================

st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()

st.sidebar.markdown("---")

# ==========================================
# AUTO REFRESH
# ==========================================

if AUTO_REFRESH:

    st_autorefresh(

        interval=5000,

        key="dashboard_refresh"
    )

# ==========================================
# HEADER
# ==========================================

st.title("🚨 CryptoShield AI")

st.subheader(
    "Enterprise Crypto Intelligence SaaS Platform"
)

# ==========================================
# BACKEND URL
# ==========================================

API_BASE_URL = (
    "https://cryptoshield-ai-9sak.onrender.com"
)

# ==========================================
# FETCH API DATA
# ==========================================

trades = []
alerts = []
metrics = {}

try:

    trades_response = requests.get(
        f"{API_BASE_URL}/api/trades",
        timeout=10
    )

    alerts_response = requests.get(
        f"{API_BASE_URL}/api/alerts",
        timeout=10
    )

    metrics_response = requests.get(
        f"{API_BASE_URL}/api/metrics",
        timeout=10
    )

    if trades_response.status_code == 200:

        trades = trades_response.json()

    if alerts_response.status_code == 200:

        alerts = alerts_response.json()

    if metrics_response.status_code == 200:

        metrics = metrics_response.json()

except Exception as e:

    st.warning(
        "Backend API temporarily unavailable."
    )

# ==========================================
# DATAFRAMES
# ==========================================

trades_df = pd.DataFrame(trades)

alerts_df = pd.DataFrame(alerts)

# ==========================================
# METRICS
# ==========================================

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(

    "Total Trades",

    metrics.get(
        "total_trades",
        len(trades_df)
    )
)

metric2.metric(

    "Risk Alerts",

    metrics.get(
        "total_alerts",
        len(alerts_df)
    )
)

metric3.metric(

    "Active Assets",

    metrics.get(
        "active_assets",
        trades_df["symbol"].nunique()
        if not trades_df.empty
        else 0
    )
)

metric4.metric(

    "System Status",

    "LIVE"
)

st.divider()

# ==========================================
# MARKET TABLE
# ==========================================

st.subheader("📈 Live Market Trades")

if not trades_df.empty:

    st.dataframe(

        trades_df,

        use_container_width=True,

        height=350
    )

else:

    st.info(
        "Waiting for live market data..."
    )

# ==========================================
# ALERTS TABLE
# ==========================================

st.subheader("🚨 Live Risk Alerts")

if not alerts_df.empty:

    st.dataframe(

        alerts_df,

        use_container_width=True,

        height=300
    )

else:

    st.success(
        "No high-risk alerts detected."
    )

# ==========================================
# CHARTS
# ==========================================

chart_left, chart_right = st.columns(2)

# ==========================================
# ASSET DISTRIBUTION
# ==========================================

with chart_left:

    st.subheader("📊 Asset Distribution")

    if not trades_df.empty:

        symbol_counts = (
            trades_df["symbol"]
            .value_counts()
            .reset_index()
        )

        symbol_counts.columns = [
            "symbol",
            "count"
        ]

        fig_pie = px.pie(

            symbol_counts,

            names="symbol",

            values="count",

            template="plotly_dark"
        )

        fig_pie.update_layout(

            paper_bgcolor="#050816",

            plot_bgcolor="#050816"
        )

        st.plotly_chart(

            fig_pie,

            use_container_width=True
        )

# ==========================================
# RISK CHART
# ==========================================

with chart_right:

    st.subheader("⚠️ Risk Levels")

    if not alerts_df.empty:

        if "risk_level" in alerts_df.columns:

            risk_counts = (
                alerts_df["risk_level"]
                .value_counts()
                .reset_index()
            )

            risk_counts.columns = [
                "risk_level",
                "count"
            ]

            fig_bar = px.bar(

                risk_counts,

                x="risk_level",

                y="count",

                color="risk_level",

                template="plotly_dark"
            )

            fig_bar.update_layout(

                paper_bgcolor="#050816",

                plot_bgcolor="#050816"
            )

            st.plotly_chart(

                fig_bar,

                use_container_width=True
            )

# ==========================================
# LIVE CANDLESTICK
# ==========================================

if not trades_df.empty:

    if "symbol" in trades_df.columns:

        st.subheader("📉 Live Candlestick")

        symbols = trades_df["symbol"].unique()

        selected_symbol = st.selectbox(

            "Select Coin",

            symbols
        )

        filtered_df = trades_df[
            trades_df["symbol"]
            == selected_symbol
        ]

        if not filtered_df.empty:

            if "trade_time" in filtered_df.columns:

                filtered_df[
                    "trade_time"
                ] = pd.to_datetime(
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

                if not candle_data.empty:

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

                        template="plotly_dark",

                        paper_bgcolor="#050816",

                        plot_bgcolor="#050816",

                        height=600
                    )

                    st.plotly_chart(

                        fig,

                        use_container_width=True
                    )

# ==========================================
# AI MARKET SUMMARY
# ==========================================

st.subheader("🧠 AI Market Intelligence")

if not alerts_df.empty:

    st.warning(

        f"AI engine detected {len(alerts_df)} suspicious market activities."
    )

else:

    st.success(
        "Market currently stable."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(

    f"CryptoShield AI © 2026 | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)