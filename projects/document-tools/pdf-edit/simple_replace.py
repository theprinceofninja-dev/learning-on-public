import re

import pdfrw


def simple_text_replace(input_pdf_path, output_pdf_path, old_text, new_text):
    """
    Simple text replacement in PDF content streams.
    """

    template_pdf = pdfrw.PdfReader(input_pdf_path)

    for page in template_pdf.pages:
        if page.Contents:
            contents = page.Contents
            if not isinstance(contents, list):
                contents = [contents]

            for content_obj in contents:
                if hasattr(content_obj, "stream"):
                    content = content_obj.stream

                    # Handle both bytes and string
                    if isinstance(content, bytes):
                        content_str = content.decode("latin-1", errors="ignore")
                    else:
                        content_str = str(content)

                    # Simple text replacement
                    if old_text in content_str:
                        new_content_str = content_str.replace(old_text, new_text)
                        content_obj.stream = new_content_str.encode("latin-1")

    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
    print(f"PDF saved to {output_pdf_path}")


# Usage
simple_text_replace(
    "/home/*******/Downloads/FCH Test_AUG_22.pdf",
    "/home/*******/Downloads/output.pdf",
    "SYR01OMNNT05",
    "XYZ01ABC0144",
)
