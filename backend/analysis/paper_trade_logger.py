import sqlite3
from datetime import datetime, UTC

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

conn.execute("""
CREATE TABLE IF NOT EXISTS paper_trades(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    mint TEXT,
    name TEXT,
    symbol TEXT,
    creator TEXT,
    market_cap REAL,
    buy_sol REAL,
    alpha_score REAL,
    status TEXT DEFAULT 'OPEN'
)
""")

rows = conn.execute("""
SELECT *
FROM tokens
ORDER BY market_cap_sol DESC
LIMIT 5
""").fetchall()

saved = 0
skipped = 0

for row in rows:

    creator = row["creator"]

    memory = conn.execute("""
    SELECT *
    FROM creator_memory
    WHERE creator=?
    """, (creator,)).fetchone()

    if memory is None:
        continue

    total = memory["total_tokens"]

    # spam creator
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

    existing = conn.execute("""
    SELECT id
    FROM paper_trades
    WHERE mint=?
      AND status='OPEN'
    """, (row["mint"],)).fetchone()

    if existing:
        skipped += 1
        continue

    conn.execute("""
    INSERT INTO paper_trades(
        created_at,
        mint,
        name,
        symbol,
        creator,
        market_cap,
        buy_sol,
        alpha_score,
        status
    )
    VALUES(?,?,?,?,?,?,?,?,?)
    """, (
        datetime.now(UTC).isoformat(),
        row["mint"],
        row["name"],
        row["symbol"],
        creator,
        row["market_cap_sol"],
        row["sol_amount"],
        score,
        "OPEN"
    ))

    saved += 1

conn.commit()

print("=" * 70)
print("PAPER TRADE LOGGER")
print("=" * 70)
print("NEW SAVED :", saved)
print("SKIPPED   :", skipped)
print("=" * 70)

conn.close()