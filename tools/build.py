#!/usr/bin/env python3
"""
Fill in your callback host and write ready-to-upload payloads to dist/.

  python3 tools/build.py --collab abc123.oast.fun
  python3 tools/build.py --collab abc123.oast.fun --only xss xxe
  python3 tools/build.py --list
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATEGORIES = ["xss", "xxe", "ssrf", "ssti", "renderers"]
EXTENSIONS = {".svg", ".dtd"}
PLACEHOLDER = "COLLAB_HOST"


def payload_files(categories):
    for cat in categories:
        base = ROOT / cat
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in EXTENSIONS:
                yield path


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--collab", help="callback host, e.g. abc123.oast.fun (no scheme)")
    ap.add_argument("--only", nargs="+", choices=CATEGORIES, default=CATEGORIES,
                    help="limit to these categories")
    ap.add_argument("--out", default=str(ROOT / "dist"), help="output directory (default: dist/)")
    ap.add_argument("--list", action="store_true", help="list payload files and exit")
    args = ap.parse_args()

    files = list(payload_files(args.only))
    if args.list:
        for f in files:
            print(f.relative_to(ROOT))
        print(f"{len(files)} files")
        return 0

    if not args.collab:
        ap.error("--collab is required (unless --list)")

    host = args.collab.strip()
    for prefix in ("https://", "http://"):
        if host.startswith(prefix):
            host = host[len(prefix):]
    host = host.strip("/")

    out = pathlib.Path(args.out)
    for f in files:
        dest = out / f.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f.read_text(encoding="utf-8").replace(PLACEHOLDER, host), encoding="utf-8")
    print(f"wrote {len(files)} files to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
