"""
Semantic search using sentence-transformers embeddings.
Converts song metadata and user queries into dense vectors for similarity ranking.
"""

from typing import Dict, List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Wrapper around sentence-transformers for encoding songs and queries.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: HuggingFace model ID (default is small and fast).
        """
        self.model = SentenceTransformer(model_name)
        self.embedding_cache: Dict[str, np.ndarray] = {}
    
    def encode_query(self, user_query: str) -> np.ndarray:
        """
        Encode a user query into an embedding vector.
        
        Args:
            user_query: Natural language request from user.
        
        Returns:
            1D embedding vector (numpy array).
        """
        return self.model.encode(user_query, convert_to_numpy=True)
    
    def encode_song(self, song: Dict) -> np.ndarray:
        """
        Encode a song into an embedding vector using its metadata.
        
        Args:
            song: Dictionary with keys like title, artist, genre, mood, detailed_mood_tags.
        
        Returns:
            1D embedding vector (numpy array).
        """
        # Create a text description of the song
        title = song.get("title", "")
        artist = song.get("artist", "")
        genre = song.get("genre", "")
        mood = song.get("mood", "")
        tags = song.get("detailed_mood_tags", "")
        
        song_text = f"{title} by {artist}. Genre: {genre}. Mood: {mood}. Tags: {tags}."
        return self.model.encode(song_text, convert_to_numpy=True)
    
    def compute_similarity(self, query_embedding: np.ndarray, song_embedding: np.ndarray) -> float:
        """
        Compute cosine similarity between query and song embeddings.
        
        Args:
            query_embedding: Query vector.
            song_embedding: Song vector.
        
        Returns:
            Similarity score in range [0, 1].
        """
        # Cosine similarity
        dot_product = np.dot(query_embedding, song_embedding)
        norm_query = np.linalg.norm(query_embedding)
        norm_song = np.linalg.norm(song_embedding)
        
        if norm_query == 0 or norm_song == 0:
            return 0.0
        
        similarity = dot_product / (norm_query * norm_song)
        # Shift from [-1, 1] to [0, 1]
        return (similarity + 1) / 2
