#!/usr/bin/env python3
"""Check or repair external links in generated release-note hubs.

Hubs are embedded in product iframes. External sites such as Experience League
refuse to be framed, so every external link must open in a new tab.
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_TARGET = "_blank"
REQUIRED_REL = ("noopener", "noreferrer")
ANCHOR_TAG = re.compile(r"<a\b[^>]*>", re.IGNORECASE)


def is_external(href):
    return (href or "").strip().lower().startswith(("http://", "https://"))


def is_compliant(attributes):
    rel = (attributes.get("rel") or "").lower().split()
    return attributes.get("target") == REQUIRED_TARGET and all(
        token in rel for token in REQUIRED_REL
    )


class ExternalLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.violations = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attributes = dict(attrs)
        href = attributes.get("href")
        if is_external(href) and not is_compliant(attributes):
            self.violations.append((self.getpos()[0], href))


def find_violations(html):
    parser = ExternalLinkParser()
    parser.feed(html)
    parser.close()
    return parser.violations


class _TagAttributes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attributes = {}

    def handle_starttag(self, tag, attrs):
        self.attributes = {name: value or "" for name, value in attrs}


def _tag_attributes(tag):
    parser = _TagAttributes()
    parser.feed(tag)
    parser.close()
    return parser.attributes


def _repair_tag(tag):
    attributes = _tag_attributes(tag)
    if not is_external(attributes.get("href")) or is_compliant(attributes):
        return tag

    body = tag[:-1].rstrip()
    for name in ("target", "rel"):
        body = re.sub(
            rf"""\s{name}\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)""",
            "",
            body,
            flags=re.IGNORECASE,
        )
    rel_tokens = attributes.get("rel", "").split()
    lowered = [token.lower() for token in rel_tokens]
    rel_tokens += [token for token in REQUIRED_REL if token not in lowered]
    return f'{body} target="{REQUIRED_TARGET}" rel="{" ".join(rel_tokens)}">'


def repair(html):
    repaired = ANCHOR_TAG.sub(lambda match: _repair_tag(match.group(0)), html)
    return repaired, html != repaired


def hub_paths(repo_root, paths):
    if paths:
        return [Path(path) for path in paths]
    return sorted((repo_root / "generated").rglob("*.html"))


def display_path(path, repo_root):
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


def command_check(args):
    failures = 0
    for path in hub_paths(args.repo_root, args.paths):
        for line, href in find_violations(path.read_text(encoding="utf-8")):
            failures += 1
            print(
                f"ERROR: {display_path(path, args.repo_root)}:{line}: external link "
                f'must use target="_blank" rel="noopener noreferrer": {href}',
                file=sys.stderr,
            )
    if failures:
        print(
            f"{failures} external link(s) would navigate inside the product iframe. "
            "Run: python3 scripts/hub_links.py fix",
            file=sys.stderr,
        )
        return 1
    print("All external hub links open in a new tab")
    return 0


def command_fix(args):
    changed = 0
    for path in hub_paths(args.repo_root, args.paths):
        html = path.read_text(encoding="utf-8")
        repaired, was_changed = repair(html)
        if was_changed:
            path.write_text(repaired, encoding="utf-8")
            changed += 1
            print(f"Fixed {display_path(path, args.repo_root)}")
    print(f"{changed} file(s) updated")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name, handler, help_text in (
        ("check", command_check, "fail if an external link opens inside the iframe"),
        ("fix", command_fix, "add the new-tab attributes to external links"),
    ):
        subparser = subparsers.add_parser(name, help=help_text)
        subparser.add_argument(
            "paths", nargs="*", help="HTML files (default: generated/**/*.html)"
        )
        subparser.set_defaults(handler=handler)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.repo_root = args.repo_root.resolve()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
