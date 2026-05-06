from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write a message to a file.")
    parser.add_argument("--message", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the write without creating the output file.",
    )
    return parser


def write_message(message: str, output: str, *, dry_run: bool = False) -> None:
    if dry_run:
        print(f"dry-run: would write {message!r} to {output}")
        return
    Path(output).write_text(message + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_message(args.message, args.output, dry_run=args.dry_run)
    if not args.dry_run:
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
