class TokenParser:

    def parse(self, token):

        return {

            "signature": token.get("signature"),

            "mint": token.get("mint"),

            "name": token.get("name"),

            "symbol": token.get("symbol"),

            "creator": token.get("traderPublicKey"),

            "tx_type": token.get("txType"),

            "initial_buy": token.get("initialBuy"),

            "sol_amount": token.get("solAmount"),

            "market_cap_sol": token.get("marketCapSol"),

            "bonding_curve": token.get("bondingCurveKey"),

            "uri": token.get("uri"),

            "pool": token.get("pool")
        }