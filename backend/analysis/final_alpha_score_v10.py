import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT *
FROM tokens
ORDER BY market_cap_sol DESC
""").fetchall()

print("=" * 70)
print("FINAL ALPHA SCORE V10")
print("=" * 70)

shown_creator = set()

for row in rows:

    creator = row["creator"]

    if creator in shown_creator:
        continue

    shown_creator.add(creator)

    memory = conn.execute("""
    SELECT
        reputation_score,
        risk_score
    FROM creator_memory
    WHERE creator=?
    """, (creator,)).fetchone()

    if memory is None:
        continue

    score = (
        row["market_cap_sol"] * 0.5 +
        row["sol_amount"] * 0.8 +
        memory["reputation_score"] -
        memory["risk_score"] * 0.1
    )

    if score < 100:
        continue

    print()
    print("NAME    :", row["name"])
    print("SYMBOL  :", row["symbol"])
    print("CREATOR :", creator)
    print("MC      :", round(row["market_cap_sol"], 2))
    print("BUY     :", round(row["sol_amount"], 2))
    print("REP     :", memory["reputation_score"])
    print("RISK    :", memory["risk_score"])
    print("FINAL   :", round(score, 2))

conn.close()