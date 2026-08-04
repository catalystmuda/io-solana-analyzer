import sqlite3
import time

from backend.analysis.dex_updater import update_token
from backend.analysis.alpha_score_v11 import calculate_score
from backend.analysis.recommendation_engine import check_token

DB = "backend/database/tokens.db"


def worker():

    print("=" * 70)
    print("RECHECK WORKER STARTED")
    print("=" * 70)

    while True:

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
        SELECT
            mint,
            pair_address,
            volume24,
            fdv
        FROM tokens
        ORDER BY id DESC
        LIMIT 100
        """).fetchall()

        conn.close()

        for row in rows:

            mint = row["mint"]

            update_token(mint)

            conn = sqlite3.connect(DB)
            conn.row_factory = sqlite3.Row

            token = conn.execute("""
            SELECT
                volume24,
                fdv
            FROM tokens
            WHERE mint=?
            """, (mint,)).fetchone()

            conn.close()

            volume = token["volume24"] or 0
            fdv = token["fdv"] or 0

            print()
            print("=" * 70)
            print("TRACKING :", mint)
            print("VOLUME24 :", round(volume, 2))
            print("FDV      :", round(fdv, 2))
            print("=" * 70)

            # ============================
            # Token mulai hidup
            # ============================

            if volume < 500:
                print("WAITING VOLUME...")
                time.sleep(1)
                continue

            score = calculate_score(mint)

            if score is None:
                score = 0

            # =====================================
            # SIMPAN ALPHA SCORE KE DATABASE
            # =====================================

            conn = sqlite3.connect(DB)

            conn.execute("""
            UPDATE tokens
            SET alpha_score=?
            WHERE mint=?
            """, (score, mint))

            conn.commit()
            conn.close()

            print()
            print("=" * 70)
            print("READY")
            print("ALPHA :", round(score, 2))
            print("=" * 70)

            check_token(mint, score)

            time.sleep(1)

        time.sleep(5)


if __name__ == "__main__":
    worker()