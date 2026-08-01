from collector import start
from logger import log


def main():
    print("=" * 40)
    print("IO Pump Intelligence")
    print("=" * 40)

    log("System Starting...")

    start()


if __name__ == "__main__":
    main()