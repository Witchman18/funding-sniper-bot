import os
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

load_dotenv()

session = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

def get_funding_rate(symbol="BTCUSDT"):
    result = session.get_funding_rate_history(
        category="linear",
        symbol=symbol,
        limit=1
    )
    rate = result['result']['list'][0]['fundingRate']
    print(f"Funding rate for {symbol}: {rate}")

if __name__ == "__main__":
    get_funding_rate()