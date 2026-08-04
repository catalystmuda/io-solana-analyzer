import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT
    name,
    symbol,
    pair_address,
    dex,
    chain,
    liquidity,
    volume24,
    fdv,
    price_usd
FROM tokens
WHERE pair_address IS NOT NULL
ORDER BY liquidity DESC
LIMIT 20
""").fetchall()

print("=" * 80)
print("DEX DATA")
print("=" * 80)

for r in rows:
    print()
    print("NAME      :", r["name"])
    print("SYMBOL    :", r["symbol"])
    print("DEX       :", r["dex"])
    print("CHAIN     :", r["chain"])
    print("PRICE USD :", r["price_usd"])
    print("LIQUIDITY :", r["liquidity"])
    print("VOLUME24  :", r["volume24"])
    print("FDV       :", r["fdv"])

conn.close()