import argparse
from compliance_tool import list, scan, remediate


def prepare_parser_list(subparsers) -> None:
    parser = subparsers.add_parser("list",
                                   help="list available components")
    parser.set_defaults(func=list.execute)
    list_subparsers = parser.add_subparsers(required=True)

    list_subparsers.add_parser("profiles",
                               help="list available profiles")

    parser = list_subparsers.add_parser("controls",
                                        help="list available controls for a given profile")
    parser.add_argument("--profile")

    parser = list_subparsers.add_parser("rules",
                                        help="list available rules for a given profile")
    parser.add_argument("--profile")


def prepare_parser_scan(subparsers) -> None:
    parser = subparsers.add_parser("scan",
                                   help="perform a compliance scan")
    parser.set_defaults(func=scan.execute)
    parser.add_argument("--profile")
    parser.add_argument("--control")
    parser.add_argument("--rule")

    parser.add_argument("--html")
    parser.add_argument("--json")


def prepare_parser_remediate(subparsers) -> None:
    parser = subparsers.add_parser("remediate",
                                   help="perform a system remediation")
    parser.set_defaults(func=remediate.execute)
    parser.add_argument("--profile")
    parser.add_argument("--control")
    parser.add_argument("--rule")


def prepare_parsers() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    parser.add_argument("--input",
                        help="policy definitions (file)")
    parser.add_argument("--tailoring",
                        help="policy tailoring customization (file)")
    prepare_parser_list(subparsers)
    prepare_parser_scan(subparsers)
    prepare_parser_remediate(subparsers)
    return parser


def main() -> int:
    args = prepare_parsers().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
