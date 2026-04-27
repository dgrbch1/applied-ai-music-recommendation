# Applied AI Music Recommendation System

Project demo video: Watch my project demo here: https://www.loom.com/share/99985f6fb7af4546873ad6b57916f724

## 🎥 Video Walkthrough

This video demonstrates the system running end-to-end, including:
- AI routing (agent behavior)
- Recommendations
- Explanation logic
- Guardrails

## 1. Title and Summary

This project is a Python-based Applied AI Music Recommendation System that takes a user query, interprets intent, recommends songs, and explains why those songs were selected.
It matters because it goes beyond just ranking results: it also includes basic agent behavior, reasoning output, and safety guardrails so the system feels more like a real AI assistant.
I built it as a practical step from a classroom recommender into a more complete AI workflow.

## 2. Original Project

The original project was a Music Recommender Simulation using content-based filtering.
Songs were scored using user preferences like genre, mood, and energy, then sorted to return top matches.
The focus was transparent scoring and easy-to-understand recommendation logic.

## 3. Architecture Overview

System flow:

User -> Router -> Recommender -> Output

```mermaid
flowchart LR
   A[User Input] --> B[Router (Agent)]
   B --> C[Recommender (Scoring + Retrieval)]
   C --> D[Output Formatter]
   D --> E[Final Response]
```

What each component does:

- User: Provides natural-language input (for example, "recommend chill songs" or "why these songs").
- Router (Agent): Classifies intent into simple actions such as recommend, explain, or unknown.
- Recommender: Retrieves songs from the dataset and scores them using the existing recommendation logic.
- Output (Reasoning Layer): Converts raw results into clear AI-style responses with song title, artist, score, and explanation in full sentences.

## 4. Features

- Retrieval and scoring using content-based ranking
- Reasoning output that explains why recommendations were chosen
- Agentic workflow using a router for intent handling
- Guardrails for unclear queries and empty recommendation sets
- Unit testing for reliability and regression safety

## 5. User Input Preview

This screenshot shows the user input connected to the recommender flow in the `assets` folder:

![User input preview](assets/User%20Input%20to%20Recommender-2026-04-27-020950.png)

## 6. Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/your-username/applied-ai-music-recommendation-system.git
cd applied-ai-music-recommendation-system
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Run the system

```bash
python -m src.main
```

## 7. Sample Interactions

### Example 1

User input:

```text
chill
```

Example output:

```text
Here are your top song recommendations:
1. Midnight Rain by Lofi Harbor (score: 3.86)
   This song was selected because Genre match (+2.0). Mood match (+1.0). Energy similarity (+0.86).
2. Soft Streets by Ember Coast (score: 3.72)
   This song was selected because Genre match (+2.0). Mood match (+1.0). Energy similarity (+0.72).
3. Window Seat by Night Palette (score: 3.61)
   This song was selected because Genre match (+2.0). Mood match (+1.0). Energy similarity (+0.61).
```

### Example 2

User input:

```text
why these songs
```

Example output:

```text
Here are your top song recommendations:
1. Midnight Rain by Lofi Harbor (score: 3.86)
   This song was selected because Genre match (+2.0). Mood match (+1.0). Energy similarity (+0.86).
2. Soft Streets by Ember Coast (score: 3.72)
   This song was selected because Genre match (+2.0). Mood match (+1.0). Energy similarity (+0.72).

These songs ranked highest because they align best with your current preference profile, especially on genre and energy closeness.
```

Guardrail examples:

```text
No songs found, try a different input.
```

```text
I could not understand your request. Try asking me to recommend songs or explain why a song was recommended.
```

## 8. Design Decisions

I used a modular structure to keep the system easy to extend and easy to test.
The router, recommender, and output reasoning are separated so each part has one clear responsibility.

Trade-offs:

- Simple rule-based routing and scoring are transparent and reliable for a class project.
- More advanced ML (embeddings, collaborative filtering, LLM intent parsing) could improve personalization but adds complexity, data requirements, and tuning overhead.
- For this version, clarity and maintainability were prioritized over model sophistication.

## 9. Testing and Reliability

Current test status: 4/4 tests passed.

Reliability practices used:

- Unit tests check core scoring and recommendation behavior.
- Existing scoring functions were kept stable to avoid breaking prior logic.
- Guardrails handle two common failure paths:
  - unclear user intent
  - empty recommendation results
- Safe fallback messages are returned instead of crashing or giving blank output.

## 10. Reflection

The main thing I learned is that building an AI system is not just about ranking outputs.
You also need intent handling, clear reasoning, and reliability checks so users can trust what they see.
Even with simple rules, system design decisions strongly affect usability, transparency, and failure behavior.

## 11. Ethics and Limitations

This system has real limitations and should be used with those in mind.

- Bias risk: Recommendations reflect the dataset and scoring weights, so underrepresented genres or artists may get less visibility.
- Preference narrowing: Repeatedly favoring similar songs can create a filter-bubble effect.
- Limited context: The system does not learn long-term personal history or social listening patterns.
- Misuse potential: Like any recommendation tool, it could be used to over-promote specific content if objectives are not monitored.

Future improvements could include better dataset balancing, fairness-aware ranking checks, and more robust intent handling while keeping explanations transparent.
