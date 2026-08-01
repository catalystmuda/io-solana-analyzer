from logger import log


class PumpFunListener:

    def __init__(self):
        log("[Listener] PumpFun Listener Ready")

    def listen(self):
        log("[Listener] Waiting for new Pump.fun tokens...")