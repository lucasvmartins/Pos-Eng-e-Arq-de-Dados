import yfinance as yf
import psycopg2
import time
from datetime import datetime

# =========================
# Configuração do banco
# =========================
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

# =========================
# Ativos financeiros
# =========================
TICKERS = {
    "IBOVESPA": "^BVSP",
    "SP500": "^GSPC",
    "DOWJONES": "^DJI",
    "USD_BRL": "BRL=X",
    "EUR_BRL": "EURBRL=X",
    "GBP_BRL": "GBPBRL=X",
    "JPY_BRL": "JPYBRL=X",
    "BITCOIN": "BTC-USD",
    "ETHEREUM": "ETH-USD",
    "VIX": "^VIX",
    "VIX_BR": "^VXEWZ"
}

# =========================
# Conexão Postgres
# =========================
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# =========================
# Função de coleta
# =========================
def get_data():
    snapshot = {}
    now = datetime.now()
    snapshot["data_hora"] = now

    for ativo, ticker in TICKERS.items():
        hist = yf.Ticker(ticker).history(period="1d", interval="1m")

        snapshot[ativo] = (
            float(hist.iloc[-1]["Close"])
            if not hist.empty
            else None
        )

    return snapshot

# =========================
# Loop principal (5s)
# =========================
while True:
    try:
        data = get_data()

        cursor.execute(
            """
            INSERT INTO financial (
                data_hora, IBOVESPA, SP500, DOWJONES,
                USD_BRL, EUR_BRL, GBP_BRL, JPY_BRL,
                BITCOIN, ETHEREUM, VIX, VIX_BR
            )
            VALUES (
                %(data_hora)s, %(IBOVESPA)s, %(SP500)s, %(DOWJONES)s,
                %(USD_BRL)s, %(EUR_BRL)s, %(GBP_BRL)s, %(JPY_BRL)s,
                %(BITCOIN)s, %(ETHEREUM)s, %(VIX)s, %(VIX_BR)s
            )
            """,
            data
        )

        conn.commit()
        print(f"Snapshot inserido em {data['data_hora']}")

        time.sleep(5)

    except Exception as e:
        conn.rollback()
        print("Erro:", e)
        time.sleep(5)
