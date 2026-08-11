"""RFC-004: the molecular lexicon — molecules made formal.

A molecule is a named 65-trit glyph: a composition of semantic atoms. This
module loads the versioned lexicon (`data/lexicon.json`), checks its
integrity, and exposes the molecule set the validator can certify against.

Tiers: `gold` glyphs are hand-crafted and semantically exact; `derived`
glyphs come from the Ridge projection (documented in frankenswarm's
`expand_vocabulary.py`) and arrive with the factory (ROADMAP Phase 3).
"""

import json
from pathlib import Path

from k65p.primes import N_PRIMES, SYMBOL_TO_ID

DEFAULT_LEXICON_PATH = Path(__file__).resolve().parents[2] / "data" / "lexicon.json"

# Names a molecule may never take: they would collide with the bridge's
# argument atoms or functors (RFC-003 §2).
RESERVED_NAMES = frozenset({"truth", "not_", "neg", "implies", "g"})


class LexiconError(ValueError):
	"""A lexicon that violates its own contract."""


def load_lexicon(path: Path | str = DEFAULT_LEXICON_PATH) -> dict[str, dict]:
	"""Load and integrity-check the lexicon. Returns molecule name -> entry."""
	with open(path, encoding="utf-8") as handle:
		data = json.load(handle)
	molecules: dict[str, dict] = data["molecules"]
	for name, entry in molecules.items():
		key = name.casefold()
		if key in SYMBOL_TO_ID:
			raise LexiconError(f"molecule {name!r} collides with a prime symbol")
		if key in RESERVED_NAMES:
			raise LexiconError(f"molecule {name!r} uses a reserved bridge name")
		glyph = entry["glyph"]
		if len(glyph) != N_PRIMES:
			raise LexiconError(f"molecule {name!r} glyph has {len(glyph)} trits, expected {N_PRIMES}")
		if any(trit not in (-1, 0, 1) for trit in glyph):
			raise LexiconError(f"molecule {name!r} glyph contains non-trit values")
	return molecules


def molecule_names(path: Path | str = DEFAULT_LEXICON_PATH, lang: str = "es") -> set[str]:
	"""The lexicon as the `lexicon=` argument the validator expects."""
	lex = load_lexicon(path)
	if lang == "en":
		return {v.get("en", name).casefold() for name, v in lex.items()}
	return {name.casefold() for name in lex}
