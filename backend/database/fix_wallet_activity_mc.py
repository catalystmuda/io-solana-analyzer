import sqlite3


DB = "backend/database/tokens.db"


print("==============================")
print(" FIX WALLET ACTIVITY MC ")
print("==============================")


conn = sqlite3.connect(DB)
cur = conn.cursor()


cur.execute("""
UPDATE wallet_activity
SET exit_mc = (
    SELECT MAX(market_cap_sol)
    FROM tokens
    WHERE tokens.mint = wallet_activity.token_mint
)
""")


conn.commit()


cur.execute("""
SELECT COUNT(*)
FROM wallet_activity
WHERE exit_mc IS NOT NULL
""")


print("UPDATED :", cur.fetchone()[0])


conn.close()