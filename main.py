import os
import time
from datetime import datetime
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

load_dotenv()

session = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

# 👇 Добавляй сюда любые пары
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]

def get_funding_rate(symbol):
    try:
        result = session.get_funding_rate_history(
            category="linear",
            symbol=symbol,
            limit=1
        )
        rate = float(result['result']['list'][0]['fundingRate'])
        print(f"[{datetime.utcnow()}] {symbol} — Funding Rate: {rate}")
    except Exception as e:
        print(f"[{datetime.utcnow()}] Ошибка по {symbol}: {e}")

if __name__ == "__main__":
    while True:
        print(f"\n🔁 [{datetime.utcnow()}] Проверка ручных монет...\n")
        for symbol in symbols:
            get_funding_rate(symbol)
        print("✅ Готово. Ждём 30 секунд...\n")
        time.sleep(30)
