import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" WALLET ACTIVITY CHECK ")
print("==============================")


conn = sqlite3.connect(DB)
cur = conn.cursor()


cur.execute("""
SELECT COUNT(*)
FROM wallet_activity
""")


total = cur.fetchone()[0]


print()
print("TOTAL ACTIVITY :", total)



cur.execute("""
SELECT
wallet,
token_symbol,
token_name,
entry_mc,
roi,
result
FROM wallet_activity
LIMIT 10
""")


rows = cur.fetchall()


print()
print("SAMPLE DATA")
print("----------------")


for r in rows:
    print(
        "Wallet:",
        r[0][:12],
        "| Token:",
        r[1],
        "| MC:",
        r[3],
        "| ROI:",
        r[4],
        "| Result:",
        r[5]
    )


conn.close()