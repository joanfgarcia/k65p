import pytest

from k65p.core import Atom, parse_k65p


def test_atom_representation() -> None:
	atom = Atom("FIRE")
	assert repr(atom) == "FIRE"
	assert atom == Atom("FIRE")
	assert atom != "FIRE"  # type: ignore[comparison-overlap]


def test_parse_simple_k65p() -> None:
	parsed = parse_k65p("[FIRE HOT BAD]")
	expected = [Atom("FIRE"), Atom("HOT"), Atom("BAD")]
	assert parsed == expected


def test_parse_nested_k65p() -> None:
	parsed = parse_k65p("[si [tocar alguien fuego] [pasar algo malo]]")
	expected = [Atom("si"), [Atom("tocar"), Atom("alguien"), Atom("fuego")], [Atom("pasar"), Atom("algo"), Atom("malo")]]
	assert parsed == expected


def test_parse_errors() -> None:
	with pytest.raises(SyntaxError, match="Unexpected EOF"):
		parse_k65p("")

	with pytest.raises(SyntaxError, match="Expected"):
		parse_k65p("[si [tocar")

	with pytest.raises(SyntaxError, match="Unexpected"):
		parse_k65p("]")

	with pytest.raises(SyntaxError, match="Extra tokens"):
		parse_k65p("[a] [b]")
