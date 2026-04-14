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
    popularity: int = 50
    release_decade: int = 2010
    detailed_mood_tags: str = ""
    instrumentalness: float = 0.5
    speechiness: float = 0.1

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
                    "popularity": int(row.get("popularity", 50)),
                    "release_decade": int(row.get("release_decade", 2010)),
                    "detailed_mood_tags": row.get("detailed_mood_tags", ""),
                    "instrumentalness": float(row.get("instrumentalness", 0.5)),
                    "speechiness": float(row.get("speechiness", 0.1)),
                }
            )
    return songs


def _closeness(value: float, target: float) -> float:
    """Return similarity in [0, 1] based on distance between value and target."""
    return max(0.0, 1.0 - abs(value - target))


def _normalized_closeness(value: float, target: float, scale: float) -> float:
    """Return similarity in [0, 1] using a custom distance scale."""
    if scale <= 0:
        return 0.0
    return max(0.0, 1.0 - abs(value - target) / scale)


def _tag_overlap_score(song_tags_raw: str, preferred_tags: List[str]) -> float:
    """Return overlap ratio between preferred tags and song detailed mood tags."""
    if not preferred_tags:
        return 0.0

    song_tags = {tag.strip().lower() for tag in song_tags_raw.split("|") if tag.strip()}
    prefs = {tag.strip().lower() for tag in preferred_tags if tag.strip()}
    if not prefs:
        return 0.0

    overlap = len(song_tags.intersection(prefs))
    return overlap / len(prefs)

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons for the score."""
    reasons: List[str] = []

    weights = user_prefs.get("weights", {})
    genre_weight = float(weights.get("genre", 2.0))
    mood_weight = float(weights.get("mood", 1.0))
    energy_weight = float(weights.get("energy", 1.0))
    tempo_weight = float(weights.get("tempo", 0.0))
    popularity_weight = float(weights.get("popularity", 0.0))
    decade_weight = float(weights.get("decade", 0.0))
    tag_weight = float(weights.get("tag", 0.0))
    instrumentalness_weight = float(weights.get("instrumentalness", 0.0))
    speechiness_weight = float(weights.get("speechiness", 0.0))
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

    popularity_similarity = None
    if popularity_weight > 0.0:
        target_popularity = float(user_prefs.get("target_popularity", 50.0))
        popularity_similarity = _normalized_closeness(float(song.get("popularity", 50.0)), target_popularity, 100.0)
        score += popularity_weight * popularity_similarity

    decade_similarity = None
    if decade_weight > 0.0:
        target_decade = float(user_prefs.get("target_decade", 2010.0))
        decade_similarity = _normalized_closeness(float(song.get("release_decade", 2010.0)), target_decade, 40.0)
        score += decade_weight * decade_similarity

    tag_similarity = None
    if tag_weight > 0.0:
        preferred_tags = user_prefs.get("preferred_tags", [])
        tag_similarity = _tag_overlap_score(str(song.get("detailed_mood_tags", "")), preferred_tags)
        score += tag_weight * tag_similarity

    instrumentalness_similarity = None
    if instrumentalness_weight > 0.0:
        target_instrumentalness = float(user_prefs.get("target_instrumentalness", 0.5))
        instrumentalness_similarity = _closeness(float(song.get("instrumentalness", 0.5)), target_instrumentalness)
        score += instrumentalness_weight * instrumentalness_similarity

    speechiness_similarity = None
    if speechiness_weight > 0.0:
        target_speechiness = float(user_prefs.get("target_speechiness", 0.1))
        speechiness_similarity = _closeness(float(song.get("speechiness", 0.1)), target_speechiness)
        score += speechiness_weight * speechiness_similarity

    if genre_match:
        reasons.append(f"genre match (+{genre_weight:.1f})")
    if mood_match:
        reasons.append(f"mood match (+{mood_weight:.1f})")
    reasons.append(f"energy similarity (+{energy_similarity * energy_weight:.2f})")
    if tempo_similarity is not None:
        reasons.append(f"tempo similarity (+{tempo_similarity * tempo_weight:.2f})")
    if popularity_similarity is not None:
        reasons.append(f"popularity similarity (+{popularity_similarity * popularity_weight:.2f})")
    if decade_similarity is not None:
        reasons.append(f"release decade similarity (+{decade_similarity * decade_weight:.2f})")
    if tag_similarity is not None and tag_similarity > 0.0:
        reasons.append(f"detailed mood tags overlap (+{tag_similarity * tag_weight:.2f})")
    if instrumentalness_similarity is not None:
        reasons.append(f"instrumentalness similarity (+{instrumentalness_similarity * instrumentalness_weight:.2f})")
    if speechiness_similarity is not None:
        reasons.append(f"speechiness similarity (+{speechiness_similarity * speechiness_weight:.2f})")

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
