import argparse


def _parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("test", type=str, default="", help="Replace this")
    args = parser.parse_args()
    return args


def main():
    # parse command line arguments
    args = _parse()

    # logic
    print(args.test)


if __name__ == "__main__":
    main()
