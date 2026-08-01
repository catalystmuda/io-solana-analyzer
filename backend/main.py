from connectors.solana import SolanaConnector
from listeners.pumpfun_listener import PumpFunListener
from database.history import HistoryDatabase
from logger import log


def start():

    log("Collector Starting...")

    # Solana Connector
    solana = SolanaConnector()
    slot = solana.get_latest_slot()

    log(f"Current Solana Slot : {slot}")

    # History Database
    history = HistoryDatabase()

    total_tokens = history.total_tokens()
    total_creators = history.total_creators()
    total_mints = history.total_mints()
    duplicate_records = history.duplicate_tokens()

    print("\n========================================")
    print("DATA QUALITY")
    print("========================================")
    print(f"Total Tokens      : {total_tokens}")
    print(f"Unique Creators   : {total_creators}")
    print(f"Unique Mints      : {total_mints}")
    print(f"Duplicate Records : {duplicate_records}")
    print("========================================")

    print("\n========== Latest Tokens ==========\n")

    latest = history.latest_tokens()

    for token in latest:
        print(token)

    print("\n===================================\n")

    history.close()

    # Pump.fun Listener
    listener = PumpFunListener()
    listener.start()


if __name__ == "__main__":
    start()