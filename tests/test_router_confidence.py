"""
Tests for router confidence scoring.
"""

import pytest
from src.agents.router import route_query_with_confidence


def test_explain_exact_keyword():
    """High confidence for exact explain keywords."""
    intent, confidence = route_query_with_confidence("why are these songs recommended")
    assert intent == "explain"
    assert confidence == 0.95


def test_explain_fuzzy_keyword():
    """Lower confidence for fuzzy explain keywords."""
    intent, confidence = route_query_with_confidence("i'm curious about this recommendation")
    assert intent == "explain"
    assert confidence == 0.70


def test_recommend_exact_keyword():
    """High confidence for exact recommend keywords."""
    intent, confidence = route_query_with_confidence("recommend chill songs")
    assert intent == "recommend"
    assert confidence == 0.95


def test_recommend_fuzzy_keyword():
    """Lower confidence for mood-based recommend keywords."""
    intent, confidence = route_query_with_confidence("something upbeat")
    assert intent == "recommend"
    assert confidence == 0.70


def test_unknown_intent():
    """Zero confidence for unknown intents."""
    intent, confidence = route_query_with_confidence("xyzabc qwerty 123")
    assert intent == "unknown"
    assert confidence == 0.0


def test_case_insensitive():
    """Router should be case-insensitive."""
    intent_lower, conf_lower = route_query_with_confidence("recommend chill songs")
    intent_upper, conf_upper = route_query_with_confidence("RECOMMEND CHILL SONGS")
    
    assert intent_lower == intent_upper
    assert conf_lower == conf_upper
