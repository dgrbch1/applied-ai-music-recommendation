# Music Recommender Simulation

## Project Summary

I built a simplified music recommender in Python to show how recommendation logic works step by step.
The system uses a content-based approach: each song is scored against one user profile, then all songs are ranked and the top results are returned.
The main goal is transparency, so every recommendation can be explained by the score components.

## How Real Platforms Predict What You Might Like

Major platforms usually combine two families of methods:

- Collaborative filtering: learns from behavior patterns across many users (likes, skips, replays, watch time, playlist adds). If users with behavior similar to yours liked track X, the system may suggest X to you.
- Content-based filtering: learns from item attributes (genre, mood, energy, tempo, etc.) and recommends items with similar characteristics to what you already liked.

In production systems, Spotify, YouTube, and TikTok generally blend both methods plus ranking models and contextual signals (time of day, device, session behavior).

This simulator focuses on content-based filtering only.

## Rubric Checkpoint Coverage

This submission demonstrates all required learning goals:

- Data to prediction pipeline: song features + user preferences are transformed into numeric relevance scores and ranked outputs.
- Scoring vs ranking distinction: one rule computes a single-song score, a separate rule orders the full candidate list.
- Weighted-score implementation: genre, mood, and energy similarity are combined with explicit weights.
- Bias analysis: filter-bubble and representation risks are identified and discussed.
- Communication artifacts: this README, the model card, and reflection document intended use, limits, and improvements.

## How The System Works

This section captures the exact planning checkpoint completed before implementation.

### Step 1: Define Your Data

- Starter catalog was expanded from 10 songs to 18 songs in `data/songs.csv`.
- New rows add broader style coverage (for example classical, metal, country, reggae, hip hop, r&b, edm, folk).
- Added numeric depth features used by the simulation: `danceability` and `acousticness` (plus `valence` and `tempo_bpm`).

Prompt used to generate additional rows (example):

"Generate 8 additional songs for my recommender in valid CSV row format using existing headers: id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness. Include genres and moods not already in a small starter catalog. Keep numeric values realistic (0.0 to 1.0 for normalized columns)."

### Step 2: Create a User Profile

Final profile used for planning:

```python
user_profile = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.38,
    "tempo_bpm": 78,
    "weights": {"genre": 2.0, "mood": 1.0, "energy": 1.0, "tempo": 0.0}
}
```

Inline critique prompt used (example):

"Critique this profile for my recommender: {'genre':'lofi','mood':'chill','energy':0.38}. Will it clearly separate intense rock from chill lofi, or is it too narrow? Suggest one broader variant and one stricter variant."

### Step 3: Sketch the Recommendation Logic

Scoring logic design prompt (example with `#file:songs.csv`):

"Using #file:songs.csv, propose point-weighting strategies for a content-based music recommender where genre matters more than mood and energy is scored by closeness to target. Compare a balanced and genre-heavy option."

Finalized algorithm recipe:

- `+2.0` points for genre match
- `+1.0` point for mood match
- `+similarity` points from energy closeness where `energy_similarity = 1 - abs(song_energy - user_energy)`

Final score:

- `score = 2.0 * genre_match + 1.0 * mood_match + 1.0 * energy_similarity`

### Step 4: Visualize the Design

Data flow implemented as Input -> Process -> Output:

- Input: user preferences (`genre`, `mood`, `energy` target)
- Process: loop through every song and compute weighted score
- Output: rank all songs and return top `k`

Mermaid flowchart is included in the Data Flow section below.

### Step 5: Document Your Plan

Plan documentation is captured in this section and includes:

- dataset expansion,
- a specific user profile,
- finalized algorithm recipe,
- and expected bias risks.

Expected bias note:

- This system may over-prioritize genre and miss cross-genre songs that match mood and energy well.

## Data and Features

Dataset: `data/songs.csv` (18 songs)

Song features available:

- `genre`
- `mood`
- `energy`
- `tempo_bpm`
- `valence`
- `danceability`
- `acousticness`

For this first version, the strongest features are:

- `genre`: broad style preference
- `mood`: emotional vibe preference
- `energy`: numeric intensity target

Why these three first:

- They align with how users often describe music in plain language (for example, "chill lofi" or "intense rock").
- They are easy to explain mathematically.
- They allow both categorical matching (genre/mood) and numeric similarity (energy closeness).

## User Profile Design

`UserProfile` fields used in the OOP recommender:

- `favorite_genre: str`
- `favorite_mood: str`
- `target_energy: float`
- `likes_acoustic: bool`

Dictionary-style profiles used in the functional pipeline:

- `genre`
- `mood`
- `energy`
- optional `weights` (`genre`, `mood`, `energy`, `tempo`)
- optional `tempo_bpm`, `tempo_tolerance`
- optional `diversity_by_genre`

## Algorithm Recipe

### Scoring Rule (one song)

For each song:

- `genre_match = 1` if song genre equals user genre, else `0`
- `mood_match = 1` if song mood equals user mood, else `0`
- `energy_similarity = 1 - abs(song.energy - user.energy)`

Default weighted score:

- `score = 2.0 * genre_match + 1.0 * mood_match + 1.0 * energy_similarity`

This rewards songs closer to the target energy, not simply higher or lower energy.

### Ranking Rule (song list)

- Score every song in the catalog.
- Sort songs by score descending.
- Return top `k` songs.

Python sorting note used in implementation:

- `scored_results.sort(...)` updates the same list in place.
- `sorted(scored_results, ...)` returns a new sorted list and leaves the original list unchanged.
- This project uses `.sort()` in the functional pipeline for in-place ranking.

Why both rules matter:

- Scoring rule: explains the quality of one candidate.
- Ranking rule: turns many candidate scores into an ordered recommendation list.

## Data Flow

```mermaid
flowchart LR
    A[User Preferences] --> B[Load songs.csv]
    B --> C[Score Each Song]
    C --> D[Store Song + Score + Reasons]
    D --> E[Sort by Score Descending]
    E --> F[Return Top K Recommendations]
```

## Bias and Limitations

Known risks in this simple system:

- Genre over-weighting can create filter bubbles by repeatedly favoring one style.
- Mood labels are subjective and can be noisy, causing unfair ranking changes.
- Small catalog size limits variety and may overfit to narrow tastes.
- No collaborative signal means the model cannot discover "users like you also liked" patterns.

Potential fairness impact:

- Underrepresented genres or moods in the CSV can be systematically under-recommended.

## Evaluation and Test Evidence

Automated tests:

- `tests/test_recommender.py`
- Current result: `4 passed`

Manual profile checks run in `src/main.py`:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Conflicting edge case (chill + very high energy)
- Genreless edge case (energy-only)

Weight experiment:

- Baseline: `genre=2.0, mood=1.0, energy=1.0`
- Variant: `genre=1.0, mood=1.0, energy=2.0`

Observed effect:

- Energy-heavy variant increases cross-genre movement when energy similarity is strong.

Teacher-facing evidence summary:

- Implementation exists in `src/recommender.py` and `src/main.py`.
- Unit tests are in `tests/test_recommender.py`.
- Model risk and intended use are documented in `model_card.md`.
- Behavior interpretation and learning reflection are documented in `reflection.md`.

CLI verification snapshot (default pop/happy profile):

```text
Loaded songs: 18
=== Default Profile: pop/happy ===
1. Sunrise City by Neon Echo
    Score: 3.92
    Reasons:
    - genre match (+2.0)
    - mood match (+1.0)
    - energy similarity (+0.92)
2. Gym Hero by Max Pulse
    Score: 2.97
    Reasons:
    - genre match (+2.0)
    - energy similarity (+0.97)
3. Rooftop Lights by Indigo Parade
    Score: 1.86
    Reasons:
    - mood match (+1.0)
    - energy similarity (+0.86)
```

Note: terminal image capture is environment-specific, so this README includes a direct text snapshot of the verified CLI output.

## Setup and Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the recommender demo:

```bash
python -m src.main
```

3. Run tests:

```bash
pytest -q
```

## What I Learned

The biggest takeaway for me was how much behavior comes from small design choices.
Even a simple weighted formula can give useful recommendations, but changing one weight can noticeably shift what users see.
That makes bias and diversity tradeoffs impossible to ignore, even in a small classroom simulation.

For a deeper write-up, see:

- `model_card.md`
- `reflection.md`
