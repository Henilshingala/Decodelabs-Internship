# Test Cases — AI Recommendation System

| # | Test | Input | Expected Behavior |
|---|---|---|---|
| 1 | Basic recommendation for a books-focused user | `liked_item_ids=[1,8,20]` (ML/Python books) | Top recommendations are other `Books` category items |
| 2 | Basic recommendation for an electronics-focused user | `liked_item_ids=[3,9,15]` | Top recommendations are other `Electronics` items |
| 3 | Already-liked items excluded | Any user's liked list | None of the returned recommendations have an `item_id` present in `liked_item_ids` |
| 4 | Similarity scores sorted descending | Any call to `recommend_for_user` | `similarity_score` column is monotonically non-increasing |
| 5 | `top_n` respected | `top_n=3` | Exactly 3 rows returned (assuming enough unseen items exist) |
| 6 | Item-to-item similarity | `similar_items(item_id=1)` | Returns books conceptually close to "Introduction to Machine Learning" (e.g., Deep Learning, Data Viz) |
| 7 | Invalid item ID | `similar_items(item_id=9999)` | Raises `ValueError` |
| 8 | Empty liked list | `recommend_for_user([])` | Raises `ValueError` |
| 9 | Missing items file | Construct `ContentBasedRecommender(items_path=Path("missing.csv"))` | Raises `FileNotFoundError` |
| 10 | Malformed items file (missing required column) | items.csv lacking `description` column | Raises `KeyError` |

## Sample pytest Suite

```python
import pytest
from pathlib import Path
from recommendation import ContentBasedRecommender

@pytest.fixture(scope="module")
def engine():
    return ContentBasedRecommender()

def test_recommendations_exclude_liked_items(engine):
    liked = [1, 8, 20]
    recs = engine.recommend_for_user(liked, top_n=5)
    assert not set(recs["item_id"]).intersection(liked)

def test_scores_sorted_descending(engine):
    recs = engine.recommend_for_user([3, 9, 15], top_n=5)
    scores = recs["similarity_score"].tolist()
    assert scores == sorted(scores, reverse=True)

def test_top_n_respected(engine):
    recs = engine.recommend_for_user([7, 10, 13], top_n=3)
    assert len(recs) == 3

def test_invalid_item_id_raises(engine):
    with pytest.raises(ValueError):
        engine.similar_items(item_id=9999)

def test_empty_liked_list_raises(engine):
    with pytest.raises(ValueError):
        engine.recommend_for_user([])

def test_missing_items_file_raises():
    with pytest.raises(FileNotFoundError):
        ContentBasedRecommender(items_path=Path("does_not_exist.csv"))
```

Run with:
```bash
pip install pytest
pytest test_recommendation.py -v
```
