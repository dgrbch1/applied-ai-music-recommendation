from typing import Dict, List, Tuple


Recommendation = Tuple[Dict, float, List[str]]


def format_recommendation_output(results: List[Recommendation]) -> str:
    """Format recommendation results in a readable assistant-like response."""
    if not results:
        return "No songs found, try a different input."

    lines = ["Here are your top song recommendations:"]

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
    return "I could not understand your request. Try asking me to recommend songs or explain why a song was recommended."
