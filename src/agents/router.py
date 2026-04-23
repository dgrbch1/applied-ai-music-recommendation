from typing import Literal


Route = Literal["recommend", "explain", "unknown"]


def route_query(user_query: str) -> Route:
    """Route a user query to a simple intent label."""
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
