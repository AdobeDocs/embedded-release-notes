#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read JSON from {path}: {error}") from error


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def request_paths(repo_root):
    return sorted((repo_root / "requests").glob("**/*.json"))


def validate(repo_root):
    errors = []
    requests = {}
    registry_path = repo_root / "toast.json"
    registry = (
        load_json(registry_path)
        if registry_path.is_file()
        else {"surfaces": {}}
    )
    toasts_by_request = {}
    for toast in registry.get("surfaces", {}).values():
        source_request = toast.get("source_request")
        if source_request:
            toasts_by_request.setdefault(source_request, []).append(toast)

    for request_path in request_paths(repo_root):
        request = load_json(request_path)
        relative_request = request_path.relative_to(repo_root).as_posix()
        requests[relative_request] = request
        expected_name = f"{request.get('slug')}.json"
        if request_path.name != expected_name:
            errors.append(f"request filename mismatch: {relative_request}")
        output = request.get("output_directory", "")
        if not output or not (repo_root / output).is_dir():
            errors.append(f"missing output directory for {relative_request}: {output}")
        if request.get("status") == "generated":
            if "hub" in request.get("deliverables", []):
                hub_path = repo_root / output / "hub.html"
                if not hub_path.is_file():
                    errors.append(f"generated request is missing hub: {hub_path}")
            if "toast" in request.get("deliverables", []):
                matching_toasts = toasts_by_request.get(relative_request, [])
                if len(matching_toasts) != 1:
                    errors.append(
                        f"generated request requires exactly one surface entry: {relative_request}"
                    )
                elif matching_toasts[0].get("surface") != request.get("toast", {}).get("surface"):
                    errors.append(
                        f"toast surface differs from generated request: {relative_request}"
                    )

    if registry_path.is_file():
        for toast in registry.get("surfaces", {}).values():
            source_request = toast.get("source_request")
            if source_request and source_request not in requests:
                errors.append(
                    f"toast {toast.get('id')} references missing request: {source_request}"
                )
    return errors


def command_validate(args):
    errors = validate(args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Release files and references are valid")
    return 0


def command_list(args):
    for request_path in request_paths(args.repo_root):
        request = load_json(request_path)
        relative = request_path.relative_to(args.repo_root).as_posix()
        deliverables = ",".join(request.get("deliverables", []))
        print(f"{relative}\t{request.get('status')}\t{deliverables}")
    return 0


def command_rename(args):
    if not SLUG_PATTERN.fullmatch(args.new_slug):
        print("ERROR: --new-slug must be lowercase kebab-case", file=sys.stderr)
        return 1

    request_path = (args.repo_root / args.request).resolve()
    requests_root = (args.repo_root / "requests").resolve()
    if requests_root not in request_path.parents or not request_path.is_file():
        print("ERROR: --request must identify an existing file under requests/", file=sys.stderr)
        return 1

    request = load_json(request_path)
    old_slug = request["slug"]
    old_output = (args.repo_root / request["output_directory"]).resolve()
    new_request_path = request_path.with_name(f"{args.new_slug}.json")
    new_output = old_output.with_name(args.new_slug)
    if new_request_path.exists() or new_output.exists():
        print("ERROR: rename destination already exists", file=sys.stderr)
        return 1
    if not old_output.is_dir():
        print(f"ERROR: output directory does not exist: {old_output}", file=sys.stderr)
        return 1

    old_relative_request = request_path.relative_to(args.repo_root).as_posix()
    new_relative_request = new_request_path.relative_to(args.repo_root).as_posix()
    request["slug"] = args.new_slug
    request["output_directory"] = f"{new_output.relative_to(args.repo_root).as_posix()}/"

    registry_path = args.repo_root / "toast.json"
    registry = load_json(registry_path)
    surfaces = registry.get("surfaces", {})
    matching_surfaces = [
        surface
        for surface, toast in surfaces.items()
        if toast.get("source_request") == old_relative_request
    ]
    for surface in matching_surfaces:
        toast = surfaces[surface]
        release = toast["release"]
        new_id = f"{surface}-{release['year']}-{release['month']:02d}-{args.new_slug}"
        toast["id"] = new_id
        toast["release"]["slug"] = args.new_slug
        toast["source_request"] = new_relative_request
        toast["action"]["href"] = f"{request['output_directory']}hub.html"
    registry["surfaces"] = dict(sorted(surfaces.items()))

    old_output.rename(new_output)
    write_json(new_request_path, request)
    request_path.unlink()
    write_json(registry_path, registry)
    print(f"Renamed {old_slug} to {args.new_slug}")
    print(f"Request: {new_relative_request}")
    print(f"Output: {request['output_directory']}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Manage generated release-note files.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.set_defaults(handler=command_validate)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(handler=command_list)

    rename_parser = subparsers.add_parser("rename")
    rename_parser.add_argument("--request", type=Path, required=True)
    rename_parser.add_argument("--new-slug", required=True)
    rename_parser.set_defaults(handler=command_rename)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.repo_root = args.repo_root.resolve()
    try:
        return args.handler(args)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())