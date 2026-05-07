"""
Command line runner for the Music Recommender with Confidence Scoring and Guardrails.

Features:
- Intent detection with confidence scores
- Input validation and guardrails
- Semantic + rule-based hybrid ranking
- Explanations and follow-up support
"""

from src.agents.router import route_query_with_confidence
from src.reasoning.output import (
    format_recommendation_output,
    unclear_query_message,
    explain_output,
)
from src.recommender import load_songs, recommend_songs
from src.safety.guardrails import check_input_validity, check_recommendations_not_empty, get_clarification_prompt
from src.retrieval.embeddings import EmbeddingModel
from src.retrieval.hybrid_ranker import rank_with_hybrid


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
    """Main CLI loop with confidence scoring and guardrails."""
    
    # Load songs
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from dataset.\n")
    
    # Initialize embedding model for semantic search
    print("Loading AI embedding model (this happens once)...")
    embedding_model = EmbeddingModel()
    print("Ready!\n")
    
    # Main conversation loop
    while True:
        user_query = input("What would you like? (or 'quit' to exit): ").strip()
        
        # Exit condition
        if user_query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        
        # Guardrail 1: Check input validity
        is_valid, error_msg = check_input_validity(user_query)
        if not is_valid:
            print(f"\n{error_msg}\n")
            continue
        
        # Guardrail 2: Intent detection with confidence
        intent, confidence = route_query_with_confidence(user_query)
        
        if intent == "unknown":
            print(f"\n{get_clarification_prompt()}\n")
            continue
        
        if confidence < 0.65:
            print(f"\n{get_clarification_prompt()}\n")
            continue
        
        # Handle "explain" intent
        if intent == "explain":
            print("\n(Explain intent detected)")
            print("Feature coming soon: I'll explain the last recommendations.\n")
            continue
        
        # Handle "recommend" intent
        if intent == "recommend":
            user_prefs = _build_user_preferences_from_query(user_query)
            
            # Get rule-based recommendations
            recommendations = recommend_songs(user_prefs, songs, k=5)
            
            # Guardrail 3: Check if we got results
            is_valid, error_msg = check_recommendations_not_empty(recommendations)
            if not is_valid:
                print(f"\n{error_msg}\n")
                continue
            
            # Rank with hybrid scoring (semantic + rules)
            # Extract scores and reasons from recommendations
            rule_scores_and_reasons = [(score, reasons) for _, score, reasons in recommendations]
            song_list = [rec[0] for rec in recommendations]
            
            hybrid_results = rank_with_hybrid(
                user_query,
                song_list,
                rule_scores_and_reasons,
                embedding_model,
                semantic_weight=0.4,
                rule_weight=0.6,
            )
            
            # Format and display with confidence
            output = format_recommendation_output(hybrid_results, confidence)
            print(f"\n{output}\n")


if __name__ == "__main__":
    main()

