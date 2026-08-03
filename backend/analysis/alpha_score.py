import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT *
FROM tokens
ORDER BY market_cap_sol DESC
""").fetchall()

print("=" * 70)
print("IO SOLANA ANALYZER v1.0")
print("=" * 70)

shown_creator = set()
shown_token = set()

for row in rows:

    creator = row["creator"]

    if creator in shown_creator:
        continue

    name = (row["name"] or "").strip().lower()
    symbol = (row["symbol"] or "").strip().lower()

    token_key = (name, symbol)

    if token_key in shown_token:
        continue

    shown_creator.add(creator)
    shown_token.add(token_key)

    memory = conn.execute("""
    SELECT *
    FROM creator_memory
    WHERE creator=?
    """, (creator,)).fetchone()

    if memory is None:
        continue

    total = memory["total_tokens"]

    if total > 10:
        continue

    rep = memory["reputation_score"]
    risk = memory["risk_score"]
    breakout = memory["breakout_count"]
    survivor = memory["survivor_count"]
    highest = memory["highest_mc"]
    avg = memory["average_mc"]

    score = (
        rep
        + breakout * 30
        + survivor * 10
        + highest * 0.05
        + avg * 0.10
        + row["market_cap_sol"] * 0.30
        + row["sol_amount"] * 0.20
        - risk * 0.20
    )

    if score < 120:
        continue

    print()
    print("NAME   :", row["name"])
    print("SYMBOL :", row["symbol"])
    print("MC     :", round(row["market_cap_sol"], 2))
    print("BUY    :", round(row["sol_amount"], 2))
    print("REP    :", rep)
    print("FINAL  :", round(score, 2))

conn.close()