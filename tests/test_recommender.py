from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_song_returns_numeric_and_reasons():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120,
        "weights": {"tempo": 0.5},
    }
    song = {
        "id": 1,
        "title": "Test Pop Track",
        "artist": "Test Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120.0,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }

    score, reasons = score_song(user_prefs, song)
    assert isinstance(score, float)
    assert score > 0
    assert isinstance(reasons, list)
    assert any("genre match" in reason for reason in reasons)
    assert any("tempo similarity" in reason for reason in reasons)


def test_recommend_songs_diversity_by_genre_returns_varied_top_two():
    songs = [
        {
            "id": 1,
            "title": "Pop A",
            "artist": "Artist A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "tempo_bpm": 120.0,
            "valence": 0.8,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Pop B",
            "artist": "Artist B",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.88,
            "tempo_bpm": 122.0,
            "valence": 0.8,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 3,
            "title": "Rock A",
            "artist": "Artist C",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.87,
            "tempo_bpm": 130.0,
            "valence": 0.6,
            "danceability": 0.6,
            "acousticness": 0.1,
        },
    ]

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "diversity_by_genre": True,
    }

    recs = recommend_songs(user_prefs, songs, k=2)
    top_genres = {recs[0][0]["genre"], recs[1][0]["genre"]}
    assert len(top_genres) == 2
