"""Perfume database loading and note matching."""

import json
import logging

logger = logging.getLogger(__name__)


def load_perfume_database(path):
    """Load the perfume JSON database; returns an empty list on failure."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("Perfume database not found: %s", path)
    except (OSError, json.JSONDecodeError) as exc:
        logger.error("Could not load perfume database: %s", exc)
    return []


def normalize_note(note):
    """Lower-case a note and strip commas and dots."""
    return note.lower().strip().replace(",", "").replace(".", "")


def notes_match(a, b):
    """Two normalized notes match when equal or one contains the other."""
    return a in b or b in a


def calculate_similarity(user_notes, perfume):
    """Return ``(score, matched_count, total_count)`` for the user's notes against a perfume."""
    user_normalized = [normalize_note(n) for n in user_notes]
    perfume_normalized = [normalize_note(n) for n in perfume["all_notes"]]

    matched = {
        user_note
        for user_note in user_normalized
        if any(notes_match(user_note, p) for p in perfume_normalized)
    }
    total = len(user_normalized)
    if total == 0:
        return 0, 0, 0
    return len(matched) / total, len(matched), total


def find_matching_perfumes(user_notes, database):
    """Return ``(perfume, score, matched, total)`` tuples, best match first."""
    scored = []
    for perfume in database:
        score, matched, total = calculate_similarity(user_notes, perfume)
        if score > 0:
            scored.append((perfume, score, matched, total))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored
