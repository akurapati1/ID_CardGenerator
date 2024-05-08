from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import utils
import csv
import os

def create_id_pdf(template_image, csv_file, photo_dir, output_pdf):
    # Calculate page size based on template image size
    img = utils.ImageReader(template_image)
    width, height = img.getSize()
    page_size = (width, height)

    # Create a PDF file
    c = canvas.Canvas(output_pdf, pagesize=page_size)

    # Read employee details from CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Load employee photo
            photo_path = os.path.join(photo_dir, row['photo'])
            c.drawImage(photo_path, 0, 0, width=2.5*inch, height=2.5*inch)

            # Add employee details
            c.setFont("Helvetica", 12)
            c.drawString(3*inch, height-1*inch, "Name: {}".format(row['name']))
            c.drawString(3*inch, height-1.5*inch, "Title: {}".format(row['title']))

            # Add any additional fields as needed

            c.showPage()  # Move to the next page for the next ID

    c.save()

# Example usage
template_image = 'ute_id_template'
csv_file = 'file.csv'
photo_dir = 'employees'
output_pdf = 'employee_ids.pdf'

create_id_pdf(template_image, csv_file, photo_dir, output_pdf)
