"""
Guardrails for user input validation and safe fallback handling.
"""

from typing import Tuple


def check_input_validity(user_query: str) -> Tuple[bool, str]:
    """
    Validate user input for empty, very short, or nonsensical queries.
    
    Returns:
        (is_valid, reason) where reason is empty if valid, or a helpful message if invalid.
    """
    if not user_query or not user_query.strip():
        return False, "Please type something. Try: 'recommend chill songs' or 'explain why'."
    
    cleaned = user_query.strip()
    
    if len(cleaned) < 2:
        return False, "Your input is too short. Try: 'recommend chill songs' or 'explain why'."
    
    # Check for spam-like patterns (many repeated characters)
    max_repeats = max(
        len("".join(c for c in cleaned if c == char))
        for char in set(cleaned)
        if char not in " "
    )
    if max_repeats > 5:
        return False, "Your input looks unusual. Try: 'recommend chill songs' or 'explain why'."
    
    return True, ""


def check_recommendations_not_empty(recommendations: list) -> Tuple[bool, str]:
    """
    Validate that recommendations are non-empty.
    
    Returns:
        (is_valid, reason)
    """
    if not recommendations:
        return False, "No songs matched your request. Try a different style like 'upbeat', 'chill', or 'rock'."
    
    return True, ""


def get_clarification_prompt() -> str:
    """Return a helpful prompt to guide users."""
    return (
        "I'm not sure what you want. Try one of these:\n"
        "  • recommend chill songs\n"
        "  • recommend upbeat pop\n"
        "  • explain why\n"
        "  • make it more upbeat\n"
        "  • I don't like that"
    )
