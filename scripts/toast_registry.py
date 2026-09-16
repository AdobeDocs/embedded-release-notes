#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_TOAST_KEYS = {
    "id",
    "surface",
    "release",
    "title",
    "items",
    "action",
    "dismiss",
    "source_request",
}


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read JSON from {path}: {error}") from error


def validate_toast(toast, index):
    errors = []
    missing = REQUIRED_TOAST_KEYS - set(toast)
    if missing:
        errors.append(f"toasts[{index}] missing: {', '.join(sorted(missing))}")
        return errors

    if not SLUG_PATTERN.fullmatch(toast["id"]):
        errors.append(f"toasts[{index}].id must be lowercase kebab-case")
    if not SLUG_PATTERN.fullmatch(toast["surface"]):
        errors.append(f"toasts[{index}].surface must be lowercase kebab-case")

    release = toast["release"]
    if not isinstance(release, dict):
        errors.append(f"toasts[{index}].release must be an object")
    else:
        year = release.get("year")
        month = release.get("month")
        if not isinstance(year, int) or not 2000 <= year <= 2100:
            errors.append(f"toasts[{index}].release.year is invalid")
        if not isinstance(month, int) or not 1 <= month <= 12:
            errors.append(f"toasts[{index}].release.month is invalid")
        if not SLUG_PATTERN.fullmatch(str(release.get("slug", ""))):
            errors.append(f"toasts[{index}].release.slug must be lowercase kebab-case")
        if not str(release.get("label", "")).strip():
            errors.append(f"toasts[{index}].release.label is required")
        if isinstance(year, int) and isinstance(month, int):
            expected_id = (
                f"{toast['surface']}-{year}-{month:02d}-{release.get('slug', '')}"
            )
            if toast["id"] != expected_id:
                errors.append(
                    f"toasts[{index}].id must equal {expected_id}"
                )

    if not str(toast["title"]).strip():
        errors.append(f"toasts[{index}].title is required")
    items = toast["items"]
    if not isinstance(items, list) or len(items) != 2:
        errors.append(f"toasts[{index}].items must contain exactly 2 items")
    else:
        for item_index, item in enumerate(items):
            prefix = f"toasts[{index}].items[{item_index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for field in ("title", "description"):
                if not str(item.get(field, "")).strip():
                    errors.append(f"{prefix}.{field} is required")
            icon = item.get("icon")
            if not isinstance(icon, dict):
                errors.append(f"{prefix}.icon must be an object")
                continue
            if not SLUG_PATTERN.fullmatch(str(icon.get("name", ""))):
                errors.append(f"{prefix}.icon.name must be lowercase kebab-case")
            for field in ("foreground", "background"):
                if not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(icon.get(field, ""))):
                    errors.append(f"{prefix}.icon.{field} must be a hex color")

    action = toast["action"]
    if not isinstance(action, dict):
        errors.append(f"toasts[{index}].action must be an object")
    else:
        if not str(action.get("label", "")).strip():
            errors.append(f"toasts[{index}].action.label is required")
        href = str(action.get("href", ""))
        if not re.fullmatch(
            r"generated/[a-z0-9-]+/[0-9]{4}/[0-9]{2}/[a-z0-9-]+/hub\.html",
            href,
        ):
            errors.append(
                f"toasts[{index}].action.href must point to a generated hub.html"
            )

    dismiss = toast["dismiss"]
    if not isinstance(dismiss, dict) or not str(dismiss.get("label", "")).strip():
        errors.append(f"toasts[{index}].dismiss.label is required")
    if not str(toast["source_request"]).strip():
        errors.append(f"toasts[{index}].source_request is required")
    return errors


def validate_references(toast, index, repo_root):
    errors = []
    source_request = toast.get("source_request", "")
    request_path = (repo_root / source_request).resolve()
    requests_root = (repo_root / "requests").resolve()
    if requests_root not in request_path.parents or not request_path.is_file():
        return [f"toasts[{index}].source_request does not exist: {source_request}"]

    try:
        request = load_json(request_path)
    except ValueError as error:
        return [f"toasts[{index}].source_request is invalid: {error}"]

    if "toast" not in request.get("deliverables", []):
        errors.append(f"toasts[{index}] source request does not include toast")
    if toast.get("surface") != request.get("toast", {}).get("surface"):
        errors.append(f"toasts[{index}].surface differs from its source request")
    expected_release = {
        "year": request.get("year"),
        "month": request.get("month"),
        "slug": request.get("slug"),
    }
    actual_release = toast.get("release", {})
    for field, expected_value in expected_release.items():
        if actual_release.get(field) != expected_value:
            errors.append(
                f"toasts[{index}].release.{field} differs from its source request"
            )

    expected_href = f"{request.get('output_directory', '')}hub.html"
    actual_href = toast.get("action", {}).get("href")
    if actual_href != expected_href:
        errors.append(
            f"toasts[{index}].action.href must equal source output hub: {expected_href}"
        )
    if not (repo_root / expected_href).is_file():
        errors.append(f"toasts[{index}] generated hub does not exist: {expected_href}")
    return errors


def validate_registry(registry, repo_root=None):
    errors = []
    if registry.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    surfaces = registry.get("surfaces")
    if not isinstance(surfaces, dict):
        return errors + ["surfaces must be an object keyed by surface"]

    for index, (surface, toast) in enumerate(sorted(surfaces.items())):
        if not isinstance(toast, dict):
            errors.append(f"surfaces.{surface} must be an object")
            continue
        errors.extend(validate_toast(toast, index))
        if toast.get("surface") != surface:
            errors.append(f"surface key {surface} differs from its value")
        if repo_root is not None:
            errors.extend(validate_references(toast, index, repo_root))
    return errors


def write_registry(path, registry):
    path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def command_validate(args):
    errors = validate_registry(load_json(args.registry), args.registry.resolve().parent)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Valid registry: {args.registry}")
    return 0


def command_list(args):
    registry = load_json(args.registry)
    errors = validate_registry(registry, args.registry.resolve().parent)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for surface, toast in sorted(registry["surfaces"].items()):
        print(f"{surface}\t{toast['id']}\t{toast['action']['href']}")
    return 0


def command_resolve(args):
    registry = load_json(args.registry)
    errors = validate_registry(registry, args.registry.resolve().parent)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    toast = registry["surfaces"].get(args.surface)
    if toast is None:
        print(f"ERROR: no release note for surface {args.surface}", file=sys.stderr)
        return 1
    print(json.dumps(toast, indent=2))
    return 0


def command_upsert(args):
    registry = load_json(args.registry)
    entry = load_json(args.entry)
    entry_errors = validate_toast(entry, 0)
    if entry_errors:
        for error in entry_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    surfaces = dict(registry.get("surfaces", {}))
    surfaces[entry["surface"]] = entry
    registry["surfaces"] = dict(sorted(surfaces.items()))
    errors = validate_registry(registry, args.registry.resolve().parent)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    write_registry(args.registry, registry)
    print(f"Upserted {entry['id']} for surface {entry['surface']}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Manage the central toast registry.")
    parser.add_argument("--registry", type=Path, default=Path("toast.json"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.set_defaults(handler=command_validate)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(handler=command_list)

    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("--surface", required=True)
    resolve_parser.set_defaults(handler=command_resolve)

    upsert_parser = subparsers.add_parser("upsert")
    upsert_parser.add_argument("--entry", type=Path, required=True)
    upsert_parser.set_defaults(handler=command_upsert)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())