import asyncio
import json
import websockets

from parsers.token_parser import TokenParser
from database.database import Database


class PumpFunListener:

    def __init__(self):
        print("[Listener] PumpFun Listener Ready")

        self.parser = TokenParser()
        self.database = Database()

    async def listen(self):

        uri = "wss://pumpportal.fun/api/data"

        async with websockets.connect(uri) as ws:

            # Subscribe token baru
            await ws.send(json.dumps({
                "method": "subscribeNewToken"
            }))

            print("[Listener] Connected to Pump.fun")
            print("[Listener] Waiting for new Pump.fun tokens...")

            async for message in ws:

                try:
                    token = json.loads(message)

                    # Abaikan pesan selain data token
                    if "mint" not in token:
                        continue

                    print("=" * 80)
                    print("[RAW TOKEN]")
                    print(json.dumps(token, indent=4))
                    print("=" * 80)

                    parsed = self.parser.parse(token)

                    self.database.save_token(parsed)

                except Exception as e:
                    print(f"[Listener Error] {e}")

    def start(self):
        asyncio.run(self.listen())