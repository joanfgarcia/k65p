"""RFC-003: the Horn Bridge — K-65P v0 ↔ Prolog, both directions.

Representation form (canonical, round-trip guaranteed): every K-65P clause
becomes one ground Prolog term — `[48 A B]` → `implies(A', B').`
Executable form (for the engine): conditionals become ground rules —
`B' :- A'.` — so a Prolog engine can chain them.

The bridge refuses invalid K-65P: translation presupposes certification.
"""

import re

from k65p.core import SExpr, parse_k65p
from k65p.primes import GROUP, NAME, PRIMES, symbol_for
from k65p.validator import BINARY, EVALUATORS, PREDICATES, UNARY, _resolve_tree, validate


class BridgeError(ValueError):
	"""Raised when an expression cannot cross the bridge."""


# Prolog functor names per operator prime (english symbol, collision-escaped).
_FUNCTORS: dict[int, str] = {
	**{pid: symbol_for(pid, "en").lower() for pid in PREDICATES},
	**{pid: symbol_for(pid, "en").lower() for pid in EVALUATORS},
	**{pid: symbol_for(pid, "en").lower() for pid in UNARY},
	**{pid: symbol_for(pid, "en").lower() for pid in BINARY},
	44: "neg",      # NOT: `not` is reserved in Prolog
	48: "implies",  # IF: the representation functor; executable form uses `:-`
}
_FUNCTOR_TO_ID: dict[str, int] = {name: pid for pid, name in _FUNCTORS.items()}

# Atom names for primes in argument position (english symbol, escaped).
_ARG_ESCAPES = {"true": "truth", "not": "not_"}
_ARG_ATOM: dict[int, str] = {
	pid: _ARG_ESCAPES.get(row[0].lower(), row[0].lower()) for pid, row in enumerate(PRIMES)
}
_ARG_TO_ID: dict[str, int] = {name: pid for pid, name in _ARG_ATOM.items()}

_UNQUOTED = re.compile(r"^[a-z][a-zA-Z0-9_]*$")


def _atom_to_prolog(resolved: int | str) -> str:
	name = _ARG_ATOM[resolved] if isinstance(resolved, int) else resolved
	return name if _UNQUOTED.match(name) else "'" + name.replace("'", "\\'") + "'"


def _term(node: list | int | str) -> str:
	if not isinstance(node, list):
		return _atom_to_prolog(node)
	head, args = node[0], node[1:]
	if head == GROUP:
		mods = ",".join(_atom_to_prolog(arg) for arg in args[1:])
		return f"g({_atom_to_prolog(args[0])},[{mods}])"
	if head == NAME:
		# DL-021: [N juan francisco] → átomo Prolog juan_francisco (convención
		# de unión por '_'; las partes no pueden contener '_')
		joined = "_".join(str(p) for p in args)
		return joined if _UNQUOTED.match(joined) else "'" + joined + "'"
	if isinstance(head, str):
		# DL-018/021: cabezas-molécula (compuestas, atribuciones, relaciones
		# sobre nombres) — el functor es la palabra misma, escapada si hace falta
		return f"{_atom_to_prolog(head)}({','.join(_term(arg) for arg in args)})"
	return f"{_FUNCTORS[head]}({','.join(_term(arg) for arg in args)})"


def to_prolog(tree: SExpr | str, executable: bool = False) -> str:
	"""Translate a valid K-65P v0 clause to a Prolog clause (with final period)."""
	errors = validate(tree)
	if errors:
		raise BridgeError("not valid K-65P: " + "; ".join(errors))
	resolved = _resolve_tree(parse_k65p(tree) if isinstance(tree, str) else tree)
	if executable and isinstance(resolved, list) and resolved[0] == 48:
		antecedent, consequent = resolved[1], resolved[2]
		return f"{_term(consequent)} :- {_term(antecedent)}."
	return f"{_term(resolved)}."


# ── Inverse direction: a tiny parser for the generated Prolog subset ──

_TOKEN = re.compile(r"\s*(?:('(?:\\'|[^'])*')|([a-zA-Z0-9_]+)|([()\[\],]))")


def _tokenize(text: str) -> list[str]:
	tokens: list[str] = []
	position = 0
	text = text.strip().removesuffix(".")
	while position < len(text):
		match = _TOKEN.match(text, position)
		if not match:
			raise BridgeError(f"unparseable Prolog at: {text[position:position + 20]!r}")
		tokens.append(match.group(1) or match.group(2) or match.group(3))
		position = match.end()
	return tokens


def _read_atom(token: str) -> str:
	if token.startswith("'"):
		return token[1:-1].replace("\\'", "'")
	return token


def _parse_term(tokens: list[str], position: int) -> tuple[list | str, int]:
	name = _read_atom(tokens[position])
	position += 1
	if position < len(tokens) and tokens[position] == "(":
		args: list[list | str] = []
		position += 1
		while tokens[position] != ")":
			if tokens[position] == ",":
				position += 1
				continue
			if tokens[position] == "[":
				mods: list[str] = []
				position += 1
				while tokens[position] != "]":
					if tokens[position] != ",":
						mods.append(_read_atom(tokens[position]))
					position += 1
				args.append(["__list__", *mods])
				position += 1
				continue
			term, position = _parse_term(tokens, position)
			args.append(term)
		return [name, *args], position + 1
	return name, position


def _atom_to_k65p(name: str) -> str:
	if name in _ARG_TO_ID:
		return str(_ARG_TO_ID[name])
	return name


def _to_tree(node: list | str) -> str:
	if not isinstance(node, list):
		return _atom_to_k65p(node)
	name, args = node[0], node[1:]
	if name == "g":
		head, mods = args[0], args[1]
		parts = [_atom_to_k65p(head)] + [_atom_to_k65p(mod) for mod in mods[1:]]
		return "[G " + " ".join(parts) + "]"
	if name not in _FUNCTOR_TO_ID:
		raise BridgeError(f"unknown functor {name!r}")
	prime_id = _FUNCTOR_TO_ID[name]
	return f"[{prime_id} " + " ".join(_to_tree(arg) for arg in args) + "]"


def from_prolog(text: str) -> str:
	"""Translate a bridge-generated Prolog clause back to canonical K-65P."""
	if ":-" in text:
		consequent_text, antecedent_text = text.split(":-", 1)
		antecedent = from_prolog(antecedent_text)
		consequent = from_prolog(consequent_text)
		return f"[48 {antecedent} {consequent}]"
	tokens = _tokenize(text)
	term, position = _parse_term(tokens, 0)
	if position != len(tokens):
		raise BridgeError("trailing tokens after Prolog term")
	if not isinstance(term, list):
		raise BridgeError(f"a bare atom {term!r} is not a K-65P clause")
	canonical = _to_tree(term)
	errors = validate(canonical)
	if errors:
		raise BridgeError("crossed the bridge into invalid K-65P: " + "; ".join(errors))
	return canonical
