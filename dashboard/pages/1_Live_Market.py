# dashboard/pages/1_Live_Market.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Live Market",
    page_icon="📈",
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

.metric-card {
    background: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.title("📈 CryptoShield AI — Live Market")

st.markdown("""
Professional real-time cryptocurrency intelligence dashboard.
""")

# ==========================================
# FETCH ALL BINANCE SYMBOLS
# ==========================================

@st.cache_data(ttl=300)
def get_all_symbols():

    url = (
        "https://api.binance.com/api/v3/ticker/24hr"
    )

    response = requests.get(url)

    data = response.json()

    usdt_pairs = []

    for coin in data:

        symbol = coin["symbol"]

        if symbol.endswith("USDT"):

            usdt_pairs.append(symbol)

    usdt_pairs = sorted(usdt_pairs)

    return usdt_pairs


# ==========================================
# LOAD ALL COINS
# ==========================================

all_symbols = get_all_symbols()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Market Controls")

selected_symbol = st.sidebar.selectbox(
    "Select Coin",
    all_symbols,
    index=0
)

refresh_rate = st.sidebar.slider(
    "Refresh Rate (seconds)",
    5,
    60,
    10
)

# ==========================================
# FETCH SELECTED COIN DATA
# ==========================================

@st.cache_data(ttl=10)
def get_coin_data(symbol):

    url = (
        f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    )

    response = requests.get(url)

    return response.json()

coin_data = get_coin_data(selected_symbol)

# ==========================================
# METRICS
# ==========================================

price = float(
    coin_data["lastPrice"]
)

change = float(
    coin_data["priceChangePercent"]
)

volume = float(
    coin_data["volume"]
)

high_price = float(
    coin_data["highPrice"]
)

low_price = float(
    coin_data["lowPrice"]
)

# ==========================================
# METRIC ROW
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Coin",
        selected_symbol
    )

with col2:

    st.metric(
        "Current Price",
        f"${price:,.4f}"
    )

with col3:

    st.metric(
        "24h Change",
        f"{change:.2f}%"
    )

with col4:

    st.metric(
        "24h Volume",
        f"{volume:,.2f}"
    )

st.divider()

# ==========================================
# RISK LEVEL
# ==========================================

st.subheader("⚠️ AI Risk Analysis")

if abs(change) > 10:

    risk = "HIGH RISK"

    color = "red"

elif abs(change) > 5:

    risk = "MEDIUM RISK"

    color = "orange"

else:

    risk = "LOW RISK"

    color = "green"

st.markdown(f"""
## Risk Level:
<span style='color:{color}; font-weight:bold'>
{risk}
</span>
""", unsafe_allow_html=True)

st.progress(
    min(abs(change) / 20, 1.0)
)

# ==========================================
# PRICE DETAILS
# ==========================================

st.subheader("📊 Market Statistics")

stats_df = pd.DataFrame({

    "Metric": [
        "Current Price",
        "24h High",
        "24h Low",
        "24h Change %",
        "Volume"
    ],

    "Value": [
        f"${price:,.4f}",
        f"${high_price:,.4f}",
        f"${low_price:,.4f}",
        f"{change:.2f}%",
        f"{volume:,.2f}"
    ]
})

st.dataframe(
    stats_df,
    use_container_width=True
)

# ==========================================
# SIMPLE CHART
# ==========================================

st.subheader("📈 Price Visualization")

chart_df = pd.DataFrame({

    "Type": [
        "Low",
        "Current",
        "High"
    ],

    "Price": [
        low_price,
        price,
        high_price
    ]
})

fig = px.bar(
    chart_df,
    x="Type",
    y="Price",
    color="Type",
    template="plotly_dark",
    title=f"{selected_symbol} Price Levels"
)

fig.update_layout(
    height=500,
    paper_bgcolor="#050816",
    plot_bgcolor="#050816"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader("🤖 AI Market Insights")

if change > 8:

    st.error(
        "Possible pump activity detected."
    )

elif change < -8:

    st.warning(
        "Possible panic sell-off detected."
    )

else:

    st.success(
        "Market conditions appear stable."
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)