"""The Convergence Invariant (ROADMAP §1.bis): one idea, one tree.

Every rendering of a meaning set must compile to the identical canonical
form. A translator that produces valid but divergent trees fails here.
"""

import json
from pathlib import Path

import pytest

from k65p.validator import linearize, validate

MEANING_SETS_PATH = Path(__file__).resolve().parents[1] / "data" / "conformance" / "meaning_sets.json"

with open(MEANING_SETS_PATH, encoding="utf-8") as _handle:
	MEANING_SETS = json.load(_handle)["meaning_sets"]


@pytest.mark.parametrize("meaning", MEANING_SETS, ids=lambda m: m["id"])
def test_one_idea_one_tree(meaning: dict) -> None:
	canonical = meaning["canonical"]
	assert validate(canonical) == []
	for lang in ("es", "en", "zh"):
		rendering = meaning[lang]
		assert validate(rendering) == [], f"{lang} rendering is invalid"
		assert linearize(rendering) == canonical, f"{lang} rendering diverges from the canonical tree"


def test_suite_is_seeded() -> None:
	assert len(MEANING_SETS) >= 20
