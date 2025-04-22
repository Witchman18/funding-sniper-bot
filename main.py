import os
import time
from datetime import datetime, timezone
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

load_dotenv()

session = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

min_rate = 0.00005 

def get_top_funding_pairs():
    try:
        response = session.get_tickers(category="linear")
        tickers = response["result"]["list"]

        relevant = []

        for t in tickers:
            symbol = t["symbol"]
            raw_rate = t.get("fundingRate")

            try:
                rate = float(raw_rate)
                if abs(rate) >= min_rate:
                    relevant.append((symbol, rate))
            except (TypeError, ValueError):
                continue

        relevant.sort(key=lambda x: abs(x[1]), reverse=True)

        print(f"\n📊 [{datetime.now(timezone.utc)}] Топ {min(5, len(relevant))} пар по funding rate ≥ {min_rate}:\n")
        for i, (s, r) in enumerate(relevant[:5], 1):
            print(f"{i}. {s} — Funding Rate: {r * 100:.6f}%")
        print("✅ Готово.\n")

    except Exception as e:
        print(f"[!] Ошибка при получении тикеров: {e}")

if __name__ == "__main__":
    while True:
        print(f"\n🔁 [{datetime.now(timezone.utc)}] Проверка всех пар с funding...\n")
        get_top_funding_pairs()
        time.sleep(30)
