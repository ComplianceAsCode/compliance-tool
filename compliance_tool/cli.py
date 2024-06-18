import argparse
from compliance_tool import list_, scan, remediate


def prepare_parser_list(cli_sub_parsers, global_parser, profile_parser) -> None:
    parser = cli_sub_parsers.add_parser("list", parents=[global_parser],
                                        help="list available components"
                                             " (profiles, rules, controls),"
                                             " will list profiles if component type"
                                             " is not specified")
    # TODO: Set individual functions for sub-parsers to distinguish between listing modes
    #       this one should be linked with listing profiles as we consider it to
    #       be the default listing operation.
    parser.set_defaults(func=list_.execute)
    list_subparsers = parser.add_subparsers(required=False)

    list_subparsers.add_parser("profiles",
                               help="list available profiles")

    list_subparsers.add_parser("controls", parents=[profile_parser],
                               help="list available controls (requirements)"
                                    " within a given profile")

    list_subparsers.add_parser("rules", parents=[profile_parser],
                               help="list available rules for a given profile")


def prepare_parser_scan(cli_sub_parsers, global_parser, profile_parser) -> None:
    parser = cli_sub_parsers.add_parser("scan", parents=[global_parser, profile_parser],
                                        help="perform a compliance scan")
    parser.set_defaults(func=scan.execute)

    parser.add_argument("--control", metavar="CONTROL_ID",
                        help="use only control(s) (requirement(s)) with given identifier")
    parser.add_argument("--rule", metavar="RULE_ID",
                        help="use only rule(s) with given identifier")

    parser.add_argument("--html", metavar="DESTINATION_FILE",
                        help="write a human-readable HTML report with the results"
                             " at the given destination")
    parser.add_argument("--json", metavar="DESTINATION_FILE",
                        help="write a JSON-formatted report with the results"
                             " at the given destination")


def prepare_parser_remediate(cli_sub_parsers, global_parser, profile_parser) -> None:
    parser = cli_sub_parsers.add_parser("remediate", parents=[global_parser, profile_parser],
                                        help="perform a system remediation")
    parser.set_defaults(func=remediate.execute)

    parser.add_argument("--control", metavar="CONTROL_ID",
                        help="control (requirement) identifier")
    parser.add_argument("--rule", metavar="RULE_ID",
                        help="rule identifier")


def prepare_parsers() -> argparse.ArgumentParser:
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("--input", metavar="SOURCE_FILE",
                               help="policy definitions (recognized formats: SCAP Data Stream)")
    global_parser.add_argument("--tailoring", metavar="SOURCE_FILE",
                               help="policy customizations"
                                    " (recognized formats: JSON Tailoring)")

    profile_parser = argparse.ArgumentParser(add_help=False)
    profile_parser.add_argument("--profile", metavar="PROFILE_ID",
                                required=True,
                                help="identifier of the profile that should be used"
                                     " for selected operation")

    cli_parser = argparse.ArgumentParser()
    cli_sub_parsers = cli_parser.add_subparsers(required=True)
    prepare_parser_list(cli_sub_parsers, global_parser, profile_parser)
    prepare_parser_scan(cli_sub_parsers, global_parser, profile_parser)
    prepare_parser_remediate(cli_sub_parsers, global_parser, profile_parser)
    return cli_parser


def main() -> int:
    args = prepare_parsers().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
