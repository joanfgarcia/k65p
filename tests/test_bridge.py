"""Tests of the Horn Bridge (RFC-003): K-65P v0 ↔ Prolog, both directions."""

import pytest

from k65p.bridge import _FUNCTOR_TO_ID, _FUNCTORS, BridgeError, from_prolog, to_prolog
from k65p.examples import SEED_EXAMPLES
from k65p.validator import linearize


@pytest.mark.parametrize("example", SEED_EXAMPLES)
def test_round_trip_over_the_bridge(example: str) -> None:
	prolog = to_prolog(example)
	assert prolog.endswith(".")
	assert from_prolog(prolog) == linearize(example)


def test_fact_translation() -> None:
	assert to_prolog("[caliente fuego]") == "hot(fuego)."
	assert to_prolog("[60 fuego]") == "hot(fuego)."


def test_conditional_representation_and_executable() -> None:
	rule = "[si [tocar alguien fuego] [pasar [G algo malo] alguien]]"
	assert to_prolog(rule) == "implies(touch(someone,fuego),happen(g(something,[bad]),someone))."
	assert to_prolog(rule, executable=True) == "happen(g(something,[bad]),someone) :- touch(someone,fuego)."


def test_executable_round_trip() -> None:
	rule = "[si [tocar alguien fuego] [pasar [G algo malo] alguien]]"
	assert from_prolog(to_prolog(rule, executable=True)) == linearize(rule)


def test_reserved_atom_escapes() -> None:
	assert to_prolog("[querer yo [decir tú verdad yo]]") == "want(i,say(you,truth,i))."
	assert from_prolog("want(i,say(you,truth,i)).") == "[14 0 [18 1 20 0]]"


def test_quoted_molecules_survive() -> None:
	prolog = to_prolog("[caliente árbol]")
	assert prolog == "hot('árbol')."
	assert from_prolog(prolog) == "[60 árbol]"


def test_group_without_modifiers() -> None:
	assert from_prolog(to_prolog("[malo [G fuego]]")) == "[9 [G fuego]]"


def test_invalid_k65p_is_refused() -> None:
	with pytest.raises(BridgeError, match="not valid K-65P"):
		to_prolog("[FIRE HOT BAD]")


def test_inverse_rejects_foreign_prolog() -> None:
	with pytest.raises(BridgeError, match="unknown functor"):
		from_prolog("father(zeus,ares).")
	with pytest.raises(BridgeError, match="not a K-65P clause"):
		from_prolog("fuego.")
	with pytest.raises(BridgeError, match="unparseable"):
		from_prolog("hot(?).")
	with pytest.raises(BridgeError, match="trailing tokens"):
		from_prolog("hot(fuego) hot(agua).")


def test_inverse_rejects_wellformed_prolog_that_maps_to_invalid_k65p() -> None:
	with pytest.raises(BridgeError, match="crossed the bridge"):
		from_prolog("die(i,you).")


def test_functor_table_is_bijective() -> None:
	assert len(_FUNCTOR_TO_ID) == len(_FUNCTORS)
	assert _FUNCTORS[48] == "implies"
	assert _FUNCTORS[44] == "neg"
