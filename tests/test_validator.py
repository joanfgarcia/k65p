"""Tests of the K-65P v0 reference validator (RFC-002, canonical ids + renderings)."""

import pytest

from k65p.core import Atom, parse_k65p
from k65p.examples import SEED_EXAMPLES
from k65p.primes import LANGUAGES, N_PRIMES, PRIMES, SYMBOL_TO_ID, symbol_for
from k65p.validator import K65PResolveError, is_valid, linearize, render, resolve_atom, validate


@pytest.mark.parametrize("example", SEED_EXAMPLES)
def test_rfc_examples_are_valid(example: str) -> None:
	assert validate(example) == []


@pytest.mark.parametrize("example", SEED_EXAMPLES)
def test_renderings_are_the_same_compound(example: str) -> None:
	canonical = linearize(example)
	for lang in LANGUAGES:
		rendered = render(example, lang)
		assert validate(rendered) == []
		assert linearize(rendered) == canonical


def test_canonical_numeric_form_validates() -> None:
	assert validate("[48 [24 2 60] [22 4 9]]") == []
	assert render("[48 [24 2 60] [22 4 9]]", "en") == "[IF [TOUCH SOMEONE HOT] [HAPPEN SOMETHING BAD]]"


def test_fire_hot_bad_is_not_k65p() -> None:
	# DL-018: los encabezados de moléculas son unarios — tres átomos desnudos
	# siguen sin ser K-65P (el error ahora nombra la aridad de la molécula)
	errors = validate("[FIRE HOT BAD]")
	assert errors, "[FIRE HOT BAD] debe seguir siendo inválido"
	assert any("expects exactly 1 argument" in error for error in errors)


def test_mixed_language_resolves_to_one_compound() -> None:
	assert linearize("[IF [tocar SOMEONE 热] [pasar algo mauvais]]") == "[48 [24 2 60] [22 4 9]]"


def test_arity_errors() -> None:
	assert not is_valid("[sentir yo]")
	assert not is_valid("[morir yo tú]")
	assert not is_valid("[si [ver yo algo]]")
	assert not is_valid("[bueno agua fuego]")


def test_unary_needs_a_clause() -> None:
	errors = validate("[quizá lluvia]")
	assert any("operates on a clause" in error for error in errors)


def test_group_rules() -> None:
	assert any("without a head" in error for error in validate("[malo [G]]"))
	assert any("group members must be atoms" in error for error in validate("[malo [G fuego [caliente fuego]]]"))


def test_root_must_be_a_clause() -> None:
	assert any("root must be a clause" in error for error in validate("yo"))


def test_non_operator_prime_as_head() -> None:
	errors = validate("[yo tú]")
	assert any("is not an operator" in error for error in errors)


def test_operator_must_be_an_atom() -> None:
	errors = validate("[[si] yo]")
	assert any("operator must be an atom" in error for error in errors)


def test_prime_id_out_of_range() -> None:
	errors = validate("[65 yo]")
	assert any("out of range" in error for error in errors)
	with pytest.raises(K65PResolveError):
		resolve_atom(Atom("99"))


def test_empty_clause_reported() -> None:
	tree = parse_k65p("[si [ver yo] [ver yo]]")
	tree[1] = []
	assert any("empty clause" in error for error in validate(tree))


def test_syntax_errors_are_reported_as_validation_errors() -> None:
	assert validate("[si [tocar") != []


def test_lexicon_check() -> None:
	lexicon = {"fuego", "agua"}
	assert is_valid("[caliente fuego]", lexicon=lexicon)
	errors = validate("[caliente dragón]", lexicon=lexicon)
	assert any("not in the lexicon" in error for error in errors)


def test_resolve_atom_kinds() -> None:
	assert resolve_atom(Atom("g")) == "G"
	assert resolve_atom(Atom("48")) == 48
	assert resolve_atom(Atom("WENN")) == 48
	assert resolve_atom(Atom("fuego")) == "fuego"


def test_primes_table_shape() -> None:
	assert N_PRIMES == 65
	assert all(len(row) == len(LANGUAGES) for row in PRIMES)
	assert SYMBOL_TO_ID["si"] == 48
	assert symbol_for(62, "es") == "agua_prima"
	with pytest.raises(ValueError, match="unknown language"):
		symbol_for(0, "klingon")


def test_render_keeps_lexicon_words() -> None:
	assert render("[querer yo [hacer yo beber agua]]", "en") == "[WANT I [DO I beber agua]]"


# ── DL-021: nombres propios como símbolos ──

def test_name_terms_are_valid() -> None:
	assert validate("[capital [N paris] [N france]]") == []
	assert validate("[N juan francisco garcia]") == []
	assert validate("[have [N juan] dog]") == []


def test_name_marker_rules() -> None:
	assert validate("[N]")                       # vacía
	assert validate("[N [N a]]")                 # N anidado
	assert validate("[N [G a b]]")               # cláusula dentro
	assert validate("[N water]")                 # colisión con primo
	assert validate("[fuego agua tierra]")       # bolsa sin nombres: fuera


def test_names_are_never_heads() -> None:
	# la relación es la cabeza; el nombre solo argumento
	assert validate("[[N juan] have dog]"), "un nombre no puede encabezar"
	assert validate("[have [N juan] dog]") == []
	# con namespace declarado, el átomo-nombre desnudo tampoco encabeza
	assert validate("[paris algo]", names={"paris"})


def test_name_bridge_flattening() -> None:
	from k65p.bridge import to_prolog
	assert to_prolog("[capital [N paris] [N france]]") == "capital(paris,france)."
	assert to_prolog("[N juan francisco garcia]") == "juan_francisco_garcia."
	assert to_prolog("[have [N juan] dog]") == "have(juan,dog)."
