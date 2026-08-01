import requests


class PumpFunConnector:

    def __init__(self):
        print("[PumpFun] Connector Ready")

    def get_new_tokens(self):
        print("[PumpFun] Getting new tokens...")

        # Sementara kita kembalikan list kosong
        # Nanti akan diganti dengan data asli Pump.fun
        return []