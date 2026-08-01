from connectors.pumpfun import PumpFunConnector
from connectors.solana import SolanaConnector
from listeners.pumpfun_listener import PumpFunListener
from logger import log


def start():
    log("Collector Starting...")

    # Pump.fun Connector
    connector = PumpFunConnector()
    tokens = connector.get_new_tokens()

    log(f"Found {len(tokens)} token(s)")

    # Solana Connector
    solana = SolanaConnector()
    slot = solana.get_latest_slot()

    log(f"Current Solana Slot : {slot}")

    # Pump.fun Listener
    listener = PumpFunListener()
    listener.listen()