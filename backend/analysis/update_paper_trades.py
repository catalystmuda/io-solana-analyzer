import sqlite3
import requests
from datetime import datetime, UTC

DB = "backend/database/tokens.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# Tambahkan kolom jika belum ada
columns = [r[1] for r in conn.execute("PRAGMA table_info(paper_trades)")]

if "current_market_cap" not in columns:
    conn.execute("ALTER TABLE paper_trades ADD COLUMN current_market_cap REAL DEFAULT 0")

if "highest_market_cap" not in columns:
    conn.execute("ALTER TABLE paper_trades ADD COLUMN highest_market_cap REAL DEFAULT 0")

if "roi_percent" not in columns:
    conn.execute("ALTER TABLE paper_trades ADD COLUMN roi_percent REAL DEFAULT 0")

if "last_update" not in columns:
    conn.execute("ALTER TABLE paper_trades ADD COLUMN last_update TEXT")

conn.commit()

rows = conn.execute("""
SELECT *
FROM paper_trades
WHERE status='OPEN'
""").fetchall()

print("=" * 70)
print("UPDATE PAPER TRADES")
print("=" * 70)

for row in rows:

    mint = row["mint"]

    try:

        url = f"https://frontend-api-v3.pump.fun/coins/{mint}"

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            print("SKIP :", row["symbol"])
            continue

        data = r.json()

        current_mc = float(data.get("usd_market_cap", 0))

        if current_mc <= 0:
            print("NO MC :", row["symbol"])
            continue

        old_mc = row["market_cap"]

        roi = ((current_mc - old_mc) / old_mc) * 100

        highest = max(
            current_mc,
            row["highest_market_cap"] or 0
        )

        conn.execute("""
        UPDATE paper_trades
        SET
            current_market_cap=?,
            highest_market_cap=?,
            roi_percent=?,
            last_update=?
        WHERE id=?
        """, (
            current_mc,
            highest,
            roi,
            datetime.now(UTC).isoformat(),
            row["id"]
        ))

        print()
        print("TOKEN :", row["symbol"])
        print("ENTRY :", round(old_mc,2))
        print("NOW   :", round(current_mc,2))
        print("ROI   :", round(roi,2), "%")

    except Exception as e:
        print("ERROR :", row["symbol"], e)

conn.commit()
conn.close()

print()
print("=" * 70)
print("DONE")
print("=" * 70)