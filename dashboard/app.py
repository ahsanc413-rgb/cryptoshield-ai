# =============================================================
# dashboard/app.py
# CryptoShield AI — MongoDB SaaS Dashboard
# =============================================================

import os
import sys
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime

# =============================================================
# PATH FIX
# =============================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# =============================================================
# IMPORTS
# =============================================================

from backend.utils.auth import (
    hash_password,
    verify_password
)

from backend.database.users import (
    create_user,
    get_user
)

# =============================================================
# PAGE CONFIG
# =============================================================

st.set_page_config(

    page_title="CryptoShield AI",

    page_icon="🛡️",

    layout="wide",

    initial_sidebar_state="expanded"
)

# =============================================================
# CUSTOM CSS
# =============================================================

st.markdown("""

<style>

.stApp {

    background-color: #060b14;

    color: white;
}

section[data-testid="stSidebar"] {

    background-color: #0b1322;
}

div[data-testid="metric-container"] {

    background-color: #0b1322;

    border: 1px solid rgba(0,229,160,0.2);

    border-radius: 10px;

    padding: 15px;
}

.stButton > button {

    background-color: #00e5a0;

    color: black;

    font-weight: bold;

    border-radius: 8px;

    border: none;
}

</style>

""", unsafe_allow_html=True)

# =============================================================
# SESSION STATE
# =============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = ""

# =============================================================
# SIDEBAR
# =============================================================

with st.sidebar:

    st.title("🛡️ CryptoShield AI")

    st.markdown("---")

# =============================================================
# LOGIN / SIGNUP
# =============================================================

if not st.session_state.logged_in:

    st.title("🛡️ CryptoShield AI")

    st.subheader(
        "Enterprise Crypto Intelligence SaaS"
    )

    st.markdown("---")

    login_tab, signup_tab = st.tabs([
        "Login",
        "Signup"
    ])

    # =========================================================
    # SIGNUP TAB
    # =========================================================

    with signup_tab:

        st.subheader("🚀 Create Account")

        su_username = st.text_input(
            "Username",
            key="signup_username"
        )

        su_email = st.text_input(
            "Email",
            key="signup_email"
        )

        su_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        su_confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm"
        )

        if st.button("Create Account"):

            try:

                # =============================================
                # VALIDATION
                # =============================================

                if (
                    su_username == ""
                    or
                    su_email == ""
                    or
                    su_password == ""
                ):

                    st.error(
                        "Please fill all fields."
                    )

                elif su_password != su_confirm:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    # =========================================
                    # HASH PASSWORD
                    # =========================================

                    hashed_pw = hash_password(
                        su_password
                    )

                    # =========================================
                    # USER DATA
                    # =========================================

                    user_data = {

                        "username": su_username,

                        "email": su_email,

                        "password": hashed_pw,

                        "plan": "Free",

                        "created_at": str(
                            datetime.now()
                        )
                    }

                    # =========================================
                    # CREATE USER
                    # =========================================

                    success = create_user(
                        user_data
                    )

                    if success:

                        st.success(
                            "Account created successfully."
                        )

                    else:

                        st.error(
                            "Username already exists."
                        )

            except Exception as e:

                st.error(str(e))

    # =========================================================
    # LOGIN TAB
    # =========================================================

    with login_tab:

        st.subheader("🔐 Login")

        li_username = st.text_input(
            "Username",
            key="login_username"
        )

        li_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            try:

                user = get_user(
                    li_username
                )

                if user:

                    valid = verify_password(

                        li_password,

                        user["password"]
                    )

                    if valid:

                        st.session_state.logged_in = True

                        st.session_state.username = li_username

                        st.success(
                            "Login successful."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Invalid password."
                        )

                else:

                    st.error(
                        "User not found."
                    )

            except Exception as e:

                st.error(str(e))

    st.stop()

# =============================================================
# LOGGED IN SIDEBAR
# =============================================================

with st.sidebar:

    st.success(
        f"Welcome {st.session_state.username}"
    )

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()

# =============================================================
# DASHBOARD
# =============================================================

st.title("📊 CryptoShield AI Dashboard")

API_BASE_URL = (
    "https://cryptoshield-ai-9sak.onrender.com"
)

# =============================================================
# FETCH DATA
# =============================================================

trades = []
alerts = []

try:

    trades_response = requests.get(

        f"{API_BASE_URL}/api/trades",

        timeout=10
    )

    alerts_response = requests.get(

        f"{API_BASE_URL}/api/alerts",

        timeout=10
    )

    if trades_response.status_code == 200:

        trades = trades_response.json()

    if alerts_response.status_code == 200:

        alerts = alerts_response.json()

except Exception as e:

    st.error(
        f"API Error: {e}"
    )

# =============================================================
# DATAFRAMES
# =============================================================

trades_df = pd.DataFrame(trades)

alerts_df = pd.DataFrame(alerts)

# =============================================================
# METRICS
# =============================================================

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Trades",
    len(trades_df)
)

m2.metric(
    "Alerts",
    len(alerts_df)
)

m3.metric(
    "Assets",
    trades_df["symbol"].nunique()
    if not trades_df.empty
    else 0
)

m4.metric(
    "System",
    "LIVE"
)

st.divider()

# =============================================================
# LIVE TRADES
# =============================================================

st.subheader("📈 Live Trades")

if not trades_df.empty:

    st.dataframe(

        trades_df,

        use_container_width=True,

        height=350
    )

else:

    st.warning(
        "No live trades available."
    )

# =============================================================
# ALERTS
# =============================================================

st.subheader("🚨 Risk Alerts")

if not alerts_df.empty:

    st.dataframe(

        alerts_df,

        use_container_width=True,

        height=300
    )

else:

    st.success(
        "No alerts detected."
    )

# =============================================================
# CHARTS
# =============================================================

left_chart, right_chart = st.columns(2)

# =============================================================
# PIE CHART
# =============================================================

with left_chart:

    st.subheader("📊 Asset Distribution")

    if (
        not trades_df.empty
        and
        "symbol" in trades_df.columns
    ):

        symbol_counts = (

            trades_df["symbol"]

            .value_counts()

            .reset_index()
        )

        symbol_counts.columns = [
            "symbol",
            "count"
        ]

        fig = px.pie(

            symbol_counts,

            names="symbol",

            values="count",

            template="plotly_dark"
        )

        fig.update_layout(

            paper_bgcolor="#0b1322",

            plot_bgcolor="#0b1322"
        )

        st.plotly_chart(

            fig,

            use_container_width=True
        )

# =============================================================
# RISK BAR CHART
# =============================================================

with right_chart:

    st.subheader("⚠️ Risk Levels")

    if (
        not alerts_df.empty
        and
        "risk_level" in alerts_df.columns
    ):

        risk_counts = (

            alerts_df["risk_level"]

            .value_counts()

            .reset_index()
        )

        risk_counts.columns = [
            "risk_level",
            "count"
        ]

        fig2 = px.bar(

            risk_counts,

            x="risk_level",

            y="count",

            color="risk_level",

            template="plotly_dark"
        )

        fig2.update_layout(

            paper_bgcolor="#0b1322",

            plot_bgcolor="#0b1322"
        )

        st.plotly_chart(

            fig2,

            use_container_width=True
        )

# =============================================================
# AI SUMMARY
# =============================================================

st.divider()

st.subheader("🧠 AI Market Intelligence")

if not alerts_df.empty:

    st.warning(

        f"AI engine detected {len(alerts_df)} suspicious market activities."
    )

else:

    st.success(
        "Market currently stable."
    )

# =============================================================
# FOOTER
# =============================================================

st.divider()

st.caption(

    f"CryptoShield AI © 2026 | Updated: {datetime.now()}"
)