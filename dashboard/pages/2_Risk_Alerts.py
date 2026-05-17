import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Risk Alerts",
    page_icon="🚨",
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

.alert-box {
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #1f2937;
}

.high-risk {
    background-color: #450a0a;
}

.medium-risk {
    background-color: #78350f;
}

.low-risk {
    background-color: #052e16;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.title("🚨 CryptoShield AI — Risk Alerts")

st.markdown("""
AI-powered crypto threat monitoring and anomaly detection.
""")

# ==========================================
# FETCH ALL COINS
# ==========================================

@st.cache_data(ttl=60)
def get_market_data():

    url = (
        "https://api.binance.com/api/v3/ticker/24hr"
    )

    response = requests.get(url)

    data = response.json()

    filtered = []

    for coin in data:

        symbol = coin["symbol"]

        if symbol.endswith("USDT"):

            change = float(
                coin["priceChangePercent"]
            )

            volume = float(
                coin["quoteVolume"]
            )

            filtered.append({

                "Symbol": symbol,

                "Price": float(
                    coin["lastPrice"]
                ),

                "Change": change,

                "Volume": volume
            })

    return pd.DataFrame(filtered)

df = get_market_data()

# ==========================================
# AI RISK ENGINE
# ==========================================

risk_alerts = []

for _, row in df.iterrows():

    risk_score = 0

    reason = []

    # ======================================
    # HIGH VOLATILITY
    # ======================================

    if abs(row["Change"]) > 15:

        risk_score += 50

        reason.append(
            "Extreme volatility"
        )

    elif abs(row["Change"]) > 8:

        risk_score += 30

        reason.append(
            "High volatility"
        )

    # ======================================
    # HIGH VOLUME
    # ======================================

    if row["Volume"] > 100000000:

        risk_score += 25

        reason.append(
            "Whale activity"
        )

    # ======================================
    # POSSIBLE PUMP
    # ======================================

    if row["Change"] > 20:

        risk_score += 40

        reason.append(
            "Possible pump activity"
        )

    # ======================================
    # POSSIBLE DUMP
    # ======================================

    if row["Change"] < -20:

        risk_score += 40

        reason.append(
            "Possible dump activity"
        )

    # ======================================
    # DETERMINE RISK LEVEL
    # ======================================

    if risk_score >= 70:

        level = "HIGH"

    elif risk_score >= 40:

        level = "MEDIUM"

    else:

        level = "LOW"

    risk_alerts.append({

        "Symbol": row["Symbol"],

        "Price": row["Price"],

        "Change": row["Change"],

        "Volume": row["Volume"],

        "Risk Score": risk_score,

        "Risk Level": level,

        "Reason": ", ".join(reason)
    })

# ==========================================
# ALERT DATAFRAME
# ==========================================

alerts_df = pd.DataFrame(risk_alerts)

# ==========================================
# FILTER HIGH/MEDIUM RISK
# ==========================================

alerts_df = alerts_df[
    alerts_df["Risk Score"] > 0
]

alerts_df = alerts_df.sort_values(
    by="Risk Score",
    ascending=False
)

# ==========================================
# TOP METRICS
# ==========================================

high_risk_count = len(
    alerts_df[
        alerts_df["Risk Level"] == "HIGH"
    ]
)

medium_risk_count = len(
    alerts_df[
        alerts_df["Risk Level"] == "MEDIUM"
    ]
)

total_alerts = len(alerts_df)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Alerts",
        total_alerts
    )

with col2:

    st.metric(
        "High Risk",
        high_risk_count
    )

with col3:

    st.metric(
        "Medium Risk",
        medium_risk_count
    )

st.divider()

# ==========================================
# ALERT TABLE
# ==========================================

st.subheader("⚠️ Live Risk Alerts")

st.dataframe(
    alerts_df,
    use_container_width=True,
    height=500
)

# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.subheader("📊 Risk Distribution")

risk_counts = (
    alerts_df["Risk Level"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk Level",
    "Count"
]

fig = px.pie(
    risk_counts,
    names="Risk Level",
    values="Count",
    title="AI Risk Levels",
    template="plotly_dark"
)

fig.update_layout(
    paper_bgcolor="#050816",
    plot_bgcolor="#050816"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# HIGH RISK ALERTS
# ==========================================

st.subheader("🚨 Critical Alerts")

high_risk_df = alerts_df[
    alerts_df["Risk Level"] == "HIGH"
]

if not high_risk_df.empty:

    for _, row in high_risk_df.head(10).iterrows():

        st.markdown(f"""
        <div class="alert-box high-risk">

        <h3>{row['Symbol']}</h3>

        <b>Risk Score:</b> {row['Risk Score']}<br>

        <b>24h Change:</b> {row['Change']:.2f}%<br>

        <b>Reason:</b> {row['Reason']}

        </div>
        """, unsafe_allow_html=True)

else:

    st.success(
        "No critical threats detected."
    )

# ==========================================
# WHALE ACTIVITY
# ==========================================

st.subheader("🐋 Whale Activity Monitor")

whale_df = alerts_df[
    alerts_df["Volume"] > 100000000
]

if not whale_df.empty:

    st.dataframe(
        whale_df[
            [
                "Symbol",
                "Volume",
                "Risk Level",
                "Reason"
            ]
        ],
        use_container_width=True
    )

else:

    st.info(
        "No unusual whale activity detected."
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)