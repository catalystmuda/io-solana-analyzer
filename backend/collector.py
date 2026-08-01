from connectors.solana import SolanaConnector
from listeners.pumpfun_listener import PumpFunListener
from logger import log


def start():

    log("Collector Starting...")

    # Solana Connection
    solana = SolanaConnector()

    slot = solana.get_latest_slot()

    log(f"Current Solana Slot : {slot}")

    # Pump.fun Listener
    listener = PumpFunListener()

    listener.start()