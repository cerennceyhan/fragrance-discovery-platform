import logging

from markupsafe import escape
from flask import Blueprint, current_app, jsonify, render_template, request

from perfume_finder.matching import find_matching_perfumes, load_perfume_database
from perfume_finder.rendering import (
    error_html,
    extracted_notes_html,
    no_match_html,
    no_notes_html,
    perfume_card_html,
)

logger = logging.getLogger(__name__)
bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/analyze_comment", methods=["POST"])
def analyze_comment():
    text = (request.get_json(silent=True) or {}).get("text", "")
    extractor = current_app.extensions["note_extractor"]

    if not extractor.available:
        return jsonify({"reply": error_html("Groq client could not be established during application startup.")})
    if not text:
        return jsonify({"reply": error_html("Please enter a comment.")})

    try:
        notes = extractor.extract(text)

        database = load_perfume_database(current_app.config["PERFUME_DATABASE_PATH"])
        if not database:
            return jsonify({"reply": error_html("Perfume database could not be loaded.")})

        if not notes:
            return jsonify({"reply": no_notes_html()})

        matches = find_matching_perfumes(notes, database)
        if not matches:
            return jsonify({"reply": str(no_match_html(notes))})

        return jsonify({
            "notes_html": str(extracted_notes_html(notes)),
            "perfumes": [
                perfume_card_html(perfume, matched, total, notes)
                for perfume, _score, matched, total in matches
            ],
        })
    except Exception as exc:  # Groq/network errors are shown to the user, not raised
        logger.exception("analyze_comment failed")
        return jsonify({"reply": f"<h3>API Error Occurred</h3><p>{escape(str(exc))}</p>"})
