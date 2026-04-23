"""Command line runner for the Music Recommender Simulation."""

from src.agents.router import route_query
from src.reasoning.output import format_recommendation_output, unclear_query_message
from src.recommender import load_songs, recommend_songs


def _build_user_preferences_from_query(user_query: str) -> dict:
    """Build simple preferences from query text with safe defaults."""
    text = user_query.lower()

    genre = "pop"
    if "rock" in text:
        genre = "rock"
    elif "lofi" in text:
        genre = "lofi"

    mood = "happy"
    if "chill" in text:
        mood = "chill"
    elif "intense" in text:
        mood = "intense"

    energy = 0.8
    if "low energy" in text or "calm" in text:
        energy = 0.4
    elif "high energy" in text:
        energy = 0.9

    return {
        "genre": genre,
        "mood": mood,
        "energy": energy,
    }


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_query = input("What would you like? ").strip()
    route = route_query(user_query)

    if route == "unknown":
        print(unclear_query_message())
        return

    user_prefs = _build_user_preferences_from_query(user_query)
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print(format_recommendation_output(recommendations))


if __name__ == "__main__":
    main()
