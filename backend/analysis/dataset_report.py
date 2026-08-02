from backend.analysis.report_general import ReportGeneral
from backend.analysis.report_market import ReportMarket
from backend.analysis.report_creator import ReportCreator


def main():

    general = ReportGeneral()
    market = ReportMarket()
    creator = ReportCreator()

    g = general.generate()
    m = market.generate()
    c = creator.generate()

    print()
    print("==========================================")
    print("      SOLANA DATASET REPORT")
    print("==========================================")

    print()
    print("GENERAL")
    print("------------------------------------------")
    print(f"Total Token           : {g['total_token']}")
    print(f"Unique Mint           : {g['total_mint']}")
    print(f"Unique Creator        : {g['total_creator']}")
    print(f"Duplicate Token       : {g['duplicate']}")
    print(f"Average TokenCreator  : {g['avg_token_creator']:.2f}")

    print()
    print("MARKET")
    print("------------------------------------------")
    print(f"Average Initial Buy   : {m['avg_initial_buy']:.4f}")
    print(f"Average SOL Amount    : {m['avg_sol']:.4f}")
    print(f"Average MarketCap     : {m['avg_marketcap']:.2f}")
    print(f"Highest MarketCap     : {m['highest_marketcap']:.2f}")
    print(f"Lowest MarketCap      : {m['lowest_marketcap']:.2f}")

    print()
    print("TOP 10 CREATOR")
    print("------------------------------------------")

    for i, (wallet, total) in enumerate(c, start=1):
        print(f"{i:>2}. {wallet} ({total} token)")

    general.close()
    market.close()
    creator.close()

    print()
    print("==========================================")


if __name__ == "__main__":
    main()