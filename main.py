import os
import time
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

load_dotenv()

session = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

def get_top_funding_pairs(min_rate=0.00005, top_n=5):
    try:
        response = session.get_tickers(category="linear")
        symbols = response["result"]["list"]

        top = []
        for s in symbols:
            symbol = s["symbol"]
            raw_rate = s.get("fundingRate")
            try:
                rate = float(raw_rate)
                if abs(rate) >= min_rate:
                    top.append((symbol, rate))
            except (TypeError, ValueError):
                # fundingRate = None или '' — пропускаем
                continue

        top.sort(key=lambda x: abs(x[1]), reverse=True)

        print(f"\n📊 Топ {top_n} активных пар по funding rate:\n")
        for i, (symbol, rate) in enumerate(top[:top_n], 1):
            print(f"{i}. {symbol} — Funding Rate: {rate:.8f}")
        print("✅ Готово.\n")
    except Exception as e:
        print(f"Ошибка при получении тикеров: {e}")

if __name__ == "__main__":
    while True:
        print("🔁 Получаю лучшие пары по funding...\n")
        get_top_funding_pairs()
        time.sleep(30)
