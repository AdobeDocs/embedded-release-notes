#!/usr/bin/env python3
import argparse
import json
import re
from datetime import date
from pathlib import Path


SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VALUE_SCOPES = {"latest-updates", "custom"}


def slug(value):
    if not SLUG_PATTERN.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "must use lowercase ASCII kebab-case (for example: loyalty-admin)"
        )
    return value


def unique(values):
    return list(dict.fromkeys(values or []))


def build_parser():
    parser = argparse.ArgumentParser(
        description="Create a versioned embedded release-notes request."
    )
    parser.add_argument("--products", nargs="+", required=True, type=slug)
    parser.add_argument(
        "--deliverables",
        nargs="+",
        choices=("hub", "toast"),
        default=("hub", "toast"),
    )
    parser.add_argument("--year", type=int, default=date.today().year)
    parser.add_argument("--month", type=int, default=date.today().month)
    parser.add_argument("--slug", required=True, type=slug)
    parser.add_argument("--theme", required=True)
    parser.add_argument("--persona", default="Generic")
    parser.add_argument(
        "--release-scope",
        choices=(
            "latest-release",
            "last-two-releases",
            "latest-updates",
            "custom",
        ),
        default="latest-release",
    )
    parser.add_argument("--release-value")
    parser.add_argument("--include", action="append", default=[])
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--source-repo", action="append", default=[])
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not 2000 <= args.year <= 2100:
        parser.error("--year must be between 2000 and 2100")
    if not 1 <= args.month <= 12:
        parser.error("--month must be between 1 and 12")
    if args.release_scope in VALUE_SCOPES and not args.release_value:
        parser.error(f"--release-value is required for {args.release_scope}")

    products = unique(args.products)
    product_scope = "-".join(products)
    month = f"{args.month:02d}"
    relative_output = Path("generated", product_scope, str(args.year), month, args.slug)
    relative_request = Path("requests", product_scope, str(args.year), month, f"{args.slug}.json")
    repo_root = args.repo_root.resolve()
    request_path = repo_root / relative_request
    output_path = repo_root / relative_output

    if request_path.exists():
        parser.error(f"request already exists: {relative_request.as_posix()}")

    request = {
        "schema_version": 1,
        "status": "intake",
        "products": products,
        "deliverables": unique(args.deliverables),
        "year": args.year,
        "month": args.month,
        "slug": args.slug,
        "theme": args.theme,
        "persona": args.persona,
        "release_scope": args.release_scope,
        "release_value": args.release_value,
        "include": unique(args.include),
        "exclude": unique(args.exclude),
        "source_repos": unique(args.source_repo),
        "output_directory": f"{relative_output.as_posix()}/",
        "created_on": date.today().isoformat(),
    }

    request_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    request_path.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")

    print(f"Created request: {relative_request.as_posix()}")
    print(f"Output directory: {relative_output.as_posix()}/")
    print(f"Run skill: /custom-release-notes request={relative_request.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())