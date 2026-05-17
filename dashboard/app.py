import sys
import os
import requests

# =========================
# FIX PYTHON IMPORT PATH
# =========================

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

from streamlit_autorefresh import (
    st_autorefresh
)

from backend.analytics.market_summary import (
    MarketSummaryGenerator
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="CryptoShield AI",
    layout="wide"
)


# =========================
# LOGIN CONFIG
# =========================

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

authenticator = stauth.Authenticate(

    credentials,

    "cryptoshield_cookie",

    "abcdef",

    cookie_expiry_days=1
)


# =========================
# LOGIN UI
# =========================

authenticator.login(
    location="main"
)

name = st.session_state.get(
    "name"
)

authentication_status = (
    st.session_state.get(
        "authentication_status"
    )
)

username = st.session_state.get(
    "username"
)


# =========================
# LOGIN VALIDATION
# =========================

if authentication_status is False:

    st.error(
        "Incorrect username/password"
    )

elif authentication_status is None:

    st.warning(
        "Please login"
    )

elif authentication_status:

    # =========================
    # LOGOUT BUTTON
    # =========================

    authenticator.logout(
        "Logout",
        "sidebar"
    )

    st.sidebar.success(
        f"Welcome {name}"
    )

    # =========================
    # AUTO REFRESH
    # =========================

    st_autorefresh(
        interval=5000,
        key="dashboard_refresh"
    )

    # =========================
    # PAGE HEADER
    # =========================

    st.title(
        "🚨 CryptoShield AI"
    )

    st.subheader(
        "Real-Time Crypto Risk Intelligence Platform"
    )

    # =========================
    # FASTAPI CONFIG
    # =========================

    API_BASE_URL = (
        "https://cryptoshield-ai-9sak.onrender.com"
    )

    # =========================
    # FETCH API DATA
    # =========================

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

        trades = (
            trades_response.json()
        )

        alerts = (
            alerts_response.json()
        )

        metrics = (
            metrics_response.json()
        )

    except Exception as e:

        st.error(
            "FastAPI Backend Not Running"
        )

        st.stop()

    # =========================
    # DATAFRAMES
    # =========================

    trades_df = pd.DataFrame(
        trades
    )

    alerts_df = pd.DataFrame(
        alerts
    )

    # =========================
    # AI SUMMARY ENGINE
    # =========================

    summary_generator = (
        MarketSummaryGenerator()
    )

    # =========================
    # GENERATE AI SUMMARY
    # =========================

    summary = (
        summary_generator.generate_summary(
            alerts_df,
            trades_df
        )
    )

    # =========================
    # AI MARKET SUMMARY
    # =========================

    st.subheader(
        "🧠 AI Market Summary"
    )

    st.info(summary)

    # =========================
    # RISK TIMELINE ANALYTICS
    # =========================

    if not alerts_df.empty:

        st.subheader(
            "📈 Risk Timeline Analytics"
        )

        timeline_df = alerts_df.copy()

        timeline_df["timestamp"] = (
            pd.to_datetime(
                timeline_df["timestamp"]
            )
        )

        timeline_counts = (

            timeline_df

            .groupby(

                pd.Grouper(
                    key="timestamp",
                    freq="1min"
                )
            )

            .size()

            .reset_index(
                name="alert_count"
            )
        )

        timeline_fig = px.line(

            timeline_counts,

            x="timestamp",

            y="alert_count",

            title="Risk Alerts Over Time"
        )

        st.plotly_chart(

            timeline_fig,

            use_container_width=True
        )

    # =========================
    # TOP METRICS
    # =========================

    metric1, metric2, metric3 = (
        st.columns(3)
    )

    metric1.metric(
        "Total Trades",
        metrics["total_trades"]
    )

    metric2.metric(
        "Risk Alerts",
        metrics["total_alerts"]
    )

    metric3.metric(
        "Most Active Asset",
        metrics["most_active_asset"]
    )

    # =========================
    # RECENT ALERTS
    # =========================

    st.subheader(
        "🚨 Recent Risk Alerts"
    )

    if not alerts_df.empty:

        st.dataframe(

            alerts_df[
                [
                    "symbol",
                    "trade_quantity",
                    "risk_score",
                    "risk_level",
                    "timestamp"
                ]
            ],

            use_container_width=True,

            height=300
        )

    else:

        st.info(
            "No alerts detected yet."
        )

    # =========================
    # ANALYTICS ROW
    # =========================

    col_left, col_right = (
        st.columns(2)
    )

    # =========================
    # RISK DISTRIBUTION
    # =========================

    with col_left:

        if not alerts_df.empty:

            st.subheader(
                "⚠️ Risk Level Distribution"
            )

            risk_counts = (

                alerts_df[
                    "risk_level"
                ]

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

    # =========================
    # TOP RISKY ASSETS
    # =========================

    with col_right:

        if not alerts_df.empty:

            st.subheader(
                "🔥 Top Risky Assets"
            )

            risk_summary = (

                alerts_df

                .groupby("symbol")

                .agg({

                    "risk_score": "mean",

                    "symbol": "count"
                })

                .rename(columns={
                    "symbol": "alert_count"
                })

                .reset_index()
            )

            risk_summary[
                "risk_score"
            ] = (

                risk_summary[
                    "risk_score"
                ]

                .round(2)
            )

            risk_summary = (

                risk_summary

                .sort_values(
                    by="risk_score",
                    ascending=False
                )
            )

            st.dataframe(

                risk_summary,

                use_container_width=True,

                height=420
            )

    # =========================
    # VISUALIZATION ROW
    # =========================

    chart_left, chart_right = (
        st.columns(2)
    )

    # =========================
    # ASSET DISTRIBUTION
    # =========================

    with chart_left:

        if not trades_df.empty:

            st.subheader(
                "📊 Asset Trade Distribution"
            )

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

                values="count",

                title="Market Activity Distribution"
            )

            st.plotly_chart(

                pie_fig,

                use_container_width=True
            )

    # =========================
    # CANDLESTICK CHARTS
    # =========================

    with chart_right:

        st.subheader(
            "📉 Real-Time Price Charts"
        )

        if not trades_df.empty:

            chart_symbols = [

                "BTCUSDT",

                "ETHUSDT",

                "DOGEUSDT",

                "SOLUSDT"
            ]

            selected_symbol = (
                st.selectbox(
                    "Select Asset",
                    chart_symbols
                )
            )

            filtered_df = trades_df[
                trades_df["symbol"]
                == selected_symbol
            ]

            if not filtered_df.empty:

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

                fig.update_layout(

                    title=(
                        f"{selected_symbol} "
                        f"Candlestick Chart"
                    ),

                    xaxis_title="Time",

                    yaxis_title="Price",

                    height=500
                )

                st.plotly_chart(

                    fig,

                    use_container_width=True
                )

    # =========================
    # WHALE LEADERBOARD
    # =========================

    if not alerts_df.empty:

        st.subheader(
            "🐋 Whale Activity Leaderboard"
        )

        whale_df = (

            alerts_df

            .sort_values(
                by="trade_quantity",
                ascending=False
            )
        )

        whale_df = whale_df[
            [
                "symbol",
                "trade_quantity",
                "risk_score",
                "risk_level",
                "timestamp"
            ]
        ].head(10)

        st.dataframe(

            whale_df,

            use_container_width=True,

            height=400
        )

    # =========================
    # LIVE TRADE TABLE
    # =========================

    st.subheader(
        "📈 Live Market Trades"
    )

    if not trades_df.empty:

        st.dataframe(

            trades_df[
                [
                    "symbol",
                    "price",
                    "quantity",
                    "trade_time"
                ]
            ],

            use_container_width=True,

            height=400
        )

    else:

        st.info(
            "No live trades available."
        )