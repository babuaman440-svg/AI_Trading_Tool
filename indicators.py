import pandas as pd

def add_indicators(data):

    # ==========================
    # EMA
    # ==========================
    data["EMA20"] = data["Close"].ewm(span=20).mean()
    data["EMA50"] = data["Close"].ewm(span=50).mean()
    data["EMA200"] = data["Close"].ewm(span=200).mean()

    # ==========================
    # RSI
    # ==========================
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    data["RSI"] = 100 - (100 / (1 + rs))

    # ==========================
    # MACD
    # ==========================
    ema12 = data["Close"].ewm(span=12).mean()
    ema26 = data["Close"].ewm(span=26).mean()

    data["MACD"] = ema12 - ema26
    data["MACD_SIGNAL"] = data["MACD"].ewm(span=9).mean()
    data["MACD_HIST"] = data["MACD"] - data["MACD_SIGNAL"]

    # ==========================
    # VWAP
    # ==========================
    tp = (data["High"] + data["Low"] + data["Close"]) / 3

    data["VWAP"] = (
        (tp * data["Volume"]).cumsum()
        / data["Volume"].cumsum()
    )

    # ==========================
    # ATR (14)
    # ==========================
    high_low = data["High"] - data["Low"]

    high_close = (
        data["High"] - data["Close"].shift()
    ).abs()

    low_close = (
        data["Low"] - data["Close"].shift()
    ).abs()

    tr = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    data["ATR"] = tr.rolling(14).mean()

    return data