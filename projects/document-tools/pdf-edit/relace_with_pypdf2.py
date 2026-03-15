import io
import re

import PyPDF2
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def replace_text_in_pdf(
    input_pdf_path,
    output_pdf_path,
    old_text,
    new_text,
    font_name="Helvetica",
    font_size=12,
):
    """
    Replace text in PDF by creating a new PDF with replaced text.
    This preserves the original layout by using the original PDF as a background.
    """

    print(f"Processing PDF: {input_pdf_path}")
    print(f"Replacing '{old_text}' with '{new_text}'")

    # Read the original PDF
    with open(input_pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        print(f"Found {num_pages} pages in the PDF")

        # Create a new PDF writer
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(num_pages):
            print(f"\nProcessing page {page_num + 1}...")

            page = pdf_reader.pages[page_num]

            # Extract text from the page
            text = page.extract_text()

            # Check if the text exists on this page
            if old_text in text:
                count = text.count(old_text)
                print(f"  Found {count} occurrence(s) of '{old_text}'")

                # Get page dimensions
                mediabox = page.mediabox
                page_width = float(mediabox.width)
                page_height = float(mediabox.height)

                print(f"  Page size: {page_width} x {page_height}")

                # Create a new PDF page with the same dimensions
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(page_width, page_height))

                # Extract text with more detail to get positions
                # PyPDF2 doesn't give text positions, so we'll use a different approach

                # Split text into lines to approximate positioning
                lines = text.split("\n")
                y_position = page_height - 50  # Start near the top

                for line in lines:
                    # Replace text in this line
                    if old_text in line:
                        modified_line = line.replace(old_text, new_text)
                        print(f"  Original: {line}")
                        print(f"  Modified: {modified_line}")
                    else:
                        modified_line = line

                    # Draw the line (this is simplified - exact positioning would need more work)
                    can.setFont(font_name, font_size)
                    can.drawString(50, y_position, modified_line)
                    y_position -= 20

                can.save()

                # Move to the beginning of the StringIO buffer
                packet.seek(0)

                # Create a new PDF with the text
                new_pdf = PyPDF2.PdfReader(packet)
                text_page = new_pdf.pages[0]

                # Merge the original page (as background) with new text
                # Create a new page object
                merged_page = PyPDF2.PageObject.create_blank_page(
                    width=page_width, height=page_height
                )

                # Merge original page first (as background)
                merged_page.merge_page(page)

                # Merge text page on top
                merged_page.merge_page(text_page)

                # Add to writer
                pdf_writer.add_page(merged_page)

            else:
                print(f"  Text '{old_text}' not found on this page")
                # Add original page unchanged
                pdf_writer.add_page(page)

        # Write the output PDF
        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)

        print(f"\n✅ Success! Modified PDF saved to: {output_pdf_path}")


def find_text_locations(input_pdf_path, search_text):
    """
    Find text locations in PDF using PyPDF2.
    Helper function to verify text exists.
    """

    print(f"\n=== Searching for '{search_text}' in PDF ===")

    with open(input_pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_occurrences = 0

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            if search_text in text:
                count = text.count(search_text)
                total_occurrences += count
                print(f"\n✓ Found '{search_text}' on page {page_num + 1}")
                print(f"  Occurrences: {count}")

                # Show lines containing the search text
                lines = text.split("\n")
                found_lines = []
                for line in lines:
                    if search_text in line:
                        found_lines.append(line)

                if found_lines:
                    print("  Context lines:")
                    for line in found_lines[:3]:  # Show first 3 lines
                        print(f"    - {line}")
                    if len(found_lines) > 3:
                        print(f"    ... and {len(found_lines) - 3} more lines")

        if total_occurrences == 0:
            print(f"\n❌ Text '{search_text}' not found in the PDF")
        else:
            print(f"\n📊 Total occurrences found: {total_occurrences}")

        return total_occurrences > 0


# Main execution
if __name__ == "__main__":
    # Configuration
    #  = "input.pdf"  # Change this to your input file
    #  = "output.pdf"  # Change this to your output file
    #  = "ABCDE"  # Text to search for
    #  = "XYZWQ"  # Text to replace with
    input_pdf = "/home/*******/Downloads/FCH Test_AUG_22.pdf"
    output_pdf = "/home/*******/Downloads/output.pdf"
    text_to_find = "SYR01OMNNT05"
    text_to_replace = "XYZ01ABC0144"

    print("=" * 60)
    print("PDF Text Replacement Tool")
    print("=" * 60)

    # First, verify the text exists
    if find_text_locations(input_pdf, text_to_find):
        # If text exists, proceed with replacement
        print("\n" + "=" * 60)
        print("Starting text replacement...")
        print("=" * 60)

        replace_text_in_pdf(
            input_pdf_path=input_pdf,
            output_pdf_path=output_pdf,
            old_text=text_to_find,
            new_text=text_to_replace,
            font_name="Helvetica",  # You can change font if needed
            font_size=12,  # You can adjust font size
        )
    else:
        print("\n❌ Cannot proceed - text not found in PDF.")
        print("Please check:")
        print("1. The text spelling (case-sensitive)")
        print("2. That the PDF contains selectable text (not scanned images)")
        print("3. That you're using the correct input file")
