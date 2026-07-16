"""Tests of the K-65P v0 reference validator (RFC-002, canonical ids + renderings)."""

import pytest

from k65p.core import Atom, parse_k65p
from k65p.primes import LANGUAGES, N_PRIMES, PRIMES, SYMBOL_TO_ID, symbol_for
from k65p.validator import K65PResolveError, is_valid, linearize, render, resolve_atom, validate

# The 20 hand-compiled seed examples from RFC-002 §3 (Spanish rendering).
RFC_EXAMPLES_ES = [
	"[ver yo algo]",
	"[oír tú agua]",
	"[caliente fuego]",
	"[malo [G fuego caliente]]",
	"[si [tocar alguien [G fuego caliente]] [pasar [G algo malo] alguien]]",
	"[porque [mover tú lejos] [sentir yo malo]]",
	"[querer yo agua]",
	"[querer yo [hacer yo beber agua]]",
	"[quizá [pasar lluvia]]",
	"[poder [mover yo]]",
	"[no [ver yo algo]]",
	"[saber yo [bueno agua]]",
	"[querer yo [decir tú verdad yo]]",
	"[vivir gente aquí]",
	"[antes [pequeño yo]]",
	"[después [pasar [G algo malo]]]",
	"[como [G cosa este] agua]",
	"[morir [G gente todo]]",
	"[porque [pensar yo] [existir yo]]",
	"[si [tocar tú [G agua frío]] [sentir tú frío]]",
]


@pytest.mark.parametrize("example", RFC_EXAMPLES_ES)
def test_rfc_examples_are_valid(example: str) -> None:
	assert validate(example) == []


@pytest.mark.parametrize("example", RFC_EXAMPLES_ES)
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
	errors = validate("[FIRE HOT BAD]")
	assert any("unknown operator 'fire'" in error for error in errors)


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
