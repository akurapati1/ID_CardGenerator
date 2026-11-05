# ID_CardGenerator

Generate print-ready **employee ID cards** as a multi-page PDF from a template image, a CSV of employees and a folder of photos — one card per page, sized exactly to the template.

![Sample card](docs/preview.png)

## Features
- Page size is derived from the template image; the template is drawn as the card background
- Photos are scaled to fit the template's photo slot while **preserving aspect ratio**
- CSV validation (required columns) and graceful handling of missing photos (skipped with a warning)
- Clean CLI with sensible defaults; unit tests and CI

## Usage
```bash
pip install -r requirements.txt
python main.py            # uses ute_id_template.png, file.csv, employees/ -> employee_ids.pdf
python main.py --template my_template.png --csv staff.csv --photos photos --out staff_ids.pdf
```

### Input format
`file.csv`
```csv
name,title,photo
John Doe,Software Engineer,e1.png
Jane Smith,Product Manager,e2.png
```
`photo` is a file name inside the `--photos` directory.

### Using your own template
Adjust `PHOTO_BOX` (photo slot) and `TEXT_X / NAME_Y / TITLE_Y` at the top of `main.py` to match your design.

## Tests
```bash
pytest
```
