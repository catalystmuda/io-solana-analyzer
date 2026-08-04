import sqlite3

conn = sqlite3.connect("backend/database/tokens.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT *
FROM paper_trades
ORDER BY roi_percent DESC
""").fetchall()

print("=" * 70)
print("PAPER TRADE REPORT")
print("=" * 70)

win = 0
lose = 0

for row in rows:

    roi = row["roi_percent"]

    if roi > 0:
        win += 1
    else:
        lose += 1

    print()
    print("NAME      :", row["name"])
    print("SYMBOL    :", row["symbol"])
    print("ENTRY MC  :", round(row["market_cap"], 2))
    print("NOW MC    :", round(row["current_market_cap"], 2))
    print("HIGH MC   :", round(row["highest_market_cap"], 2))
    print("ROI       :", round(roi, 2), "%")
    print("ALPHA     :", round(row["alpha_score"], 2))
    print("STATUS    :", row["status"])

print()
print("=" * 70)
print("TOTAL     :", len(rows))
print("WIN       :", win)
print("LOSE      :", lose)

if len(rows) > 0:
    print("WIN RATE  :", round(win / len(rows) * 100, 2), "%")

conn.close()