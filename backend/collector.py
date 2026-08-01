from connectors.pumpfun import PumpFunConnector
from connectors.solana import SolanaConnector
from logger import log


def start():
    log("Collector Starting...")

    connector = PumpFunConnector()
    tokens = connector.get_new_tokens()

    log(f"Found {len(tokens)} token(s)")

    solana = SolanaConnector()
    slot = solana.get_latest_slot()

    log(f"Current Solana Slot : {slot}")