# MobileNet SSD Model Files

This folder is intentionally empty in the repository (pre-trained weight
files are large binary artifacts and are not committed to source control).

Download the two required files into this folder before running
`object_detection.py` in full deep-learning mode:

1. `MobileNetSSD_deploy.prototxt` (network architecture definition)
2. `MobileNetSSD_deploy.caffemodel` (pre-trained weights, ~23 MB)

Both files are widely mirrored in public OpenCV/MobileNet-SSD demo
repositories. Search for "MobileNetSSD_deploy.prototxt" and
"MobileNetSSD_deploy.caffemodel" and place both files directly inside this
`models/` folder.

If these files are not present, `object_detection.py` automatically falls
back to a classical OpenCV contour/edge-based detector so the script always
runs end-to-end, clearly logging that it is in fallback mode.
