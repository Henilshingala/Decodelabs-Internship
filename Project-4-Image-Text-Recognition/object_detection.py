import sys
import logging
from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Validate basic dependencies
try:
    import cv2
    import numpy as np
except ImportError as e:
    logger.error(f"Missing required dependency: {e.name}. Please run 'pip install -r requirements.txt'")
    sys.exit(1)

MODEL_DIR = Path(__file__).parent / "models"
PROTOTXT_PATH = MODEL_DIR / "MobileNetSSD_deploy.prototxt"
WEIGHTS_PATH = MODEL_DIR / "MobileNetSSD_deploy.caffemodel"
IMAGES_DIR = Path(__file__).parent / "images"
OUTPUTS_DIR = Path(__file__).parent / "outputs"

CONFIDENCE_THRESHOLD = 0.4

VOC_CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
    "car", "cat", "chair", "cow", "diningtable", "dog", "horse",
    "motorbike", "person", "pottedplant", "sheep", "sofa", "train",
    "tvmonitor",
]

np.random.seed(42)
CLASS_COLORS = np.random.randint(0, 255, size=(len(VOC_CLASSES), 3), dtype=np.uint8)


class MobileNetSSDDetector:
    def __init__(self, prototxt_path: Path = PROTOTXT_PATH, weights_path: Path = WEIGHTS_PATH) -> None:
        if not prototxt_path.exists() or not weights_path.exists():
            logger.error("MobileNet SSD model files not found.")
            logger.error("Please run: python download_models.py")
            sys.exit(1)
        
        try:
            self.net = cv2.dnn.readNetFromCaffe(str(prototxt_path), str(weights_path))
        except Exception as e:
            logger.error(f"Failed to load the model: {e}")
            logger.error("The model files might be corrupted. Try deleting the 'models' folder and running 'python download_models.py' again.")
            sys.exit(1)

    def detect(self, image: np.ndarray, confidence_threshold: float = CONFIDENCE_THRESHOLD) -> List[Tuple[str, float, Tuple[int, int, int, int]]]:
        height, width = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        results = []
        for i in range(detections.shape[2]):
            confidence = float(detections[0, 0, i, 2])
            if confidence < confidence_threshold:
                continue

            class_id = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            x1, y1, x2, y2 = box.astype("int")
            class_name = VOC_CLASSES[class_id] if class_id < len(VOC_CLASSES) else "unknown"
            results.append((class_name, confidence, (x1, y1, x2, y2)))

        return results


def draw_detections(image: np.ndarray, detections: List[Tuple[str, float, Tuple[int, int, int, int]]]) -> np.ndarray:
    annotated = image.copy()
    for class_name, confidence, (x1, y1, x2, y2) in detections:
        class_id = VOC_CLASSES.index(class_name) if class_name in VOC_CLASSES else 0
        color = tuple(int(c) for c in CLASS_COLORS[class_id])
        label = f"{class_name}: {confidence * 100:.1f}%"
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated, label, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return annotated


def main() -> None:
    logger.info("Environment validation successful for Object Detection.")

    if not IMAGES_DIR.exists():
        logger.error(f"Images directory not found: {IMAGES_DIR}. Please provide images to process.")
        sys.exit(1)

    image_paths = sorted(p for p in IMAGES_DIR.glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    if not image_paths:
        logger.info(f"No images found in {IMAGES_DIR}.")
        return

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    detector = MobileNetSSDDetector()

    for image_path in image_paths:
        logger.info(f"Processing: {image_path.name}")
        image = cv2.imread(str(image_path))
        if image is None:
            logger.error(f"Skipped (could not read image): {image_path.name}")
            continue

        try:
            detections = detector.detect(image)
            annotated = draw_detections(image, detections)
            for class_name, confidence, bbox in detections:
                logger.info(f"  -> {class_name} ({confidence * 100:.1f}%) at {bbox}")

            output_path = OUTPUTS_DIR / f"detected_{image_path.name}"
            cv2.imwrite(str(output_path), annotated)
            logger.info(f"Saved annotated image to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to process {image_path.name}: {e}")

if __name__ == "__main__":
    main()
