from __future__ import annotations

from sample_cli import build_parser, main


def test_main_writes_message(tmp_path):
    output = tmp_path / "message.txt"

    rc = main(["--message", "hello", "--output", str(output)])

    assert rc == 0
    assert output.read_text(encoding="utf-8") == "hello\n"


def test_parser_accepts_dry_run():
    args = build_parser().parse_args(
        ["--message", "hello", "--output", "message.txt", "--dry-run"]
    )

    assert args.dry_run is True
