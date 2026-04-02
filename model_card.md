# Model Card - Music Recommender Simulation

## Model Name

VibeRank CLI 1.0

## Goal / Task

This system suggests the top 5 songs from a small catalog.
It predicts what songs best match a user taste profile.

## Data Used

The dataset has 18 songs in data/songs.csv.
It includes genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.
The data is small, hand-labeled, and not representative of all music tastes.

## Algorithm Summary

Each song gets points for genre match and mood match.
It also gets similarity points for how close song energy is to the user's target energy.
The recommender sorts all songs by score and returns the top 5.

## Observed Behavior / Biases

Genre can dominate results and create a filter bubble.
If genre and mood are blank, results become almost energy-only.
Tag quality matters a lot, so wrong mood labels can hurt ranking quality.

## Evaluation Process

I tested High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases.
I compared top-5 lists and checked whether reasons matched the score math.
I also ran a weight-shift experiment: lower genre weight and higher energy weight.

## Intended Use and Non-Intended Use

Intended use: classroom learning and transparent recommendation demos.
Non-intended use: real user personalization, high-stakes decisions, or commercial deployment.

## Ideas for Improvement

- Add more songs and more balanced genre coverage.
- Add diversity controls so top songs are not too similar.
- Add more user preference inputs like tempo range and dislike signals.

## Personal Reflection

My biggest learning moment was seeing how one strong weight changes almost every result.
AI tools helped me draft scoring logic and test profile ideas faster.
I still had to double-check AI output, especially for weight choices and edge cases.
I was surprised that a simple point system can still feel like a real recommender.
Next, I would test diversity-aware ranking and better mood labeling.
