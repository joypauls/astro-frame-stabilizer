import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("test", type=str, default="", help="Replace this")
    args = parser.parse_args()
    return args


def main():
    # parse command line arguments
    args = parse()

    # logic


if __name__ == "__main__":
    main()
