# AI Music Recommendation System

A modular, production-oriented Python application that demonstrates applied AI techniques for semantic search, intent understanding, and explainable ranking. This system goes beyond basic filtering by combining rule-based logic with semantic embeddings, confidence scoring, and safety guardrails.

---

## 1. Project Overview

This project implements an intelligent music recommendation engine that:

- **Understands Intent**: Routes user queries with confidence scoring (0.0–1.0) to detect whether they want recommendations, explanations, or clarification
- **Validates Input**: Uses guardrails to catch malformed, spam-like, or empty inputs before processing
- **Searches Semantically**: Encodes songs and queries into dense vector embeddings using `sentence-transformers` for "vibe" matching
- **Ranks Intelligently**: Combines rule-based scores (60% weight) with semantic similarity (40% weight) for hybrid ranking
- **Explains Reasoning**: Shows why each song was selected, citing both genre/mood matches and semantic similarity scores

The system is modular, fully tested (26/26 passing tests), and deployable as either a CLI application or an API endpoint. It prioritizes explainability and reliability over raw accuracy, making it ideal for educational purposes and real-world demonstrations.

---

## 2. Features

### Core AI Components

- **Intent Routing with Confidence**: Detects user intent (recommend, explain, unknown) with keyword-based confidence scoring
  - Exact keyword match: 0.95 confidence
  - Fuzzy keyword match: 0.70 confidence
  - No match: 0.0 confidence (triggers clarification)

- **Semantic Search & Embeddings**: Uses `sentence-transformers` to encode songs and queries into dense vectors
  - Local model execution (no external API calls)
  - Cosine similarity ranking for semantic relationships
  - One-time model download (~60MB), then fully offline-capable

- **Hybrid Ranking System**: Combines multiple signals for robust recommendations
  - Rule-based scoring: Genre, mood, and energy matching
  - Semantic scoring: Vector similarity between query and songs
  - Adaptive weighting: 60% rules + 40% semantics (tunable)

- **Input Validation & Guardrails**: Prevents crashes and provides helpful feedback
  - Empty input detection
  - Spam pattern recognition
  - Malformed data handling
  - User-friendly error messages

- **Explainable Output**: Every recommendation includes reasoning
  - Shows detected intent and confidence
  - Lists contributing factors (genre match, energy similarity, etc.)
  - Enables transparency and trust

- **Comprehensive Test Suite**: 26 unit tests covering all components
  - Confidence routing and edge cases
  - Input validation and guardrails
  - Semantic embeddings and similarity
  - Backward compatibility with original recommender

---

## 3. AI Workflow

The system follows a structured pipeline:

```
User Input
    ↓
Guardrails Validation (empty, spam, malformed check)
    ↓
Intent Routing (detect intent + compute confidence score)
    ↓
Confidence Threshold Check
    ├─→ Low confidence → Generate clarification prompt
    └─→ High confidence → Continue processing
    ↓
Rule-Based Recommender (score songs by genre/mood/energy)
    ↓
Semantic Embeddings (encode songs and query to vectors)
    ↓
Hybrid Ranker (combine rule scores + semantic similarity)
    ↓
Output Formatter (structure results with explanations)
    ↓
Final Response (recommendations + reasoning)
```

**Key Decision Points**:
- If intent confidence < 0.65: Ask user to clarify rather than guess
- If no songs match criteria: Suggest alternatives or ask for refinement
- If input invalid: Show guardrail error and provide examples

---

## 4. Project Architecture

### Directory Structure

```
src/
├── main.py                    # CLI entry point, main interaction loop
├── recommender.py             # Rule-based scoring engine
├── agents/
│   └── router.py              # Intent detection + confidence scoring
├── retrieval/
│   ├── embeddings.py          # Semantic search using sentence-transformers
│   └── hybrid_ranker.py       # Combines rule + semantic scores
├── reasoning/
│   └── output.py              # Formats recommendations with explanations
└── safety/
    └── guardrails.py          # Input validation + error handling

tests/
├── test_recommender.py        # Original recommender tests
├── test_router_confidence.py  # Confidence routing tests
├── test_guardrails.py         # Input validation tests
└── test_semantic_search.py    # Embedding + similarity tests

data/
└── songs.csv                  # 18 sample songs with metadata

requirements.txt               # Dependencies
README.md                      # This file
```

### Component Responsibilities

| Component | Purpose | Key Technologies |
|-----------|---------|------------------|
| **Router** | Detects intent, computes confidence | Keyword matching, string similarity |
| **Recommender** | Scores songs by genre/mood/energy | Content-based filtering, rule logic |
| **Embeddings** | Encodes text to semantic vectors | sentence-transformers, cosine similarity |
| **Hybrid Ranker** | Merges rule + semantic scores | Weighted averaging, normalization |
| **Guardrails** | Validates input, handles errors | Regex patterns, length checks, error messages |
| **Output Formatter** | Structures results for display | Template formatting, explanation logic |

---

## 5. Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)

### Step 1: Install AI & Semantic Search Dependencies

Before running the application, install all required dependencies:

```powershell
pip install -r requirements.txt
```

This installs core AI and semantic search packages:

- **sentence-transformers**: Semantic embedding model for vector-based similarity
- **torch**: Deep learning framework underlying the embeddings
- **transformers**: Hugging Face model architecture library
- **scikit-learn**: Similarity metrics and ML utilities
- **pandas**: Data loading and manipulation
- **pytest**: Testing framework

> **Note**: The first run will download the embedding model (~60MB). This is a one-time operation and the model is cached locally for offline use in subsequent runs.

### Step 2: Verify Installation

```powershell
python -m pytest tests/ -v
```

Expected output: **26/26 tests passing**

---

## 6. Running the Application

### Start the CLI Application

```powershell
python -m src.main
```

This launches the interactive command-line interface. The application will prompt you for input and process your requests through the full AI workflow.

### Example Prompts to Try

- **`chill songs`** — Semantic search for relaxing music; hybrid ranking combines mood match + vibe
- **`workout music`** — High-energy recommendations; rule-based genre/energy scoring dominates
- **`why these songs`** — Explanation mode (shows why previous recommendations were selected)
- **`blah blah`** — Low-confidence input; triggers clarification with suggested commands
- **(empty input)** — Caught by guardrails; shows validation error and helpful suggestions

---

## 7. Example Usage

### Session 1: Recommendation Request

```
What would you like? chill songs

Here are your top song recommendations:
(Intent detected with 95% confidence)

1. Sunrise City by Neon Echo (score: 0.72)
   Selected because: Genre match (+2.0) + Energy similarity (+0.98)

2. Midnight Chill by LoRoom (score: 0.68)
   Selected because: Mood match (+1.5) + Semantic match (+0.82)

3. Acoustic Vibes by Alex Nova (score: 0.65)
   Selected because: Genre match (+2.0) + Energy similarity (+0.70)
```

**What Happened**:
- Router detected "chill" keyword with exact match (0.95 confidence)
- Recommender scored songs using mood/energy rules
- Semantic embeddings found vectors similar to "chill"
- Hybrid ranker merged both signals into final scores

### Session 2: Low Confidence Triggers Clarification

```
What would you like? xyz abc random

I'm not sure what you want. Try one of these:
  • chill songs
  • workout music
  • why these songs
  • make it more upbeat
  • I don't like that
```

**What Happened**:
- Router found no keyword matches (0.0 confidence)
- Confidence below threshold → Clarification mode triggered
- System suggests valid commands instead of guessing

### Session 3: Guardrails Catch Invalid Input

```
What would you like? (empty)

Please enter a command. Try:
  • chill songs
  • workout music
  • why these songs
```

```
What would you like? aaaaaaaaaa

Your input looks unusual. Try:
  • chill songs
  • workout music
  • why these songs
```

---

## 8. Technologies Used

### Core Stack

- **Python 3.8+**: Language and runtime
- **pandas**: Data loading (CSV) and manipulation
- **scikit-learn**: Cosine similarity and ML utilities
- **numpy**: Numerical operations and matrix math

### AI & ML

- **sentence-transformers**: Pre-trained semantic embedding model (all-MiniLM-L6-v2)
- **torch**: Deep learning framework for embeddings
- **transformers**: Hugging Face model architecture and tokenization

### Testing & Quality

- **pytest**: Unit testing framework
- **pytest-cov** (optional): Code coverage analysis

### Optional Future Layers

- **Flask** / **FastAPI**: REST API development
- **Streamlit**: Interactive UI
- **Spotify API**: Live music catalog integration

---

## 9. Current Limitations

### Dataset & Scope

- **Small dataset**: Only 18 hand-labeled songs; may not reflect diversity of real music libraries
- **Subjective labels**: Mood and energy are labeled manually and may not align with all listener preferences
- **No personalization**: System doesn't learn from user feedback or history

### Technical Constraints

- **No frontend**: Currently CLI-only; no web UI or GUI
- **Lightweight embeddings**: Using all-MiniLM-L6-v2 (lightweight but less expressive than larger models)
- **Semantic ranking only**: Doesn't integrate with live APIs (Spotify, YouTube Music, etc.)
- **No filter diversity**: May recommend similar songs repeatedly without explicit diversity control

### Model Limitations

- **Embedding model bias**: Reflects biases in training data (Common Crawl, etc.)
- **Fixed weights**: Hybrid ranking uses fixed 60/40 split; not adaptive per query
- **Cold start**: New songs require manual label entry (no auto-labeling)

---

## 10. Future Improvements

### Phase 5: Feedback Memory & Personalization
- Save user "liked" and "disliked" feedback to persistent storage
- Boost recommendations similar to liked songs
- Down-rank songs similar to disliked ones
- Detect preference drift over time

### Phase 6: Conversational Context
- Maintain session memory (last query, last recommendations)
- Support follow-up queries: "more like the first one" or "less intense"
- Multi-turn dialogue with context awareness

### Phase 7: Web Interface & Deployment
- **Streamlit dashboard**: Interactive UI with song cards, thumbs up/down
- **Flask/FastAPI**: REST API for external integrations
- **Docker containerization**: Reproducible deployment
- **Cloud hosting**: AWS/GCP/Vercel deployment

### Phase 8: Enhanced Explanations & Integration
- **LLM-powered explanations**: Natural language descriptions using GPT or Gemini
- **Spotify API**: Real catalog access instead of sample data
- **YouTube Music integration**: Broader music source
- **User studies**: Test recommendations with real users

### Phase 9: Advanced Ranking
- **Learning-to-rank**: ML-based score optimization using user feedback
- **Diversity boosting**: Ensure recommendations span multiple genres/moods
- **Cross-user insights**: Collaborative filtering component
- **Real-time trending**: Incorporate popularity signals

---

## Why I Built This

This project bridges the gap between academic recommender systems and real-world AI applications. The goal was to deeply understand:

- **Semantic search**: How embeddings capture meaning beyond keywords
- **Ranking systems**: Combining multiple signals for better results
- **Intent understanding**: Routing user requests with confidence scores
- **Explainability**: Why a system made a choice (not a black box)
- **Modular architecture**: Building testable, composable AI components
- **Graceful degradation**: Handling edge cases and invalid input
- **Production readiness**: Guardrails, error handling, comprehensive tests

Rather than chasing accuracy, the focus is on **demonstrating applied AI concepts** in a clear, understandable way that's both educational and impressive in technical interviews.

---

## Testing

Run the full test suite:

```powershell
pytest tests/ -v
```

**Test Coverage**:
- 4 recommender tests (rule-based scoring)
- 9 guardrails tests (input validation, edge cases)
- 6 router confidence tests (keyword detection, fuzzy matching)
- 7 semantic search tests (embeddings, similarity, caching)

All tests are isolated, fast, and designed to demonstrate component reliability.

---

## Design Philosophy

### Modularity First
Each component (router, recommender, embeddings, guardrails) is independently testable and swappable. Easy to replace embeddings or try different ranking strategies.

### Explainability Over Accuracy
Rather than optimizing for perfect recommendations, the system explains its reasoning. Users understand why they got results, building trust.

### Graceful Failures
Invalid input doesn't crash the app—it triggers helpful guidance. Low confidence triggers clarification instead of guessing.

### Backward Compatibility
The original rule-based recommender is untouched. New AI features are additive, not replacements.

### Local-First
All processing runs locally; no external API calls required (except initial embedding model download). Fully offline after setup.

---

## Disclaimer

This is a student-built educational project, not production software. Use for learning, demos, and portfolio purposes. The dataset is small, the model is lightweight, and there are no real user guarantees. See "Current Limitations" for details.

---


