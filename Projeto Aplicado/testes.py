import yfinance as yf
import time
from datetime import datetime

# Tickers que vamos acompanhar
TICKERS = {
    "VIX": "^VIX",
    "BOVESPA": "^BVSP",
    "NASDAQ": "^IXIC",
    "DOLAR": "BRL=X"
}

def fetch_prices():
    prices = {}
    for name, ticker in TICKERS.items():
        try:
            price = yf.Ticker(ticker).fast_info.last_price
            prices[name] = price
        except Exception as e:
            prices[name] = None
            print(f"Erro ao buscar {name}: {e}")
    return prices

if __name__ == "__main__":
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        prices = fetch_prices()

        print("\n==============================")
        print(f"⏱️ Atualização: {now}")
        print("==============================")

        for name, price in prices.items():
            if price is not None:
                print(f"{name}: {price:.3f}")
            else:
                print(f"{name}: ERRO ao obter preço")

        # Espera 10 segundos
        time.sleep(10)
