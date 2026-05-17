import sys
import os
import requests
from datetime import datetime

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit_authenticator as stauth

# ==========================================
# SAFE AUTO REFRESH IMPORT
# ==========================================

try:
    from streamlit_autorefresh import (
        st_autorefresh
    )
except:

    def st_autorefresh(*args, **kwargs):
        pass


# ==========================================
# PAGE CONFIG
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

html, body, [class*="css"] {

    background-color: #0E1117;
    color: white;
    font-family: Arial;
}

.stApp {
    background-color: #0E1117;
}

.main-title {

    font-size: 55px;
    font-weight: bold;
    color: white;
}

.sub-title {

    font-size: 22px;
    color: #A1A1AA;
    margin-bottom: 20px;
}

.metric-card {

    background: #161B22;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #30363D;
}

.metric-label {

    color: #9CA3AF;
    font-size: 16px;
}

.metric-value {

    font-size: 30px;
    font-weight: bold;
    color: white;
}

.success-box {

    background: #052e16;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #14532d;
}

.warning-box {

    background: #3f2f00;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #854d0e;
}

.danger-box {

    background: #450a0a;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #991b1b;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOGIN CONFIG
# ==========================================

names = [
    "Ahsan"
]

usernames = [
    "admin"
]

passwords = [
    "admin123"
]

credentials = {

    "usernames": {

        usernames[0]: {

            "name": names[0],

            "password": passwords[0]
        }
    }
}


# ==========================================
# AUTHENTICATION
# ==========================================

authenticator = stauth.Authenticate(

    credentials,

    "cryptoshield_cookie",

    "abcdef",

    cookie_expiry_days=7
)


# ==========================================
# LOGIN SYSTEM
# ==========================================

authenticator.login(
    location="main"
)

name = st.session_state.get(
    "name"
)

authentication_status = st.session_state.get(
    "authentication_status"
)


# ==========================================
# LOGIN CHECK
# ==========================================

if authentication_status is False:

    st.error(
        "Incorrect username/password"
    )

elif authentication_status is None:

    st.warning(
        "Please login"
    )

elif authentication_status:

    # ==========================================
    # SIDEBAR
    # ==========================================

    authenticator.logout(
        "Logout",
        "sidebar"
    )

    st.sidebar.success(
        f"Welcome {name}"
    )

    st.sidebar.title(
        "🛡️ CryptoShield AI"
    )

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "AI Detection",
            "Whale Alerts",
            "WhatsApp Alerts",
            "User Profile",
            "SaaS Plans",
            "Settings"
        ]
    )

    st_autorefresh(
        interval=15000,
        key="dashboard_refresh"
    )

    # ==========================================
    # LIVE API
    # ==========================================

    API_BASE_URL = (
        "https://cryptoshield-ai-9sak.onrender.com"
    )

    trades = []
    alerts = []
    metrics = {}

    try:

        trades_response = requests.get(
            f"{API_BASE_URL}/api/trades",
            timeout=15
        )

        alerts_response = requests.get(
            f"{API_BASE_URL}/api/alerts",
            timeout=15
        )

        metrics_response = requests.get(
            f"{API_BASE_URL}/api/metrics",
            timeout=15
        )

        if trades_response.status_code == 200:
            trades = trades_response.json()

        if alerts_response.status_code == 200:
            alerts = alerts_response.json()

        if metrics_response.status_code == 200:
            metrics = metrics_response.json()

    except Exception:

        st.warning(
            "Backend sleeping or temporarily unavailable"
        )

    trades_df = pd.DataFrame(trades)
    alerts_df = pd.DataFrame(alerts)

    # ==========================================
    # DASHBOARD
    # ==========================================

    if menu == "Dashboard":

        st.markdown(
            '<div class="main-title">🚨 CryptoShield AI</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sub-title">AI-Powered Crypto Risk Intelligence Platform</div>',
            unsafe_allow_html=True
        )

        # ==========================================
        # METRICS
        # ==========================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f'''
                <div class="metric-card">
                    <div class="metric-label">Total Trades</div>
                    <div class="metric-value">{metrics.get("total_trades", 0)}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f'''
                <div class="metric-card">
                    <div class="metric-label">Risk Alerts</div>
                    <div class="metric-value">{metrics.get("total_alerts", 0)}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f'''
                <div class="metric-card">
                    <div class="metric-label">Most Active</div>
                    <div class="metric-value">{metrics.get("most_active_asset", "BTCUSDT")}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )

        with col4:

            st.markdown(
                '''
                <div class="metric-card">
                    <div class="metric-label">System Status</div>
                    <div class="metric-value">LIVE</div>
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.divider()

        # ==========================================
        # AI SUMMARY
        # ==========================================

        st.subheader(
            "🧠 AI Market Summary"
        )

        if not alerts_df.empty:

            high_risk = len(
                alerts_df[
                    alerts_df["risk_score"] > 80
                ]
            )

            st.markdown(
                f'''
                <div class="warning-box">
                ⚠️ AI detected {high_risk} high-risk market events.
                Whale activity and suspicious patterns detected.
                </div>
                ''',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '''
                <div class="success-box">
                ✅ Market conditions stable.
                No significant anomalies detected.
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.divider()

        # ==========================================
        # LIVE TABLES
        # ==========================================

        left, right = st.columns(2)

        with left:

            st.subheader(
                "📈 Live Trades"
            )

            if not trades_df.empty:

                st.dataframe(
                    trades_df.head(100),
                    use_container_width=True,
                    height=400
                )

            else:

                st.info(
                    "No live trades available"
                )

        with right:

            st.subheader(
                "🚨 Risk Alerts"
            )

            if not alerts_df.empty:

                st.dataframe(
                    alerts_df.head(100),
                    use_container_width=True,
                    height=400
                )

            else:

                st.success(
                    "No active threats"
                )

        st.divider()

        # ==========================================
        # CHARTS
        # ==========================================

        chart_left, chart_right = st.columns(2)

        with chart_left:

            st.subheader(
                "📊 Asset Distribution"
            )

            if (
                not trades_df.empty
                and "symbol" in trades_df.columns
            ):

                symbol_counts = (
                    trades_df[
                        "symbol"
                    ]
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
                    values="count"
                )

                st.plotly_chart(
                    pie_fig,
                    use_container_width=True
                )

        with chart_right:

            st.subheader(
                "📉 Candlestick Chart"
            )

            if (
                not trades_df.empty
                and "symbol" in trades_df.columns
                and "price" in trades_df.columns
                and "trade_time" in trades_df.columns
            ):

                chart_symbols = [
                    "BTCUSDT",
                    "ETHUSDT",
                    "DOGEUSDT",
                    "SOLUSDT"
                ]

                selected_symbol = st.selectbox(
                    "Select Asset",
                    chart_symbols
                )

                filtered_df = trades_df[
                    trades_df["symbol"]
                    == selected_symbol
                ]

                if not filtered_df.empty:

                    filtered_df[
                        "trade_time"
                    ] = pd.to_datetime(
                        filtered_df[
                            "trade_time"
                        ]
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
                                x=candle_data[
                                    "trade_time"
                                ],
                                open=candle_data[
                                    "open"
                                ],
                                high=candle_data[
                                    "high"
                                ],
                                low=candle_data[
                                    "low"
                                ],
                                close=candle_data[
                                    "close"
                                ]
                            )
                        ]
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

    # ==========================================
    # AI DETECTION
    # ==========================================

    elif menu == "AI Detection":

        st.title(
            "🤖 AI Scam Detection"
        )

        suspicious_text = st.text_area(
            "Paste suspicious crypto message"
        )

        if st.button(
            "Analyze Message"
        ):

            keywords = [
                "guaranteed",
                "double",
                "100%",
                "free usdt",
                "send btc"
            ]

            detected = False

            for word in keywords:

                if word in suspicious_text.lower():
                    detected = True

            if detected:

                st.markdown(
                    '''
                    <div class="danger-box">
                    🚨 HIGH RISK SCAM DETECTED
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '''
                    <div class="success-box">
                    ✅ Message appears safe
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

    # ==========================================
    # WHALE ALERTS
    # ==========================================

    elif menu == "Whale Alerts":

        st.title(
            "🐋 Whale Activity Dashboard"
        )

        if not alerts_df.empty:

            whale_df = alerts_df.sort_values(
                by="trade_quantity",
                ascending=False
            )

            st.dataframe(
                whale_df.head(20),
                use_container_width=True
            )

        else:

            st.info(
                "No whale activity available"
            )

    # ==========================================
    # WHATSAPP ALERTS
    # ==========================================

    elif menu == "WhatsApp Alerts":

        st.title(
            "📱 WhatsApp Alert System"
        )

        phone = st.text_input(
            "Enter WhatsApp Number"
        )

        alert_type = st.selectbox(
            "Alert Type",
            [
                "Whale Alerts",
                "Scam Alerts",
                "Market Crash",
                "All Alerts"
            ]
        )

        if st.button(
            "Enable Alerts"
        ):

            st.success(
                f"WhatsApp alerts enabled for {phone}"
            )

    # ==========================================
    # USER PROFILE
    # ==========================================

    elif menu == "User Profile":

        st.title(
            "👤 User Profile"
        )

        st.text_input(
            "Username",
            value=name
        )

        st.text_input(
            "Subscription",
            value="PRO"
        )

        st.success(
            "Profile Loaded"
        )

    # ==========================================
    # SAAS PLANS
    # ==========================================

    elif menu == "SaaS Plans":

        st.title(
            "💳 CryptoShield SaaS Plans"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                '''
                ### FREE
                $0/month

                - Basic Monitoring
                - Public Dashboard
                - Limited Alerts
                '''
            )

        with col2:

            st.markdown(
                '''
                ### PRO
                $19/month

                - AI Detection
                - WhatsApp Alerts
                - Whale Tracking
                - Premium Analytics
                '''
            )

        with col3:

            st.markdown(
                '''
                ### ENTERPRISE
                $99/month

                - Full AI Suite
                - API Access
                - Unlimited Monitoring
                - Priority Support
                '''
            )

    # ==========================================
    # SETTINGS
    # ==========================================

    elif menu == "Settings":

        st.title(
            "⚙️ Settings"
        )

        st.selectbox(
            "Theme",
            [
                "Dark",
                "Light"
            ]
        )

        st.slider(
            "Refresh Interval",
            5,
            60,
            15
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    f"CryptoShield AI © {datetime.now().year}"
)