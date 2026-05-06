from __future__ import annotations

from sample_cli import main


def test_main_writes_message(tmp_path):
    output = tmp_path / "message.txt"

    rc = main(["--message", "hello", "--output", str(output)])

    assert rc == 0
    assert output.read_text(encoding="utf-8") == "hello\n"


def test_dry_run_does_not_write_file(tmp_path, capsys):
    output = tmp_path / "message.txt"

    rc = main(["--message", "hello", "--output", str(output), "--dry-run"])

    assert rc == 0
    assert not output.exists()
    assert "dry-run: would write 'hello'" in capsys.readouterr().out
