import sqlite3

DB = "backend/database/tokens.db"


def calculate_score(mint):

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
    ON t.creator = c.creator
    WHERE t.mint = ?
    """, (mint,)).fetchone()

    conn.close()

    if row is None:
        return None

    volume24 = row["volume24"] or 0
    fdv = row["fdv"] or 0
    mc = row["market_cap_sol"] or 0

    reputation = row["reputation_score"] or 0
    breakout = row["breakout_count"] or 0
    survivor = row["survivor_count"] or 0
    category = row["category"] or "RISK"

    # =====================================================
    # DATA BELUM MATANG
    # =====================================================

    if volume24 < 100:
        return None

    if fdv <= 0:
        return None

    score = 0

    # =====================================================
    # MARKET
    # =====================================================

    if volume24 >= 10000:
        score += 400

    elif volume24 >= 5000:
        score += 250

    elif volume24 >= 2000:
        score += 160

    elif volume24 >= 1000:
        score += 80

    if 20 <= mc <= 60:
        score += 120

    elif 60 < mc <= 120:
        score += 60

    if fdv >= 5000:
        score += 140

    elif fdv >= 3000:
        score += 80

    elif fdv >= 2000:
        score += 40

    # =====================================================
    # CREATOR MEMORY
    # =====================================================

    score += reputation * 5
    score += breakout * 80
    score += survivor * 50

    if category == "ELITE":
        score += 250

    elif category == "GOOD":
        score += 120

    elif category == "NORMAL":
        score += 40

    return round(score, 2)


if __name__ == "__main__":

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
    SELECT mint
    FROM tokens
    ORDER BY created_at DESC
    LIMIT 20
    """).fetchall()

    conn.close()

    print("=" * 70)
    print("ALPHA SCORE TEST")
    print("=" * 70)

    for row in rows:

        score = calculate_score(row["mint"])

        if score is None:
            continue

        print(row["mint"], score)