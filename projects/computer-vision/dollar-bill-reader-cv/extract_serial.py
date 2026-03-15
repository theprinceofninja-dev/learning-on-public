import argparse
import os
import re

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from PIL import Image

# Set Tesseract path for Linux (usually already in PATH)
# If Tesseract is not found, uncomment and update the path below:
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import cv2
        import pytesseract
        from PIL import Image

        print("✓ All dependencies are installed correctly")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install missing packages using:")
        print("pip install opencv-python pillow pytesseract numpy")
        return False


def preprocess_image(image_path):
    """
    Preprocess the image to enhance text regions
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image from {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Apply morphological operations to enhance text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Noise removal
    denoised = cv2.medianBlur(morphed, 3)

    return img, denoised


def find_serial_number_region(image):
    """
    Find potential regions containing serial numbers
    """
    # Use contour detection to find text regions
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Filter based on aspect ratio and size
        aspect_ratio = w / h if h > 0 else 0

        # Typical serial number characteristics
        if (
            w > 50
            and h > 20  # Minimum size for serial numbers
            and 2 < aspect_ratio < 8  # Wide rectangles
            and w < image.shape[1] * 0.4
        ):  # Not too wide
            regions.append((x, y, w, h))

    # Sort regions by position
    regions.sort(key=lambda r: (r[1], r[0]))

    return regions


def extract_text_from_region(region_img):
    """Extract text from a region using optimized OCR settings"""
    # Convert to PIL Image
    region_pil = Image.fromarray(cv2.cvtColor(region_img, cv2.COLOR_BGR2RGB))

    # Multiple OCR configurations for better accuracy
    configs = [
        r"--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        r"--oem 3 --psm 8",
        r"--oem 3 --psm 6",
    ]

    best_text = ""
    for config in configs:
        text = pytesseract.image_to_string(region_pil, config=config).strip()
        if len(text) > len(best_text) and is_valid_serial_number(text):
            best_text = text

    return best_text


def is_valid_serial_number(text):
    """
    Validate if the extracted text resembles a US dollar serial number
    """
    if not text:
        return False

    # Remove spaces and special characters
    text = re.sub(r"[^A-Z0-9]", "", text.upper())

    if len(text) < 8 or len(text) > 11:
        return False

    # Must contain both letters and numbers
    has_letter = any(c.isalpha() for c in text)
    has_digit = any(c.isdigit() for c in text)

    if not (has_letter and has_digit):
        return False

    # Check common patterns
    patterns = [
        r"^[A-Z]{1,2}\d{6,8}[A-Z]?$",  # Common US serial format
        r"^\d{8,9}$",  # Older bills might be all numbers
        r"^[A-Z]\d{7,9}[A-Z]?$",
    ]

    for pattern in patterns:
        if re.match(pattern, text):
            return True

    return False


def visualize_preprocessing_steps(image_path):
    """
    Visualize different preprocessing steps in subplots
    """
    # Read the original image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Apply morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Apply median blur for noise removal
    denoised = cv2.medianBlur(morphed, 3)

    # Apply Canny edge detection
    edges = cv2.Canny(denoised, 50, 150)

    # Create subplots
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle("Image Preprocessing Steps", fontsize=16, fontweight="bold")

    # Plot images
    images = [
        ("Original", img_rgb),
        ("Grayscale", gray),
        ("Blurred", blurred),
        ("Adaptive Threshold", thresh),
        ("Morphological Ops", morphed),
        ("Denoised", denoised),
        ("Edges", edges),
        ("Contours", draw_contours(img.copy(), denoised)),
    ]

    for idx, (title, image) in enumerate(images):
        row = idx // 4
        col = idx % 4
        ax = axes[row, col]

        if len(image.shape) == 2:  # Grayscale images
            ax.imshow(image, cmap="gray")
        else:
            ax.imshow(image)

        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.axis("off")

    plt.tight_layout()
    plt.show()

    # Also show intermediate steps in a compact way
    fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
    fig2.suptitle("Key Processing Steps", fontsize=14, fontweight="bold")

    # Show original, processed, and regions
    axes2[0].imshow(img_rgb)
    axes2[0].set_title("Original Image", fontweight="bold")
    axes2[0].axis("off")

    axes2[1].imshow(denoised, cmap="gray")
    axes2[1].set_title("Final Processed", fontweight="bold")
    axes2[1].axis("off")

    # Show with contours
    contour_img = draw_contours(img.copy(), denoised)
    axes2[2].imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
    axes2[2].set_title("Detected Contours", fontweight="bold")
    axes2[2].axis("off")

    plt.tight_layout()
    plt.show()


def draw_contours(img, processed_img):
    """
    Draw contours on the image for visualization
    """
    # Find contours
    contours, _ = cv2.findContours(
        processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw all contours
    contour_img = img.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

    # Draw bounding boxes for potential serial number regions
    regions = find_serial_number_region(processed_img)
    for x, y, w, h in regions:
        cv2.rectangle(contour_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return contour_img


def extract_serial_number(image_path, visualize=False):
    """
    Main function to extract serial number from dollar banknote image
    """
    print(f"Processing image: {image_path}")

    try:
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found!")
            return []

        # Preprocess image
        original, processed = preprocess_image(image_path)

        # Show preprocessed images in subplots if requested
        visualize_preprocessing_steps(image_path)

        # Find potential serial number regions
        regions = find_serial_number_region(processed)

        print(f"Found {len(regions)} potential text regions")

        serial_numbers = []

        # OCR each region
        for i, (x, y, w, h) in enumerate(regions, 1):
            # Extract region with padding
            padding = 10
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(original.shape[1], x + w + padding)
            y2 = min(original.shape[0], y + h + padding)

            region_img = original[y1:y2, x1:x2]

            # Extract text from region
            text = extract_text_from_region(region_img)

            if text and is_valid_serial_number(text):
                print(f"Region {i}: Found serial number: {text}")
                serial_numbers.append(
                    {"text": text, "bbox": (x1, y1, x2, y2), "region": i}
                )

        # If no valid serial numbers found, try full image OCR
        if not serial_numbers:
            print("No serial numbers found in regions. Trying full image OCR...")
            full_image_pil = Image.fromarray(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
            full_text = pytesseract.image_to_string(full_image_pil)

            # Search for serial number patterns
            pattern = r"[A-Z]{1,2}\d{6,8}[A-Z]?|\b[A-Z0-9]{8,11}\b"
            matches = re.findall(pattern, full_text, re.IGNORECASE)

            for match in matches:
                match = match.upper().strip()
                if is_valid_serial_number(match):
                    serial_numbers.append(
                        {"text": match, "bbox": None, "region": "full_scan"}
                    )
                    print(f"Full scan found: {match}")

        # Visualize results if requested
        if visualize and serial_numbers:
            visualize_results(original, serial_numbers)

        return serial_numbers

    except Exception as e:
        print(f"Error processing image: {e}")
        import traceback

        traceback.print_exc()
        return []


def visualize_results(image, results):
    """Visualize the detected serial numbers on the image"""
    display_img = image.copy()

    for result in results:
        if result["bbox"]:
            x1, y1, x2, y2 = result["bbox"]
            # Draw rectangle
            cv2.rectangle(display_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Add text
            cv2.putText(
                display_img,
                result["text"],
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

    # Display
    cv2.imshow("Detected Serial Numbers", display_img)
    print("\nPress any key to close the image window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the result
    output_path = "result_with_serial.jpg"
    cv2.imwrite(output_path, display_img)
    print(f"Result saved to: {output_path}")


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Extract serial numbers from US dollar banknotes"
    )
    parser.add_argument("image", help="Path to the banknote image")
    parser.add_argument(
        "--visualize", "-v", action="store_true", help="Visualize the results"
    )
    parser.add_argument("--test", action="store_true", help="Test dependencies")

    args = parser.parse_args()

    if args.test:
        check_dependencies()
        return

    # Check dependencies
    if not check_dependencies():
        return

    # Extract serial numbers
    serial_numbers = extract_serial_number(args.image, args.visualize)

    # Print results
    print("\n" + "=" * 50)
    if serial_numbers:
        print("EXTRACTION RESULTS:")
        print("=" * 50)
        for i, sn in enumerate(serial_numbers, 1):
            print(f"Serial Number {i}: {sn['text']}")
            if sn["bbox"]:
                print(f"  Location: Region {sn['region']}")
        print("=" * 50)
    else:
        print("No serial numbers detected.")
        print("\nTroubleshooting tips:")
        print("1. Ensure the image is clear and well-lit")
        print("2. Make sure the serial number is visible")
        print("3. Try different image angles")
        print("4. Try cropping the image to focus on the serial number area")


if __name__ == "__main__":
    main()
