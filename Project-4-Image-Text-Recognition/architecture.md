# Architecture — Image & Text Recognition

This project contains two independent computer-vision pipelines that share
the same `sample_images/` input folder and `output_images/` output folder.

## Pipeline 1: OCR (`ocr.py`)

```
load_image()
     │  (cv2.imread)
     ▼
preprocess_for_ocr()
     │  grayscale -> Gaussian blur -> Otsu threshold
     ▼
extract_text()
     │  pytesseract.image_to_string()
     ▼
draw_text_boxes()
     │  pytesseract.image_to_data() -> per-word bounding boxes
     ▼
output_images/ocr_<name>.png  (annotated)
+ extracted text printed to console
```

### Why Otsu Thresholding?

Otsu's method automatically computes the optimal binary threshold value by
minimizing intra-class variance between foreground (text) and background
pixels. This removes the need to manually tune a fixed threshold across
images with different lighting/contrast — improving OCR robustness on
real-world (non-studio) photos.

## Pipeline 2: Object Detection (`object_detection.py`)

```
MobileNetSSDDetector.__init__()
     │  cv2.dnn.readNetFromCaffe(prototxt, weights)
     ▼
detect(image)
     │  cv2.dnn.blobFromImage() -> resize to 300x300, normalize
     │  net.forward() -> raw detection tensor
     │  filter by CONFIDENCE_THRESHOLD (0.4)
     ▼
draw_detections()
     │  draw class-colored bounding boxes + confidence labels
     ▼
output_images/detected_<name>.png  (annotated)
```

If the MobileNet SSD `.prototxt`/`.caffemodel` files are not present (see
`models/README.md`), the script automatically falls back to
`run_fallback_contour_detection()`, a classical Canny-edge + contour-based
region detector, clearly logging that fallback mode is active. This ensures
the script is always runnable end-to-end even without downloading the
~23 MB pre-trained weight file.

## MobileNet SSD Architecture (Conceptual)

MobileNet SSD combines two ideas:

1. **MobileNet** — a lightweight convolutional backbone using depthwise
   separable convolutions, dramatically reducing parameter count versus
   standard CNNs (e.g., VGG), making it suitable for real-time/edge inference.
2. **SSD (Single Shot MultiBox Detector)** — a detection head that predicts
   bounding boxes and class scores in a single forward pass at multiple
   feature-map scales, without a separate region-proposal stage (unlike
   R-CNN family detectors).

The combination produces a fast detector capable of running without a GPU,
trained here on the 20-class PASCAL VOC dataset (`VOC_CLASSES`).

## Shared Design Decisions

- Both scripts validate input file existence and raise clear, typed exceptions (`FileNotFoundError`, `ValueError`, `RuntimeError`) rather than failing silently.
- Both scripts write annotated output images to a shared `output_images/` directory with a consistent `<pipeline>_<original_stem>.png` naming convention.
- Both scripts can run standalone via `python ocr.py` / `python object_detection.py` and process every image found in `sample_images/`.
