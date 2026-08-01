from connectors.pumpfun import PumpFunConnector
from logger import log


def start():
    log("Collector Starting...")

    connector = PumpFunConnector()

    tokens = connector.get_new_tokens()

    log(f"Found {len(tokens)} token(s)")