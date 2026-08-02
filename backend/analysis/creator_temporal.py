import sqlite3
from datetime import datetime


class CreatorTemporal:


    def __init__(self):

        self.conn = sqlite3.connect(
            "backend/database/tokens.db"
        )

        self.cursor = self.conn.cursor()



    def parse_date(self, value):

        if value is None:
            return None


        formats = [

            "%Y-%m-%d %H:%M:%S",

            "%Y-%m-%d",

            "%Y-%m-%dT%H:%M:%S"

        ]


        for f in formats:

            try:

                return datetime.strptime(
                    value,
                    f
                )

            except:

                pass


        return None





    def analyze(self, creator):


        self.cursor.execute(
            """
            SELECT *
            FROM tokens
            WHERE creator = ?
            """,
            (creator,)
        )


        rows = self.cursor.fetchall()


        if len(rows)==0:

            return None



        total_token = len(rows)



        dates=[]


        for row in rows:


            for item in row:


                if isinstance(item,str):

                    date=self.parse_date(item)

                    if date:

                        dates.append(date)





        age_days=0



        if len(dates)>=2:


            first=min(dates)

            last=max(dates)


            age_days=(

                last-first

            ).days





        frequency=total_token



        if age_days>0:

            frequency=round(

                total_token/age_days,

                2

            )





        score=60


        reasons=[]





        if frequency>=10:


            score-=40

            reasons.append(

                "Extreme launch frequency"

            )


        elif frequency>=3:


            score-=20

            reasons.append(

                "High launch frequency"

            )


        else:

            score+=10





        if total_token>=30:


            reasons.append(

                "Large token production"

            )

            score-=10






        if age_days>=90:


            score+=20

            reasons.append(

                "Established creator"

            )


        elif age_days<7:


            reasons.append(

                "Very new creator"

            )





        score=max(

            0,

            min(score,100)

        )




        return {


            "creator":creator,

            "total_token":total_token,

            "age_days":age_days,

            "frequency":frequency,

            "temporal_score":score,

            "reasons":reasons

        }





    def close(self):

        self.conn.close()






if __name__=="__main__":


    creator=input(
        "Creator Address : "
    ).strip()


    engine=CreatorTemporal()


    result=engine.analyze(
        creator
    )


    print()

    print("==============================")
    print(" CREATOR TEMPORAL V2 ")
    print("==============================")


    print(
        f"Creator       : {result['creator']}"
    )

    print(
        f"Total Token   : {result['total_token']}"
    )

    print(
        f"Age Days      : {result['age_days']}"
    )

    print(
        f"Frequency     : {result['frequency']}"
    )

    print("--------------------------------")

    print(
        f"Temporal Score : {result['temporal_score']}/100"
    )


    print("--------------------------------")


    for r in result["reasons"]:

        print(
            "-",
            r
        )


    engine.close()