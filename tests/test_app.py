import pytest

from perfume_finder import create_app
from perfume_finder.config import Config
from perfume_finder.llm import parse_notes
from perfume_finder.matching import calculate_similarity, find_matching_perfumes, load_perfume_database
from perfume_finder.rendering import highlight_notes

DB = [
    {"brand": "A", "fragrance": "Woody", "all_notes": ["Cedarwood", "Vetiver", "Amber"],
     "top_notes": [], "heart_notes": ["Vetiver"], "base_notes": ["Cedarwood", "Amber"]},
    {"brand": "B", "fragrance": "Fresh", "all_notes": ["Lemon", "Mint"],
     "top_notes": ["Lemon", "Mint"], "heart_notes": [], "base_notes": []},
]


class FakeExtractor:
    available = True

    def __init__(self, notes):
        self.notes = notes

    def extract(self, text):
        return self.notes


@pytest.fixture
def client(tmp_path):
    import json
    db = tmp_path / "db.json"
    db.write_text(json.dumps(DB))

    class TestConfig(Config):
        PERFUME_DATABASE_PATH = str(db)
        TESTING = True

    app = create_app(TestConfig)
    app.extensions["note_extractor"] = FakeExtractor(["vetiver", "cedarwood"])
    return app.test_client()


def test_real_database_loads_and_has_required_fields():
    db = load_perfume_database(Config.PERFUME_DATABASE_PATH)
    assert len(db) > 100
    assert all("all_notes" in p and "brand" in p for p in db)


def test_missing_database_returns_empty_list(tmp_path):
    assert load_perfume_database(tmp_path / "nope.json") == []


def test_similarity_counts_partial_matches():
    score, matched, total = calculate_similarity(["vetiver", "cedar", "rose"], DB[0])
    assert (matched, total) == (2, 3)
    assert score == pytest.approx(2 / 3)
    assert calculate_similarity([], DB[0]) == (0, 0, 0)


def test_matches_are_sorted_best_first():
    results = find_matching_perfumes(["vetiver", "cedarwood", "lemon"], DB)
    assert [r[0]["brand"] for r in results] == ["A", "B"]
    assert results[0][1] > results[1][1]


def test_parse_notes_handles_noise():
    assert parse_notes('Sure! {"notes": ["rose", "oud"]} hope that helps') == ["rose", "oud"]
    assert parse_notes("no json here") == []
    assert parse_notes('{"notes": "rose"}') == []


def test_highlight_escapes_html():
    out = highlight_notes(["<script>x</script>", "Vetiver"], ["vetiver"])
    assert "<script>" not in str(out)
    assert "color: red" in str(out)
    assert highlight_notes([], ["x"]) is None


def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200 and b"analyze_comment" in res.data


def test_analyze_returns_perfume_cards(client):
    res = client.post("/analyze_comment", json={"text": "I love vetiver and cedarwood"})
    data = res.get_json()
    assert "Extracted Notes" in data["notes_html"]
    assert len(data["perfumes"]) == 1
    assert "Similarity: 2/2" in data["perfumes"][0]


def test_analyze_empty_text(client):
    assert "Please enter a comment" in client.post("/analyze_comment", json={"text": ""}).get_json()["reply"]


def test_analyze_no_notes_and_no_match(client):
    client.application.extensions["note_extractor"] = FakeExtractor([])
    assert "No valid note" in client.post("/analyze_comment", json={"text": "hi"}).get_json()["reply"]
    client.application.extensions["note_extractor"] = FakeExtractor(["unobtainium"])
    assert "no perfumes matching" in client.post("/analyze_comment", json={"text": "hi"}).get_json()["reply"]


def test_llm_error_is_reported_not_raised(client):
    class Boom(FakeExtractor):
        def extract(self, text):
            raise RuntimeError("<b>rate limited</b>")

    client.application.extensions["note_extractor"] = Boom([])
    reply = client.post("/analyze_comment", json={"text": "x"}).get_json()["reply"]
    assert "API Error" in reply and "<b>" not in reply


def test_app_starts_without_api_key(monkeypatch):
    class NoKey(Config):
        GROQ_API_KEY = ""

    app = create_app(NoKey)
    res = app.test_client().post("/analyze_comment", json={"text": "x"})
    assert res.status_code == 200
