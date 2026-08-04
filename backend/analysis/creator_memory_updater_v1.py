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
            SELECT market_cap_sol
            FROM tokens
            WHERE creator=?
        """, (creator,)).fetchall()

        mc = [r[0] for r in rows if r[0] is not None]

        if len(mc) == 0:
            continue

        total_tokens = len(mc)

        highest_mc = max(mc)

        average_mc = sum(mc) / total_tokens

        breakout = len([x for x in mc if x >= 100])

        survivor = len([x for x in mc if x >= 50])

        # -------------------------
        # NEW REPUTATION FORMULA
        # -------------------------

        success_rate = breakout / total_tokens

        reputation = (
            success_rate * 70
            + breakout * 15
            + survivor * 5
        )

        reputation = min(100, round(reputation, 2))

        risk = round(100 - reputation, 2)

        if reputation >= 80:
            category = "ELITE"
        elif reputation >= 60:
            category = "GOOD"
        elif reputation >= 40:
            category = "NORMAL"
        else:
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