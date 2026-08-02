import sqlite3
from collections import Counter
from datetime import datetime



class CreatorBehavior:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    # ==========================================
    # ANALYZE CREATOR BEHAVIOR
    # ==========================================


    def analyze(self, creator):


        self.cursor.execute(
            """
            SELECT
                name,
                symbol,
                sol_amount,
                created_at
            FROM tokens
            WHERE creator = ?
            ORDER BY created_at ASC
            """,
            (creator,)
        )


        rows = self.cursor.fetchall()



        if not rows:

            return None



        total_token = len(rows)



        names = []

        symbols = []

        sol_values = []

        times = []



        for row in rows:


            names.append(
                row[0]
            )


            symbols.append(
                row[1]
            )


            sol_values.append(
                row[2]
            )


            try:

                times.append(
                    datetime.fromisoformat(
                        str(row[3])
                    )
                )

            except:

                pass




        # ======================================
        # INTERVAL
        # ======================================


        intervals = []


        for i in range(1, len(times)):


            diff = (
                times[i] - times[i-1]
            ).total_seconds()


            intervals.append(
                diff
            )



        avg_interval = 0


        if intervals:

            avg_interval = round(
                sum(intervals) / len(intervals),
                2
            )




        # ======================================
        # FAST LAUNCH
        # < 5 menit
        # ======================================


        fast_launch = 0


        for x in intervals:


            if x < 300:

                fast_launch += 1





        # ======================================
        # SAME SOL PATTERN
        # ======================================


        sol_counter = Counter(
            round(x,4)
            for x in sol_values
        )


        common_sol = 0

        same_sol_pattern = False



        if sol_counter:


            common_sol = sol_counter.most_common(1)[0][0]


            if sol_counter.most_common(1)[0][1] >= total_token * 0.5:

                same_sol_pattern = True





        # ======================================
        # DUPLICATE PATTERN
        # ======================================


        duplicate_name = (
            total_token -
            len(set(names))
        )


        duplicate_symbol = (
            total_token -
            len(set(symbols))
        )




        # ======================================
        # BEHAVIOR RISK
        # ======================================


        risk = 0


        reasons = []



        if fast_launch >= 10:


            risk += 30


            reasons.append(
                "Mass launch detected"
            )



        if same_sol_pattern:


            risk += 25


            reasons.append(
                "Same SOL launch pattern"
            )



        if duplicate_name > 5:


            risk += 20


            reasons.append(
                "Duplicate token names"
            )



        if duplicate_symbol > 5:


            risk += 15


            reasons.append(
                "Duplicate token symbols"
            )



        risk = min(
            risk,
            100
        )




        behavior_score = max(
            100 - risk,
            0
        )





        return {


            "creator": creator,


            "total_token": total_token,


            "average_interval": avg_interval,


            "fast_launch": fast_launch,


            "same_sol_pattern": same_sol_pattern,


            "common_sol": common_sol,


            "duplicate_name": duplicate_name,


            "duplicate_symbol": duplicate_symbol,


            "behavior_risk": risk,


            "behavior_score": behavior_score,


            "reasons": reasons

        }





    # ==========================================
    # BACKWARD COMPATIBILITY
    # ==========================================


    def calculate(self, creator):

        return self.analyze(
            creator
        )




    def close(self):

        self.conn.close()







if __name__ == "__main__":


    creator = input(
        "Creator Address : "
    ).strip()



    engine = CreatorBehavior()


    result = engine.analyze(
        creator
    )



    print()


    print(
        "========================================"
    )


    print(
        "CREATOR BEHAVIOR"
    )


    print(
        "========================================"
    )



    if result:


        print(
            f"Creator          : {result['creator']}"
        )


        print(
            f"Total Token      : {result['total_token']}"
        )


        print(
            f"Average Interval : {result['average_interval']} seconds"
        )


        print(
            f"Fast Launch      : {result['fast_launch']}"
        )


        print(
            f"Same SOL Pattern : {result['same_sol_pattern']}"
        )


        print(
            f"Common SOL       : {result['common_sol']}"
        )


        print("----------------------------------------")


        print(
            f"Behavior Risk    : {result['behavior_risk']}/100"
        )


        print(
            f"Behavior Score   : {result['behavior_score']}/100"
        )


        print("----------------------------------------")


        print(
            "REASONS"
        )


        for r in result["reasons"]:

            print(
                "-",
                r
            )



    engine.close()