import re
from io import BytesIO

import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def replace_text_and_create_new_pdf(
    input_pdf_path, output_pdf_path, old_text, new_text
):
    """
    Extract text from PDF, replace it, and create a new PDF with the modified text.
    This doesn't preserve the original layout perfectly.
    """

    # Extract text from the original PDF
    with open(input_pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        all_text = []

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # Replace the text
            modified_text = text.replace(old_text, new_text)
            all_text.append(modified_text)

    # Create a new PDF with the modified text
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    for page_text in all_text:
        # Split text into lines
        lines = page_text.split("\n")

        y_position = height - 50  # Start near the top

        for line in lines:
            if y_position < 50:  # Check if we need a new page
                c.showPage()
                y_position = height - 50

            # Draw the text
            c.drawString(50, y_position, line)
            y_position -= 15  # Move down for next line

        c.showPage()  # New page for next original page

    c.save()
    print(f"New PDF created with replaced text at {output_pdf_path}")
    print(
        "Note: This creates a new PDF with text only, not preserving original layout."
    )


# Usage
replace_text_and_create_new_pdf(
    "/home/*******/Downloads/FCH Test_AUG_22.pdf",
    "/home/*******/Downloads/output.pdf",
    "SYR01OMNNT05",
    "XYZ01ABC0144",
)
