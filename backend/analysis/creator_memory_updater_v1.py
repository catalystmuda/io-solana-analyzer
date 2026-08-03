import sqlite3

DB = "backend/database/tokens.db"


def main():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    creators = cur.execute("""
        SELECT DISTINCT creator
        FROM tokens
    """).fetchall()

    total = 0

    for (creator,) in creators:

        rows = cur.execute("""
            SELECT
                market_cap_sol
            FROM tokens
            WHERE creator=?
        """, (creator,)).fetchall()

        if not rows:
            continue

        mc = [x[0] for x in rows if x[0] is not None]

        if not mc:
            continue

        total_tokens = len(mc)
        highest_mc = max(mc)
        average_mc = sum(mc) / len(mc)

        breakout = len([x for x in mc if x >= 100])
        survivor = len([x for x in mc if x >= 50])

        reputation = min(
            100,
            breakout * 20 + survivor * 5
        )

        risk = max(
            0,
            100 - reputation
        )

        category = "NORMAL"

        if reputation >= 80:
            category = "ELITE"

        elif reputation >= 60:
            category = "GOOD"

        elif reputation < 30:
            category = "RISK"

        cur.execute("""
        INSERT OR REPLACE INTO creator_memory(
            creator,
            total_tokens,
            highest_mc,
            average_mc,
            breakout_count,
            survivor_count,
            reputation_score,
            risk_score,
            category,
            signals
        )
        VALUES(
            ?,?,?,?,?,?,?,?,?,?
        )
        """, (
            creator,
            total_tokens,
            highest_mc,
            average_mc,
            breakout,
            survivor,
            reputation,
            risk,
            category,
            ""
        ))

        total += 1

    conn.commit()
    conn.close()

    print("========================")
    print("CREATOR MEMORY UPDATED")
    print("========================")
    print("Total Creator :", total)


if __name__ == "__main__":
    main()