import sqlite3


creator = "bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa"


conn = sqlite3.connect(
    "backend/database/tokens.db"
)

cursor = conn.cursor()


print()
print("==============================")
print("PATTERN CHECK")
print("==============================")


cursor.execute(
    """
    SELECT
        COUNT(*),
        COUNT(DISTINCT name),
        COUNT(DISTINCT symbol),
        COUNT(DISTINCT market_cap_sol)
    FROM tokens
    WHERE creator = ?
    """,
    (creator,)
)


result = cursor.fetchone()


print("Total Token          :", result[0])
print("Unique Name          :", result[1])
print("Unique Symbol        :", result[2])
print("Unique MarketCap     :", result[3])


print()
print("TOP NAME DUPLICATE")
print("------------------------------")


cursor.execute(
    """
    SELECT
        name,
        COUNT(*) as jumlah
    FROM tokens
    WHERE creator = ?
    GROUP BY name
    ORDER BY jumlah DESC
    LIMIT 10
    """,
    (creator,)
)


for row in cursor.fetchall():
    print(row)


conn.close()