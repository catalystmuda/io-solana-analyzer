import requests


class PriceConnector:

    def __init__(self):
        print("[Price] Connector Ready")

    def get_sol_price(self):

        try:

            url = "https://api.binance.com/api/v3/ticker/price"

            params = {
                "symbol": "SOLUSDT"
            }

            response = requests.get(url, params=params, timeout=10)

            response.raise_for_status()

            data = response.json()

            price = float(data["price"])

            print(f"[Price] SOL Price : ${price:.2f}")

            return price

        except Exception as e:

            print(f"[Price Error] {e}")

            return None