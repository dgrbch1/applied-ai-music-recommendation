from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _energy_closeness(song_energy: float, target_energy: float) -> float:
        return max(0.0, 1.0 - abs(song_energy - target_energy))

    @staticmethod
    def _acoustic_bonus(song_acousticness: float, likes_acoustic: bool) -> float:
        if likes_acoustic:
            return 1.0 if song_acousticness >= 0.6 else 0.0
        return 1.0 if song_acousticness <= 0.5 else 0.0

    def _score_song(self, user: UserProfile, song: Song) -> float:
        genre_match = 1.0 if song.genre == user.favorite_genre else 0.0
        mood_match = 1.0 if song.mood == user.favorite_mood else 0.0
        energy_closeness = self._energy_closeness(song.energy, user.target_energy)

        return (
            2.0 * genre_match
            + 1.0 * mood_match
            + 1.0 * energy_closeness
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = sorted(
            self.songs,
            key=lambda song: self._score_song(user, song),
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre matches")
        if song.mood == user.favorite_mood:
            reasons.append("mood matches")

        energy_gap = abs(song.energy - user.target_energy)
        reasons.append(f"energy is close (difference {energy_gap:.2f})")

        return f"{song.title} recommended because " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV into typed dictionaries with numeric conversions."""
    songs: List[Dict] = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def _closeness(value: float, target: float) -> float:
    """Return similarity in [0, 1] based on distance between value and target."""
    return max(0.0, 1.0 - abs(value - target))

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons for the score."""
    reasons: List[str] = []

    weights = user_prefs.get("weights", {})
    genre_weight = float(weights.get("genre", 2.0))
    mood_weight = float(weights.get("mood", 1.0))
    energy_weight = float(weights.get("energy", 1.0))
    tempo_weight = float(weights.get("tempo", 0.0))
    use_mood = bool(user_prefs.get("use_mood", True))

    genre_match = 1.0 if song["genre"] == user_prefs.get("genre") else 0.0
    mood_match = 1.0 if use_mood and song["mood"] == user_prefs.get("mood") else 0.0
    energy_similarity = _closeness(song["energy"], user_prefs.get("energy", 0.5))

    score = genre_weight * genre_match + mood_weight * mood_match + energy_weight * energy_similarity

    target_tempo = user_prefs.get("tempo_bpm")
    if target_tempo is not None and tempo_weight > 0.0:
        tempo_tolerance = float(user_prefs.get("tempo_tolerance", 60.0))
        tempo_similarity = max(0.0, 1.0 - abs(song["tempo_bpm"] - float(target_tempo)) / tempo_tolerance)
        score += tempo_weight * tempo_similarity
    else:
        tempo_similarity = None

    if genre_match:
        reasons.append(f"genre match (+{genre_weight:.1f})")
    if mood_match:
        reasons.append(f"mood match (+{mood_weight:.1f})")
    reasons.append(f"energy similarity (+{energy_similarity * energy_weight:.2f})")
    if tempo_similarity is not None:
        reasons.append(f"tempo similarity (+{tempo_similarity * tempo_weight:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Rank all songs by score and return the top-k with explanation reasons."""
    scored_results: List[Tuple[Dict, float, List[str]]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_results.append((song, score, reasons))

    # In-place sort keeps memory usage small for this simple CLI pipeline.
    scored_results.sort(key=lambda item: item[1], reverse=True)

    if not user_prefs.get("diversity_by_genre", False):
        return scored_results[:k]

    diverse_results: List[Tuple[Dict, float, List[str]]] = []
    seen_genres = set()
    selected_ids = set()

    for item in scored_results:
        song, _, reasons = item
        if song["genre"] not in seen_genres:
            diverse_results.append((song, item[1], reasons + ["diversity boost (new genre)"]))
            seen_genres.add(song["genre"])
            selected_ids.add(song["id"])
        if len(diverse_results) >= k:
            return diverse_results[:k]

    for item in scored_results:
        if item[0]["id"] not in selected_ids:
            diverse_results.append(item)
            selected_ids.add(item[0]["id"])
        if len(diverse_results) >= k:
            break

    return diverse_results[:k]
