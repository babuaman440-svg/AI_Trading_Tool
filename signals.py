def generate_signal(data):

    last = data.iloc[-1]

    signal = "HOLD"

    if (
        last["EMA20"] > last["EMA50"]
        and last["EMA50"] > last["EMA200"]
        and last["MACD"] > last["MACD_SIGNAL"]
        and last["RSI"] > 55
        and last["Close"] > last["VWAP"]
    ):
        signal = "BUY"

    elif (
        last["EMA20"] < last["EMA50"]
        and last["EMA50"] < last["EMA200"]
        and last["MACD"] < last["MACD_SIGNAL"]
        and last["RSI"] < 45
        and last["Close"] < last["VWAP"]
    ):
        signal = "SELL"

    return signal