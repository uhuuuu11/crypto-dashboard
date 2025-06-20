import streamlit as st
from tradingview_ta import TA_Handler, Interval, Exchange
import requests
import time

# ---------------------------------------------
# SETTINGS
# ---------------------------------------------
st.set_page_config(page_title="Live Crypto Dashboard", layout="wide")
st.title("📈 Live Crypto Dashboard")

# ---------------------------------------------
# LIVE PRICE FETCHING
# ---------------------------------------------
def get_price(symbol):
    handler = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_1_MINUTE
    )
    analysis = handler.get_analysis()
    price = analysis.indicators["close"]
    return round(price, 2)

btc_price = get_price("BTCUSDT")
eth_price = get_price("ETHUSDT")

col1, col2 = st.columns(2)
col1.metric("💰 BTC/USDT", f"${btc_price}")
col2.metric("💰 ETH/USDT", f"${eth_price}")

# ---------------------------------------------
# LIVE CHART VIEW (TradingView Widget)
# ---------------------------------------------
st.markdown("## 📊 TradingView Chart - BTC/USDT")
st.components.v1.iframe("https://www.tradingview.com/widgetembed/?frameElementId=tradingview_9ca65&symbol=BINANCE:BTCUSDT&interval=5&theme=dark&style=1&locale=en", height=500)

# ---------------------------------------------
# WHALE ALERT FEED (via Twitter)
# ---------------------------------------------
st.markdown("## 🐋 Whale Alert Feed")
whale_tweets = requests.get("https://nitter.net/whale_alert/rss").text
if "Transfer" in whale_tweets:
    st.success("Latest Whale Activity: Check Nitter or Twitter for details.")
    st.markdown("[View Whale Alerts (Twitter)](https://twitter.com/whale_alert)")
else:
    st.warning("Unable to fetch latest whale alerts.")

# ---------------------------------------------
# NEWS HEADLINES (via CryptoPanic)
# ---------------------------------------------
st.markdown("## 📰 Latest Crypto News")
news_api = "https://cryptopanic.com/api/v1/posts/?auth_token=demo&public=true"
response = requests.get(news_api).json()
if "results" in response:
    for post in response["results"][:5]:
        st.markdown(f"🔗 [{post['title']}]({post['url']})")

# ---------------------------------------------
# REFRESH
# ---------------------------------------------
st.markdown("⏱️ Data refreshes every 60 seconds.")
st_autorefresh = st.experimental_rerun
time.sleep(60)
st_autorefresh()
