# Recommendation Logic — Content-Based Filtering

## Approach: Content-Based Filtering with TF-IDF + Cosine Similarity

Unlike collaborative filtering (which needs many users' interaction
histories), content-based filtering recommends items by analyzing the
**content/attributes of items themselves** and matching them to a user's
demonstrated preferences. This works well even with a small user base ("cold
start" friendly).

## Step 1 — Build Item Text Representation

For every item in `items.csv`, `ContentBasedRecommender._load_items()`
concatenates `title + category + description` into a single `combined_text`
field. This text is the "content" the algorithm reasons about.

## Step 2 — TF-IDF Vectorization

`TfidfVectorizer(stop_words="english")` converts every item's `combined_text`
into a numeric vector where each dimension corresponds to a word in the
overall vocabulary. **TF-IDF (Term Frequency–Inverse Document Frequency)**
weighs words by:

- **Term Frequency (TF):** how often a word appears in an item's own description.
- **Inverse Document Frequency (IDF):** how rare that word is across *all* items.

Words that appear in nearly every item (e.g. generic catalog words) get a
low IDF weight, while distinctive words specific to fewer items (e.g.
"bluetooth", "yoga", "neural") get a higher weight — making the vector
representation focus on what makes each item *distinctive*.

## Step 3 — Item-Item Cosine Similarity

`cosine_similarity(self.tfidf_matrix)` computes the pairwise cosine
similarity between every pair of item vectors:

```
cosine_similarity(A, B) = (A · B) / (||A|| * ||B||)
```

This produces a value between 0 (completely dissimilar) and 1 (identical
content), independent of vector magnitude — which matters because items
have descriptions of different lengths.

## Step 4 — Building a User Profile Vector

`_build_user_profile_vector()` averages the TF-IDF vectors of all items a
user has liked. This produces a single vector that represents the user's
aggregate content preference — e.g., a user who liked several ML books ends
up with a profile vector weighted heavily toward ML/programming vocabulary.

## Step 5 — Ranking & Top-N Recommendation

`recommend_for_user()`:
1. Computes cosine similarity between the user's profile vector and every item vector.
2. Sorts items by similarity score, descending.
3. Filters out items the user has already liked.
4. Returns the top `N` remaining items.

## Why This Design?

- **No cold-start problem for new items**: as soon as an item has a
  description, it can be recommended — no interaction history needed.
- **Explainable**: recommendations can be traced back to shared vocabulary/category overlap.
- **Lightweight**: no need for a large user-item interaction matrix; scales naturally as new items are added (just re-fit the vectorizer).

## Limitation: No Serendipity

Because recommendations are driven purely by content similarity, the system
will never recommend something outside a user's established interest profile
(e.g., a fitness book to someone who has only liked electronics) — even if
collaborative signals from similar users might suggest it. This is the
classic content-based filtering trade-off, addressed in
[`results.md`](results.md) and the Future Improvements section of the README.
