import os
import sys
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Validate basic dependencies
try:
    import cv2
    import numpy as np
    import pytesseract
except ImportError as e:
    logger.error(f"Missing required dependency: {e.name}. Please run 'pip install -r requirements.txt'")
    sys.exit(1)

# Check Tesseract installation
def find_tesseract():
    tess_path = shutil.which("tesseract")
    if tess_path:
        return tess_path
    
    # Common Windows locations
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe")
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None

tesseract_cmd = find_tesseract()
if not tesseract_cmd:
    logger.error("Tesseract OCR engine not found.")
    logger.error("Please install Tesseract OCR:")
    logger.error("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    logger.error("  Ubuntu:  sudo apt install tesseract-ocr")
    logger.error("  macOS:   brew install tesseract")
    sys.exit(1)

pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

IMAGES_DIR = Path(__file__).parent / "images"
OUTPUT_IMAGES_DIR = Path(__file__).parent / "outputs"


def load_image(image_path: Path) -> np.ndarray:
    if not image_path.exists():
        logger.error(f"Image not found: {image_path}")
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        logger.error(f"OpenCV could not decode image: {image_path}")
        raise ValueError(f"OpenCV could not decode image: {image_path}")
    return image


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (3, 3), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def extract_text(preprocessed_image: np.ndarray, lang: str = "eng") -> str:
    try:
        raw_text = pytesseract.image_to_string(preprocessed_image, lang=lang)
    except Exception as e:
        logger.error(f"OCR Extraction failed: {e}")
        raise
    return raw_text.strip()


def draw_text_boxes(image: np.ndarray, lang: str = "eng") -> np.ndarray:
    annotated = image.copy()
    try:
        data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
        for i, word in enumerate(data["text"]):
            if word.strip() == "":
                continue
            x, y, w, h = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 200, 0), 2)
    except Exception as e:
        logger.warning(f"Could not draw text boxes: {e}")
    return annotated


def run_ocr_on_image(image_path: Path, output_dir: Path = OUTPUT_IMAGES_DIR) -> str:
    logger.info(f"Processing: {image_path.name}")
    image = load_image(image_path)
    preprocessed = preprocess_for_ocr(image)
    extracted_text = extract_text(preprocessed)
    annotated = draw_text_boxes(image)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"ocr_{image_path.name}"
    cv2.imwrite(str(output_path), annotated)
    logger.info(f"Annotated OCR image saved to: {output_path}")

    return extracted_text


def main() -> None:
    logger.info("Environment validation successful for OCR.")
    
    if not IMAGES_DIR.exists():
        logger.error(f"Images directory not found: {IMAGES_DIR}. Please provide images to process.")
        sys.exit(1)

    image_paths = sorted(p for p in IMAGES_DIR.glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    if not image_paths:
        logger.info(f"No images found in {IMAGES_DIR}.")
        return

    for image_path in image_paths:
        try:
            text = run_ocr_on_image(image_path)
            logger.info("Extracted Text:")
            print(text if text else "(no text detected)")
        except Exception as e:
            logger.error(f"Failed to process {image_path.name}")

if __name__ == "__main__":
    main()
