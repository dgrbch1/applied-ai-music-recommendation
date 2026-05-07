"""
Hybrid ranker combines semantic similarity with rule-based scoring.
"""

from typing import Dict, List, Tuple
import numpy as np
from src.retrieval.embeddings import EmbeddingModel


def hybrid_score(
    user_query: str,
    song: Dict,
    rule_score: float,
    embedding_model: EmbeddingModel,
    semantic_weight: float = 0.4,
    rule_weight: float = 0.6,
) -> float:
    """
    Combine semantic similarity score with rule-based score.
    
    Args:
        user_query: User's natural language request.
        song: Song dictionary with metadata.
        rule_score: Score from traditional rule-based ranking (0 to ~4).
        embedding_model: EmbeddingModel instance for computing similarity.
        semantic_weight: Weight for semantic similarity (default 0.4).
        rule_weight: Weight for rule-based score (default 0.6).
    
    Returns:
        Combined score as a float.
    """
    # Encode query and song
    query_embedding = embedding_model.encode_query(user_query)
    song_embedding = embedding_model.encode_song(song)
    
    # Compute semantic similarity (0 to 1)
    semantic_similarity = embedding_model.compute_similarity(query_embedding, song_embedding)
    
    # Normalize rule score to [0, 1] range (assuming max rule score is ~4)
    normalized_rule_score = min(rule_score / 4.0, 1.0)
    
    # Combine
    combined = semantic_weight * semantic_similarity + rule_weight * normalized_rule_score
    
    return combined


def rank_with_hybrid(
    user_query: str,
    songs: List[Dict],
    rule_scores: List[Tuple[float, List[str]]],
    embedding_model: EmbeddingModel,
    semantic_weight: float = 0.4,
    rule_weight: float = 0.6,
) -> List[Tuple[Dict, float, List[str]]]:
    """
    Rank songs using hybrid scoring.
    
    Args:
        user_query: User's request.
        songs: List of song dictionaries.
        rule_scores: List of (score, reasons) from traditional ranker.
        embedding_model: EmbeddingModel instance.
        semantic_weight: Weight for semantic component.
        rule_weight: Weight for rule-based component.
    
    Returns:
        List of (song, combined_score, reasons) sorted by combined_score descending.
    """
    results = []
    
    for song, (rule_score, reasons) in zip(songs, rule_scores):
        combined = hybrid_score(
            user_query,
            song,
            rule_score,
            embedding_model,
            semantic_weight,
            rule_weight,
        )
        results.append((song, combined, reasons))
    
    # Sort by combined score descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results
