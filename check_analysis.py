import sqlite3
import json



conn = sqlite3.connect(
    "backend/database/tokens.db"
)


cursor = conn.cursor()



cursor.execute(
    """
    SELECT
        creator,
        final_score,
        verdict,
        confidence,
        creator_score,
        pattern_score,
        behavior_score,
        behavior_risk,
        survival_score,
        reasons,
        created_at
    FROM creator_analysis
    ORDER BY id DESC
    """
)



rows = cursor.fetchall()



print()

print("==============================")
print("CREATOR ANALYSIS DATABASE")
print("==============================")



for row in rows:


    print()

    print("--------------------------------")

    print(
        "Creator        :",
        row[0]
    )

    print(
        "Final Score    :",
        row[1]
    )

    print(
        "Verdict        :",
        row[2]
    )

    print(
        "Confidence     :",
        row[3]
    )

    print(
        "Creator Score  :",
        row[4]
    )

    print(
        "Pattern Score  :",
        row[5]
    )

    print(
        "Behavior Score :",
        row[6]
    )

    print(
        "Behavior Risk  :",
        row[7]
    )

    print(
        "Survival Score :",
        row[8]
    )


    print()

    print(
        "Reasons:"
    )


    reasons = json.loads(
        row[9]
    )


    for r in reasons:

        print(
            "-",
            r
        )


    print()

    print(
        "Created        :",
        row[10]
    )



conn.close()