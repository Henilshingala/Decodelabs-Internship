# Project 3 — AI Recommendation System

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?logo=scikitlearn)
![Status](https://img.shields.io/badge/Status-Complete-success)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

A **content-based recommendation engine** that suggests catalog items to
users by analyzing item descriptions with **TF-IDF** and ranking candidates
via **cosine similarity** to a user's preference profile.

## Objectives

- Build a working content-based recommender from raw CSV catalog/user data.
- Demonstrate TF-IDF vectorization and cosine similarity for text-based item matching.
- Generate ranked Top-N recommendations per user, excluding already-liked items.
- Provide item-to-item "similar items" lookups in addition to per-user recommendations.

## Problem Statement

Given a catalog of items (`items.csv`) and a record of what each user has
liked (`users.csv`), recommend new items each user is likely to be
interested in — without relying on a large user-interaction matrix
(suitable for small/medium catalogs and the classic "cold start" scenario).

## Theory

See [`recommendation_logic.md`](recommendation_logic.md) for the full
mathematical and conceptual breakdown of TF-IDF and cosine similarity. In
brief:

- **TF-IDF** converts each item's text into a sparse vector that emphasizes distinctive vocabulary.
- **Cosine similarity** measures the angle between two vectors, giving a 0–1 score of content closeness independent of text length.
- A **user profile vector** is the average of the TF-IDF vectors of everything that user has liked.

## Architecture & Workflow

```mermaid
flowchart LR
    A[items.csv] --> B[Combine title+category+description]
    B --> C[TF-IDF Vectorizer]
    C --> D[Item-Item Similarity Matrix]
    E[users.csv] --> F[Liked item IDs]
    F --> G[Average TF-IDF vectors -> User Profile Vector]
    G --> H[Cosine Similarity vs all items]
    D -.used for item-to-item lookups.-> H
    H --> I[Sort, exclude liked items]
    I --> J[Top-N Recommendations]
```

```
Project-3-AI-Recommendation-System/
├── recommendation.py          # ContentBasedRecommender engine + CLI demo
├── items.csv                  # 20-item catalog (Books / Electronics / Fitness)
├── users.csv                  # 5 sample users with liked item IDs
├── requirements.txt
├── recommendation_logic.md
├── test_cases.md
├── results.md
└── screenshots/
```

## Implementation & Code Explanation

| Component | Description |
|---|---|
| `ContentBasedRecommender.__init__` | Loads items, builds combined text, fits TF-IDF, precomputes item-item similarity matrix |
| `similar_items()` | Item-to-item recommendations (e.g., "customers who liked X also liked...") |
| `_build_user_profile_vector()` | Averages TF-IDF vectors of a user's liked items into one profile vector |
| `recommend_for_user()` | Ranks all items by similarity to the user profile, excluding already-liked items, returns Top-N |
| `load_users()` | Parses the comma-separated `liked_item_ids` column into a Python list of ints |

## Execution Steps

```bash
cd Project-3-AI-Recommendation-System

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

python recommendation.py
```

## Expected Output (excerpt)

```
=== Recommendations for Aarav Shah (user_id=101) ===
Liked items: ['Introduction to Machine Learning', 'Python Programming Crash Course', 'Data Structures and Algorithms in Python']
 item_id                            title category  similarity_score
       2          Deep Learning with Python    Books            0.2147
       5      The Art of Data Visualization    Books            0.1862
      17    Recommendation Systems Handbook    Books            0.0479
      11 Natural Language Processing in Action Books          0.0475
      14        Computer Vision with OpenCV    Books            0.0275
```

Full output for all 5 users is captured in [`results.md`](results.md).

## Screenshots

> Add console screenshots of recommendation output for each user to `screenshots/`.

## Applications

- E-commerce "Recommended for You" sections
- Streaming platform content recommendations (movies, articles, courses)
- Job/candidate matching based on profile text
- Library/learning-platform "Similar reading" features

## Advantages

- Works immediately for new items with no interaction history (no item cold-start)
- Explainable — recommendations trace back to shared content/vocabulary
- No need to maintain a large user-item ratings matrix

## Limitations

- Cannot recommend outside a user's established content interests (no serendipity/cross-category discovery)
- Relies entirely on the quality of item text descriptions
- TF-IDF only captures lexical overlap, not deeper semantic meaning (e.g., "car" vs "automobile" are unrelated to TF-IDF)

## Future Improvements

- Hybridize with collaborative filtering for cross-category discovery
- Replace TF-IDF with semantic embeddings (e.g., Sentence-BERT) for true meaning-based similarity
- Add diversity-aware re-ranking to avoid near-duplicate recommendations
- Incorporate explicit ratings/weights instead of binary "liked" signals

## Interview Questions

1. **What is the difference between content-based and collaborative filtering?**
   Content-based filtering recommends based on item attributes/content matched to a user's own preference profile. Collaborative filtering recommends based on patterns across many users' behavior (e.g., "users similar to you also liked..."), requiring a larger interaction dataset.

2. **Why use cosine similarity instead of Euclidean distance for text vectors?**
   Cosine similarity measures the angle between vectors, making it insensitive to vector magnitude (i.e., document length) — important for TF-IDF vectors, which vary in length depending on description length.

3. **How is a user profile vector constructed in this project?**
   By averaging the TF-IDF vectors of every item the user has previously liked, producing a single vector representing the user's aggregate content preference.

4. **What's a major weakness of TF-IDF-based similarity?**
   It only captures exact lexical overlap and ignores semantic relationships between different words with similar meaning, unlike embedding-based approaches.

5. **How would you handle a brand-new user with no liked items (cold start)?**
   Fall back to popularity-based or category-based recommendations until the user has interacted with enough items to build a meaningful profile vector.

## Conclusion

This project implements a complete, explainable content-based recommendation
engine — from raw CSV catalog and user data through TF-IDF vectorization,
user profile construction, and Top-N ranked recommendations — demonstrating
a foundational technique used throughout real-world recommender systems.
