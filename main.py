import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from indicators import add_indicators
from signals import generate_signal

st.set_page_config(
    page_title="AI Trading Tool V4",
    layout="wide"
)

st.title("🤖 AI Intraday Trading Tool V4")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header("Market Settings")

symbol = st.sidebar.text_input(
    "Stock Symbol",
    "RELIANCE.NS"
)

interval = st.sidebar.selectbox(
    "Interval",
    [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m"
    ],
    index=2
)

period = st.sidebar.selectbox(
    "Period",
    [
        "1d",
        "5d",
        "1mo"
    ],
    index=0
)

refresh = st.sidebar.button("Load Data")

# ==========================
# LOAD DATA
# ==========================

if refresh:

    with st.spinner("Downloading Market Data..."):

        data = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False
        )

    if data.empty:

        st.error("No Market Data Found")

        st.stop()

    data = add_indicators(data)

    signal = generate_signal(data)

    last = data.iloc[-1]

    close_price = float(last["Close"])

    atr = 0

    if "ATR" in data.columns:

        atr = float(last["ATR"])

    entry = round(close_price,2)

    stoploss = round(close_price-atr,2)

    target1 = round(close_price+(atr*2),2)

    target2 = round(close_price+(atr*3),2)

    risk = round(entry-stoploss,2)

    reward = round(target1-entry,2)

    rr = 0

    if risk != 0:

        rr = round(reward/risk,2)

    trend="Sideways"

    if (
        last["EMA20"]>
        last["EMA50"]>
        last["EMA200"]
    ):
        trend="Bullish"

    elif(
        last["EMA20"]<
        last["EMA50"]<
        last["EMA200"]
    ):
        trend="Bearish"

    st.success("Market Data Loaded Successfully")

    col1,col2,col3,col4=st.columns(4)

    with col1:

        st.metric(
            "Trend",
            trend
        )

    with col2:

        st.metric(
            "Signal",
            signal
        )

    with col3:

        st.metric(
            "Close",
            round(close_price,2)
        )

    with col4:

        st.metric(
            "Risk Reward",
            rr
        )

    st.divider()

    col1,col2,col3,col4=st.columns(4)

    with col1:

        st.metric(
            "Entry",
            entry
        )

    with col2:

        st.metric(
            "Stop Loss",
            stoploss
        )

    with col3:

        st.metric(
            "Target 1",
            target1
        )

    with col4:

        st.metric(
            "Target 2",
            target2
        )