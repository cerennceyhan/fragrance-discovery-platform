"""Note extraction with the Groq API."""

import json
import logging
import re

from groq import Groq

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a perfume expert. Analyze the user's comment.
Extract the perfume notes from the comment and return them **only in English**.
Your response format must be strictly JSON, containing no other text or explanation. For example:
{
  "notes": ["bergamot", "lavender", "vanilla"]
}
Note: If no notes are found in the text, return an empty list.
"""


class NoteExtractor:
    def __init__(self, api_key, model):
        self.model = model
        try:
            self.client = Groq(api_key=api_key)
        except Exception as exc:  # missing/invalid key must not stop the app from starting
            logger.error("Groq client could not be initialized: %s", exc)
            self.client = None

    @property
    def available(self):
        return self.client is not None

    def extract(self, text):
        """Return the list of English perfume notes found in ``text``."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract perfume notes from this comment: {text}"},
            ],
            max_tokens=4096,
            temperature=0.6,
        )
        return parse_notes(response.choices[0].message.content)


def parse_notes(raw_output):
    """Pull the ``notes`` list out of the model's (JSON-ish) answer."""
    match = re.search(r"\{.*\}", (raw_output or "").strip(), re.DOTALL)
    if not match:
        return []
    try:
        notes = json.loads(match.group()).get("notes", [])
    except (json.JSONDecodeError, AttributeError) as exc:
        logger.warning("Could not parse model output: %s", exc)
        return []
    return [str(n) for n in notes] if isinstance(notes, list) else []
