"""HTML fragments returned by the API (the front end injects them as-is, so everything is escaped)."""

from markupsafe import Markup, escape

from perfume_finder.matching import normalize_note, notes_match


def error_html(message):
    return f"<h3>Error</h3><p>{escape(message)}</p>"


def highlight_notes(notes, user_notes):
    """Return the notes as HTML with matches in red, or ``None`` when there are no notes."""
    if not notes:
        return None
    wanted = [normalize_note(n) for n in user_notes]
    parts = []
    for note in notes:
        if any(notes_match(w, normalize_note(note)) for w in wanted):
            parts.append(Markup('<span style="color: red; font-weight: bold;">{}</span>').format(note))
        else:
            parts.append(escape(note))
    return Markup(", ").join(parts)


def _row(label, value):
    return Markup(
        '<div class="note-row"><span class="note-label">{}:</span>'
        '<span class="note-value">{}</span></div>'
    ).format(label, value)


def extracted_notes_html(notes):
    return Markup("<h3>Extracted Notes:</h3><p>{}</p>").format(", ".join(notes))


def no_notes_html():
    return (
        "<h3>Extracted Notes:</h3>"
        "<p>No valid note information could be retrieved from AI.</p>"
        "<h3>Result:</h3>"
        "<p>No matching was performed because no perfume notes were extracted from your comment.</p>"
    )


def no_match_html(notes):
    return (
        f"{extracted_notes_html(notes)}"
        "<h3>Result:</h3>"
        "<p>Unfortunately, no perfumes matching the extracted notes were found.</p>"
    )


def perfume_card_html(perfume, matched, total, user_notes):
    rows = Markup("")
    for label, key in (("Top notes", "top_notes"), ("Heart notes", "heart_notes"), ("Base notes", "base_notes")):
        value = highlight_notes(perfume.get(key, []), user_notes)
        if value is not None:
            rows += _row(label, value)
    # "All Notes" is always shown, even when the list is empty.
    rows += _row("All Notes", highlight_notes(perfume.get("all_notes", []), user_notes) or "Not specified")

    return str(Markup(
        '<div class="perfume-item">'
        '<div class="perfume-image"><img src="/static/perfume.png" alt="Perfume"></div>'
        '<div class="perfume-content">'
        '<div class="perfume-header"><div class="perfume-title-section">'
        '<div class="perfume-name">Perfume: {brand} - {fragrance}</div></div>'
        '<span class="similarity-badge">Similarity: {matched}/{total}</span></div>'
        '<div class="perfume-notes">{rows}</div>'
        "</div></div>"
    ).format(
        brand=perfume.get("brand", "Unknown"),
        fragrance=perfume.get("fragrance", "Unknown"),
        matched=matched,
        total=total,
        rows=rows,
    ))
