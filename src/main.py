"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list[dict], k: int = 5) -> None:
    """Print top-k recommendations for a single profile in a readable layout."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n=== {profile_name} ===")
    for idx, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{idx}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
        },
        # Adversarial / edge-case profiles for stress testing.
        "Conflicting: Chill + Very High Energy": {
            "genre": "ambient",
            "mood": "chill",
            "energy": 0.95,
        },
        "Genreless Energy-Only": {
            "genre": "",
            "mood": "",
            "energy": 0.75,
        },
    }

    for profile_name, user_prefs in profiles.items():
        print_recommendations(profile_name, user_prefs, songs, k=5)

    # Step 3 experiment: weight shift (energy x2, genre x0.5 of original 2.0 -> 1.0).
    baseline = {"genre": "pop", "mood": "happy", "energy": 0.90}
    weight_shift = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "weights": {"genre": 1.0, "mood": 1.0, "energy": 2.0},
    }

    print_recommendations("Experiment Baseline: Pop/Happy", baseline, songs, k=5)
    print_recommendations("Experiment Weight Shift: Genre 1.0, Mood 1.0, Energy 2.0", weight_shift, songs, k=5)


if __name__ == "__main__":
    main()
