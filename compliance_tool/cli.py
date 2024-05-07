import argparse


def prepare_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    parser_scan = subparsers.add_parser("scan", help="Perform a compliance scan")
    parser_scan.add_argument("profile")
    return parser


def main():
    args = prepare_parser().parse_args()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
