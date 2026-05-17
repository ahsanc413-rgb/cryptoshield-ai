import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="User Profile",
    page_icon="👤",
    layout="wide"
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

.profile-box {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #1f2937;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.title("👤 CryptoShield AI — User Profile")

st.markdown("""
Manage your account, watchlists, alerts, and subscription plan.
""")

# ==========================================
# DEMO USER DATA
# ==========================================

user_data = {

    "Username": "Ahsan",

    "Email": "ahsan@example.com",

    "Plan": "Pro",

    "Alerts Enabled": True,

    "WhatsApp Alerts": True,

    "Member Since": "2026-05-01"
}

# ==========================================
# PROFILE CARD
# ==========================================

st.subheader("🧑 Account Information")

st.markdown(f"""
<div class="profile-box">

<h2>{user_data['Username']}</h2>

<b>Email:</b> {user_data['Email']}<br><br>

<b>Subscription Plan:</b> {user_data['Plan']}<br><br>

<b>WhatsApp Alerts:</b> {user_data['WhatsApp Alerts']}<br><br>

<b>Member Since:</b> {user_data['Member Since']}

</div>
""", unsafe_allow_html=True)

# ==========================================
# EDIT PROFILE
# ==========================================

st.subheader("⚙️ Edit Profile")

with st.form("profile_form"):

    username = st.text_input(
        "Username",
        value=user_data["Username"]
    )

    email = st.text_input(
        "Email",
        value=user_data["Email"]
    )

    whatsapp_alerts = st.checkbox(
        "Enable WhatsApp Alerts",
        value=user_data["WhatsApp Alerts"]
    )

    submitted = st.form_submit_button(
        "Update Profile"
    )

    if submitted:

        st.success(
            "Profile updated successfully."
        )

# ==========================================
# WATCHLIST
# ==========================================

st.subheader("⭐ Watchlist")

watchlist = [

    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "DOGEUSDT"
]

watchlist_df = pd.DataFrame({

    "Watchlist Coins": watchlist
})

st.dataframe(
    watchlist_df,
    use_container_width=True
)

# ==========================================
# ALERT SETTINGS
# ==========================================

st.subheader("🚨 Alert Settings")

btc_alert = st.toggle(
    "BTC High Volatility Alerts",
    value=True
)

eth_alert = st.toggle(
    "ETH Whale Alerts",
    value=True
)

rugpull_alert = st.toggle(
    "Rug Pull Detection Alerts",
    value=True
)

if st.button("Save Alert Preferences"):

    st.success(
        "Alert settings saved."
    )

# ==========================================
# SUBSCRIPTION SECTION
# ==========================================

st.subheader("💳 Subscription Plan")

plan_col1, plan_col2, plan_col3 = st.columns(3)

with plan_col1:

    st.markdown("""
    ### Free

    - Basic Dashboard
    - Limited Alerts
    - Community Support
    """)

with plan_col2:

    st.markdown("""
    ### Pro

    - AI Analytics
    - Unlimited Alerts
    - WhatsApp Notifications
    - Whale Tracking
    """)

with plan_col3:

    st.markdown("""
    ### Enterprise

    - API Access
    - Advanced ML
    - Multi-user Team Access
    - Premium Monitoring
    """)

st.button("Upgrade Plan")

# ==========================================
# ACTIVITY LOGS
# ==========================================

st.subheader("📜 Recent Activity")

activity_logs = pd.DataFrame({

    "Time": [

        "2026-05-18 01:00",
        "2026-05-18 00:45",
        "2026-05-17 23:10"
    ],

    "Activity": [

        "Logged into dashboard",
        "Viewed AI Analytics",
        "Enabled Whale Alerts"
    ]
})

st.dataframe(
    activity_logs,
    use_container_width=True
)

# ==========================================
# SECURITY SETTINGS
# ==========================================

st.subheader("🔒 Security")

change_password = st.button(
    "Change Password"
)

enable_2fa = st.button(
    "Enable Two-Factor Authentication"
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    f"Profile Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)