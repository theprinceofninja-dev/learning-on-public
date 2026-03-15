import re

import PyPDF2


def find_text_locations(input_pdf_path, search_text):
    """
    Find text locations in PDF using PyPDF2.
    """

    with open(input_pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            if search_text in text:
                print(f"\n✓ Found '{search_text}' on page {page_num + 1}")
                print("Text context:")

                # Show lines containing the search text
                lines = text.split("\n")
                for line in lines:
                    if search_text in line:
                        print(f"  {line}")

                # Count occurrences
                count = text.count(search_text)
                print(f"  Found {count} occurrence(s) on this page")


# Usage
find_text_locations("/home/*******/Downloads/FCH Test_AUG_22.pdf", "SYR01")
