import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from datetime import datetime

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Analytics",
    page_icon="🧠",
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

.ai-box {
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #1f2937;
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.title("🧠 CryptoShield AI — AI Analytics")

st.markdown("""
Machine learning powered crypto anomaly detection engine.
""")

# ==========================================
# FETCH MARKET DATA
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

            filtered.append({

                "Symbol": symbol,

                "Price": float(
                    coin["lastPrice"]
                ),

                "Change": float(
                    coin["priceChangePercent"]
                ),

                "Volume": float(
                    coin["quoteVolume"]
                ),

                "Trades": int(
                    coin["count"]
                )
            })

    return pd.DataFrame(filtered)

df = get_market_data()

# ==========================================
# FEATURE ENGINEERING
# ==========================================

features = df[
    [
        "Price",
        "Change",
        "Volume",
        "Trades"
    ]
]

# ==========================================
# ISOLATION FOREST MODEL
# ==========================================

model = IsolationForest(

    contamination=0.03,

    random_state=42
)

model.fit(features)

# ==========================================
# PREDICTIONS
# ==========================================

df["Anomaly"] = model.predict(features)

df["AI Score"] = np.abs(
    model.decision_function(features)
) * 100

# ==========================================
# LABELS
# ==========================================

df["Threat Level"] = df["Anomaly"].apply(
    lambda x: (
        "HIGH RISK"
        if x == -1
        else "NORMAL"
    )
)

# ==========================================
# SORT
# ==========================================

df = df.sort_values(
    by="AI Score",
    ascending=False
)

# ==========================================
# TOP METRICS
# ==========================================

high_risk_count = len(
    df[
        df["Threat Level"] == "HIGH RISK"
    ]
)

avg_ai_score = round(
    df["AI Score"].mean(),
    2
)

top_anomaly = df.iloc[0]["Symbol"]

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "High Risk Coins",
        high_risk_count
    )

with col2:

    st.metric(
        "Average AI Score",
        avg_ai_score
    )

with col3:

    st.metric(
        "Top Anomaly",
        top_anomaly
    )

st.divider()

# ==========================================
# HIGH RISK COINS
# ==========================================

st.subheader("🚨 AI Detected Anomalies")

high_risk_df = df[
    df["Threat Level"] == "HIGH RISK"
]

if not high_risk_df.empty:

    st.dataframe(
        high_risk_df[
            [
                "Symbol",
                "Price",
                "Change",
                "Volume",
                "AI Score",
                "Threat Level"
            ]
        ],
        use_container_width=True,
        height=500
    )

else:

    st.success(
        "No major anomalies detected."
    )

# ==========================================
# AI SCORE DISTRIBUTION
# ==========================================

st.subheader("📊 AI Threat Distribution")

fig = px.histogram(
    df,
    x="AI Score",
    nbins=30,
    color="Threat Level",
    template="plotly_dark",
    title="AI Risk Score Distribution"
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
# TOP AI THREATS
# ==========================================

st.subheader("⚠️ Top AI Threats")

top_threats = df.head(10)

for _, row in top_threats.iterrows():

    if row["Threat Level"] == "HIGH RISK":

        st.markdown(f"""
        <div class="ai-box">

        <h3>{row['Symbol']}</h3>

        <b>AI Score:</b> {row['AI Score']:.2f}<br>

        <b>24h Change:</b> {row['Change']:.2f}%<br>

        <b>Volume:</b> {row['Volume']:,.0f}<br>

        <b>Status:</b>
        <span style='color:red'>
        HIGH RISK
        </span>

        </div>
        """, unsafe_allow_html=True)

# ==========================================
# COIN SEARCH
# ==========================================

st.subheader("🔍 Analyze Specific Coin")

coin_list = sorted(
    df["Symbol"].tolist()
)

selected_coin = st.selectbox(
    "Select Coin",
    coin_list
)

coin_info = df[
    df["Symbol"] == selected_coin
].iloc[0]

st.markdown(f"""
<div class="ai-box">

<h2>{selected_coin}</h2>

<b>Price:</b> ${coin_info['Price']:,.4f}<br>

<b>24h Change:</b> {coin_info['Change']:.2f}%<br>

<b>Volume:</b> {coin_info['Volume']:,.0f}<br>

<b>AI Score:</b> {coin_info['AI Score']:.2f}<br>

<b>Threat Level:</b> {coin_info['Threat Level']}

</div>
""", unsafe_allow_html=True)

# ==========================================
# AI INTERPRETATION
# ==========================================

st.subheader("🤖 AI Interpretation")

if coin_info["Threat Level"] == "HIGH RISK":

    st.error(
        f"""
        {selected_coin} shows abnormal market behavior.
        Possible causes:
        - Whale manipulation
        - Pump & dump activity
        - Extreme volatility
        - Abnormal volume spikes
        """
    )

else:

    st.success(
        f"""
        {selected_coin} currently shows
        relatively stable market behavior.
        """
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)