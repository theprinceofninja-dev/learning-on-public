#!/bin/bash

echo "Setting up Banknote Serial Number Extractor"
echo "==========================================="

# Update system
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Python
echo "Installing Python and pip..."
sudo apt install python3 python3-pip python3-venv -y

# Install Tesseract OCR
echo "Installing Tesseract OCR..."
sudo apt install tesseract-ocr libtesseract-dev tesseract-ocr-eng -y

# Install OpenCV dependencies
echo "Installing OpenCV dependencies..."
sudo apt install python3-opencv libgl1-mesa-glx -y

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install opencv-python pillow pytesseract numpy

echo "==========================================="
echo "Setup complete!"
echo ""
echo "To use the extractor:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the extractor:"
echo "   python extract_serial.py your_image.jpg"
echo ""
echo "3. For visualization:"
echo "   python extract_serial.py your_image.jpg --visualize"