"""Tests of the molecular lexicon (RFC-004)."""

import json

import pytest

from k65p.lexicon import DEFAULT_LEXICON_PATH, LexiconError, load_lexicon, molecule_names
from k65p.validator import is_valid, validate


def test_gold_lexicon_loads_and_is_sound() -> None:
	molecules = load_lexicon()
	assert len(molecules) >= 28
	assert all(entry["tier"] == "gold" for entry in molecules.values())
	assert "fuego" in molecules
	assert molecules["fuego"]["glyph"][60] == 1  # fire is HOT


def test_validator_accepts_the_gold_lexicon() -> None:
	lexicon = molecule_names()
	assert is_valid("[caliente fuego]", lexicon=lexicon)
	assert is_valid("[si [ver yo depredador] [querer yo [mover yo cueva]]]", lexicon=lexicon)
	errors = validate("[caliente dragón]", lexicon=lexicon)
	assert any("not in the lexicon" in error for error in errors)


def _broken_lexicon(tmp_path, name: str, glyph: list[int]):
	path = tmp_path / "lexicon.json"
	path.write_text(json.dumps({"molecules": {name: {"tier": "gold", "glyph": glyph}}}), encoding="utf-8")
	return path


def test_integrity_rejects_prime_collision(tmp_path) -> None:
	with pytest.raises(LexiconError, match="collides with a prime"):
		load_lexicon(_broken_lexicon(tmp_path, "si", [0] * 65))


def test_integrity_rejects_reserved_name(tmp_path) -> None:
	with pytest.raises(LexiconError, match="reserved bridge name"):
		load_lexicon(_broken_lexicon(tmp_path, "truth", [0] * 65))


def test_integrity_rejects_bad_glyphs(tmp_path) -> None:
	with pytest.raises(LexiconError, match="expected 65"):
		load_lexicon(_broken_lexicon(tmp_path, "cosa_nueva", [0] * 64))
	with pytest.raises(LexiconError, match="non-trit"):
		load_lexicon(_broken_lexicon(tmp_path, "cosa_nueva", [0] * 64 + [2]))


def test_default_path_exists() -> None:
	assert DEFAULT_LEXICON_PATH.exists()
