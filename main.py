"""Generate a multi-page employee ID card PDF (one card per page) from a template image and a CSV.

CSV columns: name, title, photo  (photo = file name inside the photo directory)

Usage:
    python main.py --template ute_id_template.png --csv file.csv --photos employees --out employee_ids.pdf
"""
import argparse
import csv
import sys
from pathlib import Path

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

REQUIRED_COLUMNS = {"name", "title", "photo"}
PHOTO_BOX = (176, 66, 121, 120)  # x, y, width, height of the template's orange photo slot (points)
TEXT_X, NAME_Y, TITLE_Y = 14, 27, 11  # text sits on the template's orange footer band


def read_employees(csv_file: Path) -> list[dict]:
    with open(csv_file, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{csv_file} is missing required column(s): {', '.join(sorted(missing))}")
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def draw_photo(c: canvas.Canvas, photo_path: Path, box: tuple[float, float, float, float]) -> None:
    """Draw the photo inside `box`, preserving aspect ratio."""
    x, y, bw, bh = box
    iw, ih = ImageReader(str(photo_path)).getSize()
    scale = min(bw / iw, bh / ih)
    w, h = iw * scale, ih * scale
    c.drawImage(str(photo_path), x + (bw - w) / 2, y + (bh - h) / 2, width=w, height=h, mask="auto")


def create_id_pdf(template_image: Path, csv_file: Path, photo_dir: Path, output_pdf: Path) -> int:
    """Create the PDF and return the number of cards generated. Rows with a missing photo are skipped with a warning."""
    template_image, csv_file, photo_dir = Path(template_image), Path(csv_file), Path(photo_dir)
    width, height = ImageReader(str(template_image)).getSize()
    employees = read_employees(csv_file)

    c = canvas.Canvas(str(output_pdf), pagesize=(width, height))
    count = 0
    for row in employees:
        photo_path = photo_dir / row["photo"]
        if not photo_path.is_file():
            print(f"warning: photo not found for {row['name']!r}: {photo_path} - skipped", file=sys.stderr)
            continue
        c.drawImage(str(template_image), 0, 0, width=width, height=height, mask="auto")
        draw_photo(c, photo_path, PHOTO_BOX)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(TEXT_X, NAME_Y, row["name"])
        c.setFont("Helvetica", 10)
        c.drawString(TEXT_X, TITLE_Y, row["title"])
        c.showPage()
        count += 1
    c.save()
    return count


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--template", default="ute_id_template.png", type=Path)
    p.add_argument("--csv", default="file.csv", type=Path)
    p.add_argument("--photos", default="employees", type=Path)
    p.add_argument("--out", default="employee_ids.pdf", type=Path)
    args = p.parse_args(argv)
    try:
        n = create_id_pdf(args.template, args.csv, args.photos, args.out)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {n} ID card(s) to {args.out}")
    return 0 if n else 2


if __name__ == "__main__":
    sys.exit(main())
