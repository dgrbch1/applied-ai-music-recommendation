"""
Tests for input guardrails and validation.
"""

import pytest
from src.safety.guardrails import (
    check_input_validity,
    check_recommendations_not_empty,
    get_clarification_prompt,
)


def test_empty_input():
    """Empty input should be invalid."""
    is_valid, reason = check_input_validity("")
    assert not is_valid
    assert reason != ""


def test_whitespace_only_input():
    """Whitespace-only input should be invalid."""
    is_valid, reason = check_input_validity("   ")
    assert not is_valid
    assert reason != ""


def test_very_short_input():
    """Single character input should be invalid."""
    is_valid, reason = check_input_validity("a")
    assert not is_valid
    assert reason != ""


def test_valid_short_input():
    """Two+ character input should be valid."""
    is_valid, reason = check_input_validity("chill")
    assert is_valid
    assert reason == ""


def test_spam_pattern_detection():
    """Repeated character spam should be invalid."""
    is_valid, reason = check_input_validity("aaaaaaaaa")
    assert not is_valid
    assert reason != ""


def test_normal_input_valid():
    """Normal user input should be valid."""
    is_valid, reason = check_input_validity("recommend chill songs")
    assert is_valid
    assert reason == ""


def test_recommendations_empty():
    """Empty recommendations list should be invalid."""
    is_valid, reason = check_recommendations_not_empty([])
    assert not is_valid
    assert "No songs" in reason or "try" in reason


def test_recommendations_not_empty():
    """Non-empty recommendations should be valid."""
    mock_recs = [
        ({"title": "Song1"}, 2.5, ["reason1"]),
    ]
    is_valid, reason = check_recommendations_not_empty(mock_recs)
    assert is_valid
    assert reason == ""


def test_clarification_prompt_not_empty():
    """Clarification prompt should contain helpful guidance."""
    prompt = get_clarification_prompt()
    assert prompt != ""
    assert "recommend" in prompt.lower()
    assert "explain" in prompt.lower()
