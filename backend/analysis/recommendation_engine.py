import sqlite3

DB = "backend/database/tokens.db"


def save_elite_signal(row, score):

    if score < 600:
        return

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
        score,
        row["market_cap_sol"],
        row["liquidity"],
        row["volume24"],
        row["fdv"],
        row["category"],
        row["reputation_score"],
        row["breakout_count"],
        row["survivor_count"],
    ))

    conn.commit()
    conn.close()


def check_token(mint, score=0):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    row = conn.execute("""
    SELECT
        t.*,
        c.reputation_score,
        c.breakout_count,
        c.survivor_count,
        c.category
    FROM tokens t
    LEFT JOIN creator_memory c
    ON t.creator=c.creator
    WHERE t.mint=?
    """, (mint,)).fetchone()

    conn.close()

    if row is None:
        return

    volume = row["volume24"] or 0
    liquidity = row["liquidity"] or 0
    fdv = row["fdv"] or 0

    reputation = row["reputation_score"] or 0
    breakout = row["breakout_count"] or 0
    survivor = row["survivor_count"] or 0
    category = row["category"] or "RISK"

    if score >= 600:

        level = "🔥 ELITE SIGNAL"

    elif score >= 350:

        level = "🔵 STRONG WATCH"

    elif score >= 180:

        level = "🟢 WATCH"

    else:
        return

    if score >= 600:
        save_elite_signal(row, score)

    reasons = []

    if volume >= 10000:
        reasons.append("Very High Volume")

    elif volume >= 5000:
        reasons.append("High Volume")

    elif volume >= 1000:
        reasons.append("Growing Volume")

    if liquidity >= 10000:
        reasons.append("Good Liquidity")

    if fdv >= 100000:
        reasons.append("Healthy FDV")

    if category == "ELITE":
        reasons.append("Elite Creator")

    elif category == "GOOD":
        reasons.append("Good Creator")

    if breakout > 0:
        reasons.append(f"{breakout} Breakout")

    if survivor > 0:
        reasons.append(f"{survivor} Survivors")

    if reputation > 0:
        reasons.append(f"Rep {reputation}")

    print()
    print("=" * 70)
    print(level)
    print("=" * 70)

    print("NAME      :", row["name"])
    print("SYMBOL    :", row["symbol"])
    print("CA        :", row["mint"])

    print()

    print("ALPHA     :", round(score, 2))
    print("MC SOL    :", round(row["market_cap_sol"] or 0, 2))
    print("LIQUIDITY :", round(liquidity, 2))
    print("VOLUME24  :", round(volume, 2))
    print("FDV       :", round(fdv, 2))

    print()

    print("CATEGORY  :", category)

    if reasons:

        print("WHY")

        for r in reasons:
            print("✔", r)

    print("=" * 70)


if __name__ == "__main__":

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
    SELECT mint
    FROM tokens
    ORDER BY created_at DESC
    LIMIT 200
    """).fetchall()

    conn.close()

    from backend.analysis.alpha_score_v11 import calculate_score

    for row in rows:

        score = calculate_score(row["mint"])

        if score is None:
            continue

        check_token(row["mint"], score)