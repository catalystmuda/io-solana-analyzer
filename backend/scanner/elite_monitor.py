import sqlite3
import time
import os

DB = "backend/database/tokens.db"

LAST_ID = 0


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def save_signal(row):

    conn = sqlite3.connect(DB)

    conn.execute("""
    INSERT OR IGNORE INTO elite_signals
    (
        mint,
        name,
        symbol,
        creator,
        alpha_score,
        market_cap_sol,
        liquidity,
        volume24,
        fdv,
        category,
        reputation_score,
        breakout_count,
        survivor_count
    )
    VALUES
    (
        ?,?,?,?,?,?,?,?,?,?,?,?,?
    )
    """,
    (
        row["mint"],
        row["name"],
        row["symbol"],
        row["creator"],
        row["alpha_score"],
        row["market_cap_sol"],
        row["liquidity"],
        row["volume24"],
        row["fdv"],
        row["category"],
        row["reputation_score"],
        row["breakout_count"],
        row["survivor_count"]
    ))

    conn.commit()
    conn.close()


def load_elite():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
    SELECT

        t.id,
        t.mint,
        t.name,
        t.symbol,
        t.creator,
        t.market_cap_sol,
        t.liquidity,
        t.volume24,
        t.fdv,
        t.alpha_score,

        c.category,
        c.reputation_score,
        c.breakout_count,
        c.survivor_count

    FROM tokens t

    LEFT JOIN creator_memory c
    ON t.creator=c.creator

    WHERE t.alpha_score>=600

    ORDER BY t.id ASC
    """).fetchall()

    conn.close()

    return rows


def print_signal(row):

    print()
    print("=" * 70)
    print("🔥 ELITE SIGNAL")
    print("=" * 70)

    print("NAME      :", row["name"])
    print("SYMBOL    :", row["symbol"])
    print("CA        :", row["mint"])
    print()

    print("ALPHA     :", row["alpha_score"])
    print("MC SOL    :", row["market_cap_sol"])
    print("LIQUIDITY :", row["liquidity"])
    print("VOLUME24  :", row["volume24"])
    print("FDV       :", row["fdv"])
    print()

    print("CATEGORY  :", row["category"])
    print("REPUTATION:", row["reputation_score"])
    print("BREAKOUT  :", row["breakout_count"])
    print("SURVIVOR  :", row["survivor_count"])

    print("=" * 70)


def main():

    global LAST_ID

    clear()

    print("=" * 70)
    print("IO ELITE MONITOR")
    print("=" * 70)

    while True:

        try:

            rows = load_elite()

            for row in rows:

                if row["id"] <= LAST_ID:
                    continue

                LAST_ID = row["id"]

                save_signal(row)

                print_signal(row)

            time.sleep(2)

        except KeyboardInterrupt:
            break

        except Exception as e:

            print(e)
            time.sleep(2)


if __name__ == "__main__":
    main()