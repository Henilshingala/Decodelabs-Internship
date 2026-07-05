"""
recommendation.py
------------------
Content-Based Recommendation Engine using TF-IDF vectorization and
Cosine Similarity to recommend items based on user preference history.

Author: AI Engineering Portfolio
Python Version: 3.12+
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ITEMS_PATH = Path(__file__).parent / "items.csv"
USERS_PATH = Path(__file__).parent / "users.csv"
TOP_N_DEFAULT = 5


class ContentBasedRecommender:
    """A content-based recommendation engine.

    Workflow:
      1. Build a combined text representation of each item (title + category + description).
      2. Vectorize all item texts using TF-IDF.
      3. Compute pairwise cosine similarity between every pair of items.
      4. For a given user, build a "user profile vector" by averaging the
         TF-IDF vectors of the items they liked.
      5. Rank all unseen items by cosine similarity to the user profile vector.
    """

    def __init__(self, items_path: Path = ITEMS_PATH) -> None:
        self.items_path = items_path
        self.items_df: pd.DataFrame = self._load_items(items_path)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.items_df["combined_text"]
        )
        self.item_similarity = cosine_similarity(self.tfidf_matrix)

    @staticmethod
    def _load_items(items_path: Path) -> pd.DataFrame:
        """Load and prepare the item catalog.

        Args:
            items_path: Path to the items CSV file.

        Returns:
            A DataFrame with an added 'combined_text' column used for TF-IDF.

        Raises:
            FileNotFoundError: If the items file does not exist.
        """
        if not items_path.exists():
            raise FileNotFoundError(f"Items file not found: {items_path}")

        dataframe = pd.read_csv(items_path)
        required_columns = {"item_id", "title", "category", "description"}
        missing = required_columns - set(dataframe.columns)
        if missing:
            raise KeyError(f"items.csv is missing required columns: {missing}")

        dataframe["combined_text"] = (
            dataframe["title"].fillna("")
            + " "
            + dataframe["category"].fillna("")
            + " "
            + dataframe["description"].fillna("")
        )
        return dataframe.reset_index(drop=True)

    def _item_index(self, item_id: int) -> int:
        """Return the DataFrame row index for a given item_id."""
        matches = self.items_df.index[self.items_df["item_id"] == item_id]
        if len(matches) == 0:
            raise ValueError(f"Item ID {item_id} not found in catalog.")
        return int(matches[0])

    def similar_items(self, item_id: int, top_n: int = TOP_N_DEFAULT) -> pd.DataFrame:
        """Find the most similar items to a given item (item-to-item recommendations).

        Args:
            item_id: The reference item's ID.
            top_n: Number of similar items to return.

        Returns:
            A DataFrame of the top_n most similar items with similarity scores.
        """
        idx = self._item_index(item_id)
        similarity_scores = list(enumerate(self.item_similarity[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        # Skip index 0 result if it is the item itself
        similarity_scores = [s for s in similarity_scores if s[0] != idx][:top_n]

        result_rows = []
        for row_idx, score in similarity_scores:
            row = self.items_df.iloc[row_idx]
            result_rows.append(
                {
                    "item_id": row["item_id"],
                    "title": row["title"],
                    "category": row["category"],
                    "similarity_score": round(float(score), 4),
                }
            )
        return pd.DataFrame(result_rows)

    def _build_user_profile_vector(self, liked_item_ids: List[int]) -> np.ndarray:
        """Average the TF-IDF vectors of a user's liked items into one profile vector.

        Args:
            liked_item_ids: List of item IDs the user has liked.

        Returns:
            A 1D numpy array representing the user's content preference profile.
        """
        indices = [self._item_index(item_id) for item_id in liked_item_ids]
        liked_vectors = self.tfidf_matrix[indices]
        profile_vector = np.asarray(liked_vectors.mean(axis=0))
        return profile_vector

    def recommend_for_user(
        self, liked_item_ids: List[int], top_n: int = TOP_N_DEFAULT
    ) -> pd.DataFrame:
        """Generate top-N recommendations for a user based on their liked items.

        Args:
            liked_item_ids: List of item IDs the user has previously liked.
            top_n: Number of recommendations to return.

        Returns:
            A ranked DataFrame of recommended items with similarity scores,
            excluding items the user has already liked.

        Raises:
            ValueError: If liked_item_ids is empty.
        """
        if not liked_item_ids:
            raise ValueError("liked_item_ids must contain at least one item ID.")

        profile_vector = self._build_user_profile_vector(liked_item_ids)
        scores = cosine_similarity(profile_vector, self.tfidf_matrix).flatten()

        ranked_indices = np.argsort(scores)[::-1]

        recommendations = []
        for idx in ranked_indices:
            item_row = self.items_df.iloc[idx]
            if int(item_row["item_id"]) in liked_item_ids:
                continue  # Do not recommend items the user already liked
            recommendations.append(
                {
                    "item_id": item_row["item_id"],
                    "title": item_row["title"],
                    "category": item_row["category"],
                    "similarity_score": round(float(scores[idx]), 4),
                }
            )
            if len(recommendations) >= top_n:
                break

        return pd.DataFrame(recommendations)


def load_users(users_path: Path = USERS_PATH) -> pd.DataFrame:
    """Load the users CSV and parse liked_item_ids into a list of ints.

    Args:
        users_path: Path to users.csv.

    Returns:
        A DataFrame with an added 'liked_items_list' column.
    """
    if not users_path.exists():
        raise FileNotFoundError(f"Users file not found: {users_path}")

    users_df = pd.read_csv(users_path)
    users_df["liked_items_list"] = users_df["liked_item_ids"].apply(
        lambda cell: [int(item.strip()) for item in str(cell).split(",")]
    )
    return users_df


def main() -> None:
    """Demonstrate the recommendation engine for every user in users.csv."""
    engine = ContentBasedRecommender()
    users_df = load_users()

    for _, user_row in users_df.iterrows():
        print(f"\n=== Recommendations for {user_row['user_name']} (user_id={user_row['user_id']}) ===")
        liked_titles = engine.items_df[
            engine.items_df["item_id"].isin(user_row["liked_items_list"])
        ]["title"].tolist()
        print(f"Liked items: {liked_titles}")

        recommendations = engine.recommend_for_user(user_row["liked_items_list"], top_n=5)
        print(recommendations.to_string(index=False))


if __name__ == "__main__":
    main()
