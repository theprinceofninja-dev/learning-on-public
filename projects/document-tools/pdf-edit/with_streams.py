import re
import zlib

import pdfrw


def replace_text_in_pdf_streams(input_pdf_path, output_pdf_path, old_text, new_text):
    """
    Replace text in PDF content streams using pdfrw.
    This works for text embedded in the page content, not just form fields.
    """

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    replacements_made = 0

    # Process each page
    for page_num, page in enumerate(template_pdf.pages):
        print(f"\n--- Processing Page {page_num + 1} ---")

        # Get the page contents
        if page.Contents:
            contents = page.Contents
            if not isinstance(contents, list):
                contents = [contents]

            for i, content_obj in enumerate(contents):
                # Check if we have a stream to work with
                if not hasattr(content_obj, "stream"):
                    print(f"Content stream {i+1}: No stream attribute")
                    continue

                content = content_obj.stream

                # Check if content is bytes or string
                if isinstance(content, bytes):
                    # Check if stream is compressed
                    if hasattr(content_obj, "Filter"):
                        # Try to decompress if needed
                        try:
                            if "/FlateDecode" in content_obj.Filter or (
                                isinstance(content_obj.Filter, list)
                                and "/FlateDecode" in content_obj.Filter
                            ):
                                try:
                                    content = zlib.decompress(content)
                                except:
                                    pass  # Might not actually be compressed
                            content_str = content.decode("latin-1", errors="ignore")
                        except Exception as e:
                            print(f"Error decoding stream: {e}")
                            content_str = content.decode("latin-1", errors="ignore")
                    else:
                        content_str = content.decode("latin-1", errors="ignore")
                else:
                    # Already a string
                    content_str = str(content)

                print(f"Content stream {i+1} length: {len(content_str)} chars")
                print(f"Sample (first 300 chars): {content_str[:300]}")

                # Check if our text is in the content
                if old_text in content_str:
                    # Replace text in the content stream
                    new_content_str = content_str.replace(old_text, new_text)
                    replacements_made += 1
                    print(
                        f"✓ Replaced '{old_text}' with '{new_text}' in content stream"
                    )

                    # Convert back to bytes
                    new_content_bytes = new_content_str.encode("latin-1")

                    # Recompress if it was compressed before
                    if hasattr(content_obj, "Filter"):
                        if "/FlateDecode" in content_obj.Filter or (
                            isinstance(content_obj.Filter, list)
                            and "/FlateDecode" in content_obj.Filter
                        ):
                            new_content_bytes = zlib.compress(new_content_bytes)

                    # Update the stream
                    content_obj.stream = new_content_bytes
                    content_obj.Length = len(new_content_bytes)
                else:
                    # Try alternative approach: look for text in PDF operators
                    print(f"Text '{old_text}' not found directly in content stream")

                    # Try to find text in PDF text showing operators
                    modified_content = replace_text_in_pdf_operators(
                        content_str, old_text, new_text
                    )
                    if modified_content != content_str:
                        new_content_bytes = modified_content.encode("latin-1")

                        # Recompress if needed
                        if hasattr(content_obj, "Filter"):
                            if "/FlateDecode" in content_obj.Filter or (
                                isinstance(content_obj.Filter, list)
                                and "/FlateDecode" in content_obj.Filter
                            ):
                                new_content_bytes = zlib.compress(new_content_bytes)

                        content_obj.stream = new_content_bytes
                        content_obj.Length = len(new_content_bytes)
                        replacements_made += 1
                        print(f"✓ Found and replaced text in PDF operators")

        # Also check for text in annotations if any exist
        if hasattr(page, "Annots") and page.Annots:
            print(f"Found annotations on page {page_num + 1}")
            for annot in page.Annots:
                if hasattr(annot, "Contents"):
                    contents = annot.Contents
                    if old_text in str(contents):
                        new_contents = str(contents).replace(old_text, new_text)
                        annot.Contents = pdfrw.objects.pdfstring.PdfString.encode(
                            new_contents
                        )
                        replacements_made += 1
                        print(f"✓ Replaced text in annotation")

    if replacements_made > 0:
        # Save the modified PDF
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
        print(f"\n✅ Successfully made {replacements_made} replacements")
        print(f"PDF saved to: {output_pdf_path}")
    else:
        print(f"\n❌ No replacements made. Text '{old_text}' not found in PDF.")
        print("Possible reasons:")
        print("1. Text might be encoded differently in the PDF")
        print("2. Text might be part of an image")
        print("3. Text might use custom font encoding")


def replace_text_in_pdf_operators(content_str, old_text, new_text):
    """
    Attempt to replace text within PDF text showing operators (TJ/Tj).
    This is more accurate for PDF content streams.
    """

    # PDF text operators: Tj shows a string, TJ shows an array
    # Patterns to match text showing operators

    # For Tj operator: (text) Tj
    tj_pattern = r"\(([^)]*)\)\s+Tj"

    def replace_in_tj(match):
        text = match.group(1)
        # Unescape PDF strings
        text = text.replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\")
        if old_text in text:
            new_text_modified = text.replace(old_text, new_text)
            # Re-escape for PDF
            new_text_modified = new_text_modified.replace("(", r"\(").replace(
                ")", r"\)"
            )
            return f"({new_text_modified}) Tj"
        return match.group(0)

    # Apply replacement to Tj operators
    modified_content = re.sub(tj_pattern, replace_in_tj, content_str)

    # For TJ operator: [ ... (text) ... ] TJ
    # This is more complex as it involves arrays
    tj_array_pattern = r"\[(.*?)\]\s*TJ"

    def replace_in_tj_array(match):
        array_content = match.group(1)
        # Split by parentheses but keep them
        parts = re.split(r"(\([^)]*\))", array_content)

        for i, part in enumerate(parts):
            if part.startswith("(") and part.endswith(")"):
                text = part[1:-1]  # Remove parentheses
                # Unescape
                text = (
                    text.replace(r"\\(", "(")
                    .replace(r"\\)", ")")
                    .replace(r"\\\\", "\\")
                )
                if old_text in text:
                    new_text_modified = text.replace(old_text, new_text)
                    # Re-escape
                    new_text_modified = new_text_modified.replace("(", r"\(").replace(
                        ")", r"\)"
                    )
                    parts[i] = f"({new_text_modified})"

        return "[" + "".join(parts) + "] TJ"

    # Apply replacement to TJ arrays
    modified_content = re.sub(
        tj_array_pattern, replace_in_tj_array, modified_content, flags=re.DOTALL
    )

    return modified_content


def search_text_in_pdf(input_pdf_path, search_text):
    """
    Helper function to search for text in PDF and see how it's encoded.
    """

    template_pdf = pdfrw.PdfReader(input_pdf_path)

    print(f"\n=== Searching for '{search_text}' in PDF ===")

    for page_num, page in enumerate(template_pdf.pages):
        if page.Contents:
            contents = page.Contents
            if not isinstance(contents, list):
                contents = [contents]

            for i, content_obj in enumerate(contents):
                if hasattr(content_obj, "stream"):
                    content = content_obj.stream

                    # Convert to string
                    if isinstance(content, bytes):
                        if hasattr(content_obj, "Filter"):
                            try:
                                if "/FlateDecode" in content_obj.Filter or (
                                    isinstance(content_obj.Filter, list)
                                    and "/FlateDecode" in content_obj.Filter
                                ):
                                    try:
                                        content = zlib.decompress(content)
                                    except:
                                        pass
                            except:
                                pass
                        content_str = content.decode("latin-1", errors="ignore")
                    else:
                        content_str = str(content)

                    # Search for the text
                    if search_text in content_str:
                        print(f"\n✓ Found on Page {page_num+1}, Content stream {i+1}")
                        # Show context around the found text
                        idx = content_str.find(search_text)
                        start = max(0, idx - 50)
                        end = min(len(content_str), idx + len(search_text) + 50)
                        print(f"Context: ...{content_str[start:end]}...")

                        # Also show how it appears in PDF operators
                        # Look for Tj or TJ operators around the found text
                        lines = content_str.split("\n")
                        for line_num, line in enumerate(lines):
                            if search_text in line:
                                print(f"Line {line_num}: {line}")

                    # Also search in PDF operators format
                    tj_pattern = r"\(([^)]*)\)\s+Tj"
                    for match in re.finditer(tj_pattern, content_str):
                        text_in_operator = match.group(1)
                        # Unescape
                        text_in_operator = text_in_operator.replace(
                            r"\\(", "("
                        ).replace(r"\\)", ")")
                        if search_text in text_in_operator:
                            print(f"\n✓ Found in Tj operator on Page {page_num+1}:")
                            print(f"  PDF format: ({match.group(1)}) Tj")
                            print(f"  Decoded text: {text_in_operator}")


# Usage
if __name__ == "__main__":
    input_pdf = "/home/*******/Downloads/FCH Test_AUG_22.pdf"
    output_pdf = "/home/*******/Downloads/output.pdf"
    old_text = "SYR01OMNNT05"
    new_text = "XYZ01ABC0144"

    # First, search for the text to understand how it's encoded
    search_text_in_pdf(input_pdf, old_text)

    # Then try to replace it
    replace_text_in_pdf_streams(input_pdf, output_pdf, old_text, new_text)
