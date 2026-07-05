# Project 4 — Image & Text Recognition (OCR + Object Detection)

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green?logo=opencv)
![Status](https://img.shields.io/badge/Status-Complete-success)

## Overview

A robust, production-ready computer vision project combining two complementary pipelines:

1. **Optical Character Recognition (OCR)** — extracts text from images using OpenCV preprocessing and `pytesseract`.
2. **Object Detection** — detects and localizes objects in images using OpenCV's DNN module with a MobileNet SSD model.

This project is designed to be fully portable and reproducible on any machine. It handles missing models, missing executables, and dependencies gracefully.

## Features

- **Robust OCR Pipeline:** Grayscale, blur, and Otsu's thresholding to maximize text recognition accuracy.
- **Deep Learning Object Detection:** OpenCV DNN with MobileNet SSD.
- **Automated Setup:** Includes scripts to download models and create virtual environments automatically.
- **Production-Ready Error Handling:** Clear logging and user-friendly error messages instead of long tracebacks.
- **Cross-Platform:** Works on Windows, Linux, and macOS.

## Requirements

- Python 3.12+
- **Tesseract OCR Engine** (must be installed on your system)
- Internet connection (to download model weights)

## Installation

### 1. Download/Clone the Repository

Ensure you have downloaded this project folder onto your local machine.

### 2. Automated Setup (Windows)

For Windows users, we have provided an automated setup script.

1. Open PowerShell or Command Prompt.
2. Navigate to this project folder.
3. Run the setup script:
   - Command Prompt: `setup.bat`
   - PowerShell: `.\setup.ps1`

This script will automatically:
- Create and activate a Python virtual environment.
- Install all required Python packages.
- Download the required MobileNet SSD model files into the `models/` folder.

### 3. Manual Setup (macOS / Linux)

If you are not on Windows or prefer to install manually:

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the model files
python download_models.py
```

### 4. Install Tesseract OCR (CRITICAL)

The `ocr.py` script requires the Tesseract engine to be installed on your operating system.

- **Windows:** Download the installer from [UB-Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki) and run it. The scripts are configured to automatically find it in default installation paths.
- **macOS:** `brew install tesseract`
- **Linux (Ubuntu):** `sudo apt install tesseract-ocr`

## Usage

Ensure your virtual environment is activated before running the scripts!

### Running Object Detection

```bash
python object_detection.py
```
This script will:
- Check for the MobileNet SSD models in the `models/` directory.
- Load images from the `images/` directory.
- Perform object detection.
- Save annotated images to the `outputs/` directory.

### Running OCR

```bash
python ocr.py
```
This script will:
- Check if Tesseract OCR is installed.
- Preprocess images from the `images/` directory.
- Extract text and draw bounding boxes.
- Save annotated images to the `outputs/` directory and print the extracted text.

## Folder Structure

```
Project-4-Image-Text-Recognition/
├── images/                   # Place input images here
├── outputs/                  # Annotated images are saved here
├── models/                   # Downloaded model files go here
├── object_detection.py       # Main object detection script
├── ocr.py                    # Main OCR script
├── download_models.py        # Utility script to download large models
├── requirements.txt          # Python dependencies
├── setup.bat                 # Windows CMD automated setup
├── setup.ps1                 # Windows PowerShell automated setup
└── README.md                 # Project documentation
```

## Troubleshooting

- **`Missing required dependency: cv2`**: You forgot to activate your virtual environment or install dependencies. Run `pip install -r requirements.txt`.
- **`MobileNet SSD model files not found`**: You need to download the models. Run `python download_models.py`.
- **`Tesseract OCR engine not found`**: Tesseract is not installed on your system. Follow the instructions in Step 4 of Installation.
- **Image Not Found**: Ensure you have images placed in the `images/` directory. Supported formats are `.png`, `.jpg`, `.jpeg`.

## Expected Output

```
2026-07-06 12:00:00 - INFO - Processing: sample_text.png
2026-07-06 12:00:01 - INFO - Annotated OCR image saved to: outputs\ocr_sample_text.png
2026-07-06 12:00:01 - INFO - Extracted Text:
DecodeLabs Al Portfolio 202
```

## Screenshots

> Add screenshots of `outputs/ocr_sample_text.png` and `outputs/detected_sample_scene.png` here.
