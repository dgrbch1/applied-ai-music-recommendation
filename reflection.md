# Reflection - Music Recommender Simulation

## 1. Profile Comparison

- High-Energy Pop vs Chill Lofi: Changing genre, mood, and target energy gave clearly different top songs. This showed me the model is responding to both category matches and numeric similarity.
- High-Energy Pop vs Deep Intense Rock: Both wanted high energy, but genre and mood still changed the top recommendation from pop to rock/intense songs.
- Chill Lofi vs Deep Intense Rock: These profiles produced almost opposite recommendation lists, which confirmed strong separation in the ranking.

## 2. Behavior Under Edge Cases

- Conflicting profile (chill + very high energy): The model still pushed songs with category matches even when energy fit was weak, so category weights can overpower numeric mismatch.
- Genreless profile (energy-only): Recommendations became almost pure energy matching, which made results less specific and less personal.

## 3. What I Learned About Recommenders

- Recommendation systems are a pipeline: represent user taste, compare candidates, score, then rank.
- Real platforms usually combine collaborative filtering (other users' behavior) and content-based filtering (item attributes). My simulation only implements the content-based side, which made the scoring logic easier to explain.
- A good scoring rule for one song is necessary but not sufficient. You still need a ranking rule to build the final list.
- Small weight changes can noticeably change what appears in top results.

## 4. Bias and Limitations

- Genre-heavy weighting can create filter bubbles.
- Subjective labels (especially mood) introduce data-quality bias.
- Small datasets can over-represent some tastes and hide others.
- In a real app, this could unfairly reduce exposure for underrepresented genres because the model repeatedly reinforces prior preferences.

## 5. AI Use Reflection

AI tools helped with:

- Structuring the scoring formula
- Stress-testing profile ideas
- Brainstorming bias and evaluation checkpoints

AI did not replace reasoning:

- I still had to verify that suggested weights made sense for this dataset.
- I still had to inspect edge cases where outputs looked plausible but were biased.

## 6. Next Improvements

- Add collaborative signals (likes/skips) to reduce pure content bias
- Add diversity-aware reranking to improve discovery
- Expand and rebalance the song dataset
