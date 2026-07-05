# Artificial Intelligence Portfolio

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?logo=scikitlearn)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?logo=opencv&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-success)
![License](https://img.shields.io/badge/License-MIT-green)

> A four-project, production-quality Artificial Intelligence portfolio covering rule-based AI, classical machine learning, recommendation systems, and computer vision — built to demonstrate end-to-end AI engineering skills for internships, placements, and technical interviews.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Skills Demonstrated](#skills-demonstrated)
- [Technologies Used](#technologies-used)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Virtual Environment Setup](#virtual-environment-setup)
- [How to Run Each Project](#how-to-run-each-project)
- [Screenshots](#screenshots)
- [Features](#features)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Author](#author)
- [Conclusion](#conclusion)

---

## Project Overview

| # | Project | Core Technique | Folder |
|---|---|---|---|
| 1 | Rule-Based AI Chatbot | Dictionary-driven intent matching, IPO model | [`Project-1-Rule-Based-AI-Chatbot`](Project-1-Rule-Based-AI-Chatbot) |
| 2 | Data Classification Using AI | K-Nearest Neighbors (scikit-learn) | [`Project-2-Data-Classification`](Project-2-Data-Classification) |
| 3 | AI Recommendation System | TF-IDF + Cosine Similarity (content-based filtering) | [`Project-3-AI-Recommendation-System`](Project-3-AI-Recommendation-System) |
| 4 | Image / Text Recognition | OCR (Tesseract) + Object Detection (MobileNet SSD) | [`Project-4-Image-Text-Recognition`](Project-4-Image-Text-Recognition) |

Each project folder is fully self-contained with its own README, runnable
source code, requirements file, generated outputs, and supporting
documentation (architecture diagrams, test cases, evaluation reports, and
interview questions).

## Skills Demonstrated

- Python software engineering: clean functions, type hints, docstrings, error handling, modular design
- Classical AI: rule-based reasoning and dictionary-driven control flow
- Supervised machine learning: preprocessing, feature scaling, train/test methodology, model evaluation
- Information retrieval techniques: TF-IDF vectorization, cosine similarity, content-based recommendation
- Computer vision: image preprocessing, OCR, deep-learning object detection with graceful fallback design
- Technical documentation: architecture diagrams (Mermaid), structured READMEs, reproducible reports

## Technologies Used

| Category | Tools |
|---|---|
| Language | Python 3.12+ |
| ML / Data | scikit-learn, pandas, numpy |
| Visualization | matplotlib, seaborn |
| Computer Vision | OpenCV, pytesseract (Tesseract OCR), Pillow |
| Documentation | Markdown, Mermaid diagrams |

## Folder Structure

```
Artificial-Intelligence-Portfolio/
├── README.md
├── Project-1-Rule-Based-AI-Chatbot/
│   ├── README.md
│   ├── requirements.txt
│   ├── chatbot.py
│   ├── responses.py
│   ├── test_cases.md
│   ├── conversation_examples.md
│   ├── architecture.md
│   ├── flowchart.md
│   └── screenshots/
├── Project-2-Data-Classification/
│   ├── README.md
│   ├── requirements.txt
│   ├── classification.py
│   ├── dataset.csv
│   ├── model_training.md
│   ├── evaluation.md
│   ├── confusion_matrix.png
│   ├── accuracy_report.md
│   └── screenshots/
├── Project-3-AI-Recommendation-System/
│   ├── README.md
│   ├── requirements.txt
│   ├── recommendation.py
│   ├── items.csv
│   ├── users.csv
│   ├── recommendation_logic.md
│   ├── test_cases.md
│   ├── results.md
│   └── screenshots/
└── Project-4-Image-Text-Recognition/
    ├── README.md
    ├── requirements.txt
    ├── ocr.py
    ├── object_detection.py
    ├── sample_images/
    ├── output_images/
    ├── results.md
    ├── architecture.md
    ├── models/ (download instructions for MobileNet SSD weights)
    └── screenshots/
```

## Installation

Clone the repository and enter its root directory:

```bash
git clone https://github.com/<your-username>/Artificial-Intelligence-Portfolio.git
cd Artificial-Intelligence-Portfolio
```

Each project is independent and has its own `requirements.txt`. Install
dependencies per-project (recommended) rather than globally, since the
projects don't share a dependency set.

## Requirements

- Python 3.12 or later
- `pip` package manager
- (Project 4 only) the Tesseract OCR system binary installed separately from `pip` (see Project 4's README)

## Virtual Environment

It's strongly recommended to use a virtual environment per project:

```bash
cd Project-<N>-<Name>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

```bash
# Project 1 — Rule-Based AI Chatbot
cd Project-1-Rule-Based-AI-Chatbot && python chatbot.py

# Project 2 — Data Classification
cd Project-2-Data-Classification && python classification.py

# Project 3 — AI Recommendation System
cd Project-3-AI-Recommendation-System && python recommendation.py

# Project 4 — Image / Text Recognition
cd Project-4-Image-Text-Recognition
python ocr.py
python object_detection.py
```

## Screenshots

Each project folder contains a `screenshots/` directory. Add terminal
output captures and generated image results there as you run each project
locally — paths are already referenced from each project's README.

## Features

- Zero placeholder content — every script is complete and runnable
- Real, reproducible outputs (actual accuracy/confusion-matrix numbers, actual recommendation rankings, actual OCR text extraction) included directly in the documentation
- Consistent professional documentation structure across all four projects
- Defensive, production-style error handling (typed exceptions, input validation) throughout
- Graceful degradation design pattern demonstrated in Project 4 (object detection falls back to classical CV when deep-learning weights are absent)

## Learning Outcomes

Across these four projects, this portfolio demonstrates the ability to:

- Translate AI/ML theory (IPO model, KNN, TF-IDF, cosine similarity, CNN-based object detection) into clean, working Python code
- Structure ML pipelines with correct methodology (avoiding data leakage, proper train/test splitting, appropriate evaluation metrics)
- Write maintainable code using data/logic separation, dispatch patterns, and modular function design
- Produce professional technical documentation suitable for engineering teams and interviewers
- Anticipate and handle real-world failure modes (missing files, missing system dependencies, edge-case inputs)

## Future Improvements

- Add a unified Dockerfile/devcontainer so all four projects run in one consistent environment
- Add automated CI (GitHub Actions) running each project's test suite on every push
- Replace the rule-based chatbot's keyword matching with a small intent-classification ML model
- Hybridize the recommendation engine with collaborative filtering
- Add YOLOv8 as an alternative object detection backend for Project 4

## License

This project is licensed under the MIT License — see the `LICENSE` file (add one at the repository root) for details. You are free to use, modify, and distribute this code with attribution.

## Author

**AI Engineering Portfolio**
Built as a complete demonstration project covering rule-based systems, classical machine learning, recommendation systems, and computer vision — created for GitHub portfolio, resume, internship, and placement use.

## Conclusion

This repository brings together four distinct branches of Artificial
Intelligence — symbolic/rule-based reasoning, supervised machine learning,
information-retrieval-based recommendation, and computer vision — into a
single, cohesive, professionally documented portfolio. Every script is
complete and was actually executed to produce the metrics, recommendations,
and extracted text shown throughout the documentation, making this a
genuine, reproducible demonstration of applied AI engineering skill.
