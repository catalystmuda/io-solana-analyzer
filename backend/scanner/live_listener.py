import asyncio
import json
import websockets

from backend.scanner.live_pipeline import process_token

WS_URL = "wss://pumpportal.fun/api/data"


async def run_process(payload):
    try:
        await asyncio.to_thread(process_token, payload)
    except Exception as e:
        print("PROCESS ERROR :", e)


async def listen():

    while True:

        try:

            async with websockets.connect(
                WS_URL,
                ping_interval=20,
                ping_timeout=20,
                max_size=None
            ) as ws:

                print("=" * 70)
                print("CONNECTED TO PUMPFUN")
                print("=" * 70)

                await ws.send(json.dumps({
                    "method": "subscribeNewToken"
                }))

                async for message in ws:

                    try:

                        data = json.loads(message)

                        mint = (
                            data.get("mint")
                            or data.get("tokenAddress")
                            or data.get("address")
                        )

                        if not mint:
                            continue

                        print()
                        print("=" * 70)
                        print("NEW TOKEN :", mint)
                        print("=" * 70)

                        # kirim seluruh payload ke pipeline
                        asyncio.create_task(run_process(data))

                    except Exception as e:

                        print("PARSE ERROR :", e)

        except Exception as e:

            print()
            print("DISCONNECTED :", e)
            print("RECONNECTING...")

            await asyncio.sleep(5)


if __name__ == "__main__":

    asyncio.run(listen())