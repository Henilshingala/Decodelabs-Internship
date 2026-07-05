# Results — Image & Text Recognition

## OCR Results (`ocr.py`)

Run against two sample images in `sample_images/`:

| Image | Extracted Text | Notes |
|---|---|---|
| `sample_text.png` (rendered text "DecodeLabs AI Portfolio 2026") | `DecodeLabs Al Portfolio 202` | Near-perfect extraction; Tesseract misread "AI" as "Al" (capital I vs lowercase L — a very common OCR ambiguity) and truncated the trailing "6" |
| `sample_scene.jpg` (synthetic shapes, no text) | *(no text detected)* | Correct behavior — the image contains no text, and OCR correctly returns an empty result rather than hallucinating text |

Annotated images with green bounding boxes around every detected word are
saved to `output_images/ocr_sample_text.png` and
`output_images/ocr_sample_scene.png`.

### Why the Minor Misread Happened

OCR engines like Tesseract frequently confuse visually similar glyphs —
capital "I" and lowercase "l" are nearly identical in many sans-serif fonts.
This is a well-documented OCR limitation rather than a bug in the
pipeline, and is one reason production OCR systems often apply a
post-processing spell-check/dictionary-correction step.

## Object Detection Results (`object_detection.py`)

Because the MobileNet SSD `.caffemodel` weights file (~23 MB) is not bundled
in this repository (see `models/README.md`), running `object_detection.py`
without first downloading the weights automatically engages the **classical
contour-based fallback detector**:

```
[Notice] MobileNet SSD model files not found...
Falling back to classical contour-based detection for this demo run.

Processing: sample_scene.jpg
  Saved annotated image to: output_images/detected_sample_scene.png

Processing: sample_text.png
  Saved annotated image to: output_images/detected_sample_text.png
```

On `sample_scene.jpg` (which contains two rectangles and a circle), the
Canny-edge + contour fallback correctly draws bounding boxes around all
three synthetic shapes, since their high-contrast edges against the plain
background are easily detected by classical edge detection.

### Expected Output With MobileNet SSD Weights Installed

Once `MobileNetSSD_deploy.prototxt` and `MobileNetSSD_deploy.caffemodel`
are placed in `models/` (see setup instructions in the root README and
`models/README.md`), running the script on a real photograph containing
people, vehicles, or animals would print detections such as:

```
Processing: street_photo.jpg
  -> person (94.2%) at (120, 60, 310, 420)
  -> car (88.7%) at (400, 220, 620, 400)
  Saved annotated image to: output_images/detected_street_photo.png
```

## Conclusion

Both pipelines run end-to-end successfully on the bundled sample images,
correctly handle the "no text present" and "no model weights present"
edge cases, and produce annotated output images suitable for portfolio
screenshots.
