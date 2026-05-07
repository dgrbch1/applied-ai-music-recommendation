"""
Tests for semantic embeddings and similarity scoring.
"""

import pytest
import numpy as np
from src.retrieval.embeddings import EmbeddingModel


def test_embedding_model_initialization():
    """EmbeddingModel should initialize without errors."""
    model = EmbeddingModel()
    assert model is not None
    assert model.model is not None


def test_encode_query():
    """Query encoding should return a numpy array."""
    model = EmbeddingModel()
    query = "chill lofi songs"
    embedding = model.encode_query(query)
    
    assert isinstance(embedding, np.ndarray)
    assert len(embedding) > 0


def test_encode_song():
    """Song encoding should return a numpy array."""
    model = EmbeddingModel()
    song = {
        "title": "Test Song",
        "artist": "Test Artist",
        "genre": "lofi",
        "mood": "chill",
        "detailed_mood_tags": "relaxing, peaceful",
    }
    embedding = model.encode_song(song)
    
    assert isinstance(embedding, np.ndarray)
    assert len(embedding) > 0


def test_similarity_same_query():
    """Similarity of a query with itself should be close to 1.0."""
    model = EmbeddingModel()
    query = "chill songs"
    query_emb = model.encode_query(query)
    
    similarity = model.compute_similarity(query_emb, query_emb)
    assert similarity > 0.99


def test_similarity_different_queries():
    """Similarity between different queries should be lower."""
    model = EmbeddingModel()
    query1 = "chill lofi songs"
    query2 = "loud rock music"
    
    emb1 = model.encode_query(query1)
    emb2 = model.encode_query(query2)
    
    sim_same = model.compute_similarity(emb1, emb1)
    sim_different = model.compute_similarity(emb1, emb2)
    
    assert sim_same > sim_different


def test_similarity_range():
    """Similarity should always be in [0, 1]."""
    model = EmbeddingModel()
    query1 = "happy upbeat"
    query2 = "sad slow"
    
    emb1 = model.encode_query(query1)
    emb2 = model.encode_query(query2)
    
    similarity = model.compute_similarity(emb1, emb2)
    assert 0.0 <= similarity <= 1.0


def test_semantic_alignment():
    """Semantically similar queries should have higher similarity."""
    model = EmbeddingModel()
    
    # Similar queries
    chill1 = "recommend chill songs"
    chill2 = "i want relaxing music"
    
    # Different queries
    chill = "chill music"
    rock = "heavy metal rock"
    
    chill1_emb = model.encode_query(chill1)
    chill2_emb = model.encode_query(chill2)
    chill_emb = model.encode_query(chill)
    rock_emb = model.encode_query(rock)
    
    sim_chill_pair = model.compute_similarity(chill1_emb, chill2_emb)
    sim_chill_rock = model.compute_similarity(chill_emb, rock_emb)
    
    # Similar queries should have higher similarity than dissimilar
    assert sim_chill_pair > sim_chill_rock
