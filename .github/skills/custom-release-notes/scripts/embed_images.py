#!/usr/bin/env python3
"""
Resolve ASSET: image markers in a release-notes HTML draft into inline base64
data URIs, so the final file is a single self-contained HTML document (no
external file dependencies) — matching the "standalone HTML" requirement.

Usage:
    python3 embed_images.py <draft.html> <assets_folder> [-o output.html]

In the draft HTML, reference source screenshots like this:
    <img src="ASSET:campaign-insights.png" alt="...">
The script looks for campaign-insights.png anywhere under <assets_folder>
(recursively, so subfolders like assets-RN/Loyalty/ are found automatically),
base64-encodes it, and replaces the marker with a data: URI in place.

If a referenced filename can't be found, the script leaves the marker
untouched and prints a warning listing the closest-named files it did find,
so nothing fails silently.
"""
import argparse
import base64
import difflib
import mimetypes
import os
import re
import sys

ASSET_RE = re.compile(r'src="ASSET:([^"]+)"')


def build_index(assets_folder):
    index = {}
    for root, _dirs, files in os.walk(assets_folder):
        for fname in files:
            if fname.startswith('.'):
                continue
            index.setdefault(fname, os.path.join(root, fname))
    return index


def encode_file(path):
    mime, _ = mimetypes.guess_type(path)
    if mime is None:
        mime = 'image/png'
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('ascii')
    return f"data:{mime};base64,{data}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('draft_html')
    ap.add_argument('assets_folder')
    ap.add_argument('-o', '--output', help='output path (default: overwrite draft in place)')
    args = ap.parse_args()

    with open(args.draft_html, encoding='utf-8') as f:
        html = f.read()

    index = build_index(args.assets_folder)
    names = list(index.keys())

    missing = []

    def replace(match):
        fname = match.group(1)
        if fname in index:
            return f'src="{encode_file(index[fname])}"'
        missing.append(fname)
        return match.group(0)

    result = ASSET_RE.sub(replace, html)

    remaining = len(ASSET_RE.findall(result))
    resolved = len(ASSET_RE.findall(html)) - remaining

    out_path = args.output or args.draft_html
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Resolved {resolved} image reference(s). Wrote {out_path}")

    if missing:
        print(f"\nWARNING: {len(missing)} asset(s) not found under {args.assets_folder}:", file=sys.stderr)
        for fname in sorted(set(missing)):
            close = difflib.get_close_matches(fname, names, n=3, cutoff=0.4)
            hint = f" — did you mean: {', '.join(close)}?" if close else ""
            print(f"  - {fname}{hint}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
