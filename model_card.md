# Model Card

## Model Name

VibeFinder 1.0

## Goal / Task

This recommender suggests songs from a small catalog.
It predicts which songs best match one user taste profile.

## Data Used

The dataset is in data/songs.csv.
It has 18 songs.
Each song has genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.
The data is small and hand-labeled, so it does not represent all listeners.
Mood labels are subjective.

## Algorithm Summary

The model gives points when genre matches the user.
The model gives points when mood matches the user.
The model also gives similarity points when song energy is close to the user's target energy.
Then it ranks all songs by total score and returns the top results.
The output also includes short reason strings, like genre match and energy similarity.

## Observed Behavior / Biases

Genre has a strong weight, so the model can repeat the same style.
That can create a filter bubble.
Songs from underrepresented genres can appear less often.
If mood labels are noisy, rankings can feel unfair.

## Evaluation Process

I tested multiple profiles, including pop/happy, chill/lofi, and intense/rock.
I also tested edge cases, like conflicting preferences and missing genre/mood.
I compared baseline weights with an energy-heavy version.
I ran automated tests and confirmed all tests pass.

## Intended Use and Non-Intended Use

Intended use:
- Classroom learning
- Simple, explainable recommendation demos

Non-intended use:
- Real production personalization
- High-stakes decisions
- Any use where fairness or safety requires stronger validation

## Ideas for Improvement

- Add more songs and better genre balance
- Add collaborative signals like likes and skips
- Add diversity-aware ranking so recommendations are less repetitive

## Personal Reflection

My biggest learning moment was seeing how one weight change can shift many recommendations.
AI tools helped me draft scoring options and test ideas quickly.
I still had to double-check AI suggestions, especially around weight choices and edge cases.
I was surprised that a simple formula can still feel like a real recommender.
If I continue this project, I want to add diversity controls and user feedback signals.
