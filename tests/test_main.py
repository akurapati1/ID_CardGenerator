import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from main import create_id_pdf, main, read_employees  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def test_generates_one_page_per_employee(tmp_path):
    out = tmp_path / "ids.pdf"
    assert create_id_pdf(ROOT / "ute_id_template.png", ROOT / "file.csv", ROOT / "employees", out) == 3
    assert out.read_bytes().count(b"/Type /Page\n") >= 3 or out.stat().st_size > 1000


def test_missing_column_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("name,title\nA,B\n")
    with pytest.raises(ValueError):
        read_employees(bad)


def test_missing_photo_is_skipped(tmp_path):
    csv_file = tmp_path / "e.csv"
    csv_file.write_text("name,title,photo\nA,B,nope.png\n")
    assert create_id_pdf(ROOT / "ute_id_template.png", csv_file, ROOT / "employees", tmp_path / "o.pdf") == 0


def test_cli_returns_error_for_missing_csv(tmp_path):
    assert main(["--csv", str(tmp_path / "missing.csv"), "--out", str(tmp_path / "o.pdf")]) == 1
