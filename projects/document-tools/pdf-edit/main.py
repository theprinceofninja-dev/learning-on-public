import re

import pdfrw


def replace_text_in_pdf_pdfrw(input_pdf_path, output_pdf_path, old_text, new_text):
    """
    Replace text in PDF form fields using pdfrw.
    This works well for PDFs with form fields but not for regular text in pages.
    """

    template_pdf = pdfrw.PdfReader(input_pdf_path)

    # Search through all form fields (annotations)
    for page in template_pdf.pages:
        print(page)
        if page.get("/Annots"):
            for annotation in page["/Annots"]:
                print(annotation)
                if annotation["/Subtype"] == "/Widget" and annotation.get("/TU"):
                    # Get the field value
                    field_value = annotation["/TU"]
                    print(field_value)
                    if isinstance(field_value, pdfrw.objects.pdfstring.PdfString):
                        field_str = field_value.decode("utf-8", errors="ignore")
                        print(field_str)
                        if old_text in field_str:
                            # Replace text in the field
                            new_field_str = field_str.replace(old_text, new_text)
                            annotation.update(pdfrw.PdfDict(TU=new_field_str))
        else:
            print("No annots")

    # Save the modified PDF
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
    print(f"PDF form fields processed and saved to {output_pdf_path}")


# Usage
replace_text_in_pdf_pdfrw(
    "/home/*******/Downloads/FCH Test_AUG_22.pdf",
    "/home/*******/Downloads/output.pdf",
    "SYR01OMNNT05",
    "XYZ01ABC0144",
)
