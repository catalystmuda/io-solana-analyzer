import httpx


class SolanaConnector:
    def __init__(self):
        self.rpc = "https://api.mainnet-beta.solana.com"
        print("[Solana] Connected")

    def get_latest_slot(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSlot"
        }

        response = httpx.post(self.rpc, json=payload, timeout=10)

        data = response.json()

        return data["result"]