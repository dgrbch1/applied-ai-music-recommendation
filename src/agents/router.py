from typing import Literal, Tuple


Route = Literal["recommend", "explain", "unknown"]


def route_query(user_query: str) -> Route:
    """
    Route a user query to a simple intent label (legacy function).
    
    Kept for backward compatibility. Use route_query_with_confidence() for new code.
    """
    text = user_query.lower()

    if "why" in text or "explain" in text:
        return "explain"

    recommend_keywords = {
        "recommend",
        "song",
        "music",
        "chill",
        "sad",
        "happy",
        "lofi",
        "action",
    }
    if any(keyword in text for keyword in recommend_keywords):
        return "recommend"

    return "unknown"


def route_query_with_confidence(user_query: str) -> Tuple[Route, float]:
    """
    Route a user query to an intent label with confidence score.
    
    Confidence scoring logic:
    - Exact keyword match: 0.95 confidence
    - Fuzzy/indirect match: 0.70 confidence
    - No match: 0.0 confidence (intent is "unknown")
    
    Args:
        user_query: User's input text.
    
    Returns:
        (intent, confidence) tuple where intent is "recommend", "explain", or "unknown",
        and confidence is a float in [0.0, 1.0].
    """
    text = user_query.lower()
    
    # Explain intent detection
    explain_exact = {"why", "explain"}
    explain_fuzzy = {"reason", "because", "how", "what", "curious"}
    
    if any(kw in text for kw in explain_exact):
        return "explain", 0.95
    if any(kw in text for kw in explain_fuzzy):
        return "explain", 0.70
    
    # Recommend intent detection
    recommend_exact = {"recommend", "song", "music"}
    recommend_fuzzy = {
        "chill", "sad", "happy", "lofi", "action",
        "upbeat", "rock", "pop", "calm", "intense",
        "suggest", "play", "like"
    }
    
    if any(kw in text for kw in recommend_exact):
        return "recommend", 0.95
    if any(kw in text for kw in recommend_fuzzy):
        return "recommend", 0.70
    
    # No match
    return "unknown", 0.0
