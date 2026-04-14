# Model Card - VibeRank CLI 1.0

## 1. Model Name

VibeRank CLI 1.0

## 2. Intended Use

This model recommends top songs from a small CSV catalog based on user taste preferences.
Primary users are students learning how recommendation systems transform data into ranked predictions.

## 3. Out of Scope

- Real-world personalization at production scale
- Safety-critical or high-stakes decisions
- Monetization or ad targeting

## 4. Inputs and Outputs

Inputs:

- Song attributes: genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- User preference profile: preferred genre, preferred mood, target energy, optional weighting controls

Outputs:

- Ranked list of songs
- Per-song score
- Human-readable reasons (for example genre match, mood match, energy similarity)

## 5. Data

Source file: `data/songs.csv`

Data characteristics:

- 18 songs
- Hand-curated labels
- Limited genre and mood coverage
- Not representative of global listening behavior

Data limitations:

- Small sample size
- Subjective labels (especially mood)
- Unknown annotation consistency

## 6. Model Details

Type: content-based weighted score recommender

Scoring idea:

- Categorical matches: genre and mood
- Numeric similarity: energy closeness to target

Default rule:

- `score = 2.0 * genre_match + 1.0 * mood_match + 1.0 * energy_similarity`

Ranking:

- Compute score for every song
- Sort descending
- Return top `k`

## 7. Evaluation

Evaluation methods used:

- Unit tests for scoring and ranking behavior
- Manual profile-based scenario checks
- Weight sensitivity experiment

Test status at submission:

- `4 passed`

Representative scenarios:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Conflicting profile (chill + very high energy)
- Genreless profile (energy-only)

## 8. Bias, Risks, and Harms

Known bias risks:

- Filter bubble risk when genre has high weight
- Under-recommendation of underrepresented genres in the dataset
- Label bias from subjective mood tags
- Popularity and social effects absent (no collaborative signals)

Potential harm if misused:

- Reinforcement of narrow taste patterns
- Reduced discovery of diverse music

## 9. Transparency and Explainability

The model is intentionally interpretable:

- Score components are explicit and weighted
- Explanations list which factors contributed points
- Weight values can be inspected and adjusted

## 10. Future Improvements

- Expand dataset size and genre balance
- Add user feedback loops (likes, skips) and collaborative features
- Add diversity-aware reranking constraints
- Calibrate weights with validation metrics instead of manual defaults
- Improve label quality and consistency checks

## 11. Ethical Reflection

The model demonstrates that recommendation quality is not just about prediction accuracy.
Weight choices encode product values. A design that optimizes only match strength can reduce diversity and increase filter bubbles.
Future versions should optimize both relevance and exploration.
