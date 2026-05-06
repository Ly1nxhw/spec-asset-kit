from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write a message to a file.")
    parser.add_argument("--message", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def write_message(message: str, output: str) -> None:
    Path(output).write_text(message + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_message(args.message, args.output)
    if args.dry_run:
        print(f"dry-run: would write {args.output}")
    else:
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
