from typing import Dict, List, Tuple


Recommendation = Tuple[Dict, float, List[str]]


def format_recommendation_output(results: List[Recommendation], confidence: float = 1.0) -> str:
    """
    Format recommendation results in a readable assistant-like response.
    
    Args:
        results: List of (song, score, reasons) tuples.
        confidence: Intent confidence score (optional, for display).
    
    Returns:
        Formatted string for display to user.
    """
    if not results:
        return "No songs found, try a different input."

    lines = ["Here are your top song recommendations:"]
    
    # Show confidence if below perfect (for transparency)
    if confidence < 0.95 and confidence > 0:
        lines.append(f"(Intent detected with {confidence*100:.0f}% confidence)")
        lines.append("")

    for idx, (song, score, reasons) in enumerate(results, start=1):
        title = song.get("title", "Unknown Title")
        artist = song.get("artist", "Unknown Artist")

        if reasons:
            reason_text = " ".join(
                reason[0].upper() + reason[1:] + "." if len(reason) > 1 else reason.upper() + "."
                for reason in reasons
            )
        else:
            reason_text = "This track aligns with your listening preferences."

        lines.append(f"{idx}. {title} by {artist} (score: {score:.2f})")
        lines.append(f"   This song was selected because {reason_text}")

    return "\n".join(lines)


def unclear_query_message() -> str:
    """Return a helpful guardrail message for unclear requests."""
    return (
        "I could not understand your request. Try asking me to:\n"
        "  • recommend chill songs\n"
        "  • recommend upbeat pop\n"
        "  • explain why\n"
        "  • make it more upbeat"
    )


def explain_output(results: List[Recommendation], confidence: float = 1.0) -> str:
    """
    Format explanation output for "why" queries.
    
    Args:
        results: List of (song, score, reasons) tuples.
        confidence: Intent confidence score.
    
    Returns:
        Formatted explanation string.
    """
    if not results:
        return "I don't have previous recommendations to explain. Ask me to recommend songs first."
    
    lines = ["These songs ranked highest because they align best with your current preferences:"]
    lines.append("")
    
    for idx, (song, score, reasons) in enumerate(results, start=1):
        title = song.get("title", "Unknown Title")
        artist = song.get("artist", "Unknown Artist")
        
        if reasons:
            reason_text = ", ".join(reasons)
        else:
            reason_text = "strong match with your profile"
        
        lines.append(f"{idx}. {title} by {artist}")
        lines.append(f"   Score: {score:.2f} — {reason_text}")
    
    return "\n".join(lines)
