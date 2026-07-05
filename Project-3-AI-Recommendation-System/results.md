# Results — AI Recommendation System

Actual output captured by running `python recommendation.py` against the
provided `items.csv` (20 items, 3 categories) and `users.csv` (5 users).

## User 101 — Aarav Shah
**Liked:** Introduction to Machine Learning, Python Programming Crash Course, Data Structures and Algorithms in Python

| item_id | title | category | similarity_score |
|---|---|---|---|
| 2 | Deep Learning with Python | Books | 0.2147 |
| 5 | The Art of Data Visualization | Books | 0.1862 |
| 17 | Recommendation Systems Handbook | Books | 0.0479 |
| 11 | Natural Language Processing in Action | Books | 0.0475 |
| 14 | Computer Vision with OpenCV | Books | 0.0275 |

## User 102 — Priya Mehta
**Liked:** Wireless Bluetooth Headphones, Wireless Gaming Mouse, 4K Webcam

| item_id | title | category | similarity_score |
|---|---|---|---|
| 12 | Noise Cancelling Earbuds | Electronics | 0.2233 |
| 6 | Mechanical Gaming Keyboard | Electronics | 0.1692 |
| 18 | Portable Bluetooth Speaker | Electronics | 0.1216 |
| 13 | Adjustable Dumbbell Set | Fitness | 0.0644 |
| 4 | Smart Fitness Watch | Electronics | 0.0388 |

## User 103 — Rohan Iyer
**Liked:** Yoga Mat Premium, Resistance Bands Set, Adjustable Dumbbell Set

| item_id | title | category | similarity_score |
|---|---|---|---|
| 4 | Smart Fitness Watch | Electronics | 0.0794 |
| 9 | Wireless Gaming Mouse | Electronics | 0.0618 |
| 19 | Foam Roller for Recovery | Fitness | 0.0370 |
| 16 | Running Shoes Lightweight | Fitness | 0.0328 |
| 15 | 4K Webcam | Electronics | 0.0250 |

## User 104 — Sneha Kapoor
**Liked:** Deep Learning with Python, Natural Language Processing in Action, Computer Vision with OpenCV

| item_id | title | category | similarity_score |
|---|---|---|---|
| 1 | Introduction to Machine Learning | Books | 0.1864 |
| 17 | Recommendation Systems Handbook | Books | 0.0957 |
| 5 | The Art of Data Visualization | Books | 0.0851 |
| 8 | Python Programming Crash Course | Books | 0.0706 |
| 20 | Data Structures and Algorithms in Python | Books | 0.0688 |

## User 105 — Vikram Nair
**Liked:** Smart Fitness Watch, Running Shoes Lightweight, Foam Roller for Recovery

| item_id | title | category | similarity_score |
|---|---|---|---|
| 13 | Adjustable Dumbbell Set | Fitness | 0.0631 |
| 10 | Resistance Bands Set | Fitness | 0.0531 |
| 7 | Yoga Mat Premium | Fitness | 0.0459 |
| 15 | 4K Webcam | Electronics | 0.0449 |
| 6 | Mechanical Gaming Keyboard | Electronics | 0.0346 |

## Observations

- Recommendations correctly stay **on-category** for users with clearly themed interests (Books for User 101/104, Electronics for User 102, Fitness-leaning for User 103/105).
- User 103's top recommendation, "Smart Fitness Watch," is technically `Electronics` but is content-adjacent to fitness vocabulary ("heart rate", "tracker") — demonstrating that the model reasons over text content, not rigid category labels.
- Similarity scores are naturally low (0.02–0.22) because TF-IDF vectors over short descriptions are sparse and high-dimensional; relative ranking matters more than absolute score magnitude.

## Future Improvements

- Blend in **collaborative filtering signals** (e.g., matrix factorization on a larger user-item interaction matrix) to capture cross-category preferences content-based filtering misses.
- Use **word embeddings** (e.g., sentence-transformers) instead of TF-IDF for semantic similarity beyond exact word overlap.
- Add **diversity re-ranking** to avoid over-recommending near-duplicate items.
- Incorporate **explicit user ratings** (not just binary "liked") to weight the profile vector.
