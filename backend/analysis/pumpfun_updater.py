import requests

PUMPFUN_API = "https://frontend-api.pump.fun/coins/"


def update_pumpfun(mint: str):

    try:

        url = PUMPFUN_API + mint

        r = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if r.status_code != 200:
            return None

        data = r.json()

        return {
            "mint": mint,
            "name": data.get("name"),
            "symbol": data.get("symbol"),
            "creator": data.get("creator"),
            "market_cap_usd": data.get("usd_market_cap", 0),
            "virtual_sol_reserves": data.get("virtual_sol_reserves", 0),
            "virtual_token_reserves": data.get("virtual_token_reserves", 0),
            "reply_count": data.get("reply_count", 0),
            "creator_fee_basis_points": data.get("creator_fee_basis_points", 0),
            "complete": data.get("complete", False),
            "nsfw": data.get("nsfw", False),
            "created_timestamp": data.get("created_timestamp", 0),
        }

    except Exception as e:

        print("PUMPFUN ERROR :", e)
        return None


if __name__ == "__main__":

    mint = input("Mint : ").strip()

    info = update_pumpfun(mint)

    print("=" * 70)

    if info is None:
        print("TOKEN NOT FOUND")
    else:
        for k, v in info.items():
            print(f"{k:25}: {v}")

    print("=" * 70)