"""K-65P v0 reference validator (RFC-002).

Ported from the original frankenswarm implementation and re-keyed by prime
id: the validator certifies the *canonical* (numeric) form, and accepts any
language rendering by resolving symbols to ids first — `[si ...]`, `[IF ...]`
and `[48 ...]` are the same compound.

Source of truth: on any discrepancy with the RFC document, this module wins
and the document gets fixed.
"""

from k65p.core import Atom, SExpr, parse_k65p
from k65p.primes import GROUP, N_PRIMES, SYMBOL_TO_ID, symbol_for


class K65PResolveError(ValueError):
	"""An atom that cannot exist in K-65P (e.g. a prime id out of range)."""


# Valency frames, keyed by prime id: (min_args, max_args).
# Optional arguments may only be omitted from the right.
PREDICATES: dict[int, tuple[int, int]] = {
	21: (1, 3),  # DO: agent, action?, patient?
	22: (1, 2),  # HAPPEN: theme, experiencer?
	23: (1, 3),  # MOVE: theme, origin?, destination?
	24: (2, 2),  # TOUCH: agent, patient
	12: (1, 2),  # THINK: experiencer, content?
	13: (1, 2),  # KNOW: experiencer, content?
	14: (2, 2),  # WANT: experiencer, content
	15: (2, 2),  # FEEL: experiencer, state
	16: (1, 2),  # SEE: experiencer, theme?
	17: (1, 2),  # HEAR: experiencer, theme?
	18: (2, 3),  # SAY: agent, content, addressee?
	25: (1, 2),  # EXIST: theme, place?
	27: (1, 2),  # LIVE: theme, place?
	28: (1, 1),  # DIE: theme
}

# Evaluators/descriptors as unary attribution predicates ("X is Y").
EVALUATORS: frozenset[int] = frozenset({8, 9, 10, 11, 26, 60, 61, 64})

# Unary operators over a clause: logical + spatio-temporal frames.
# DL-020 (3-sep): VERY (49) se une — el intensificador NSM opera sobre
# cláusulas atributivas: [very [small baby]] = "muy pequeño". Sin posición
# combinatoria para VERY, las distinciones graduales (very young vs young)
# no pueden producir huellas distintas.
UNARY: frozenset[int] = frozenset({44, 45, 46, 31, 30, 32, 37, 41, 40, 38, 39, 43, 49})

# Binary connectors, foreground-first (condition/cause/base always leads).
BINARY: frozenset[int] = frozenset({48, 47, 51})


def resolve_atom(atom: Atom) -> int | str:
	"""Resolve an atom to a prime id, the GROUP marker, or a lexicon word."""
	name = atom.name
	if name in {"G", "g"}:
		return GROUP
	if name.lstrip("-").isdigit():
		prime_id = int(name)
		if not 0 <= prime_id < N_PRIMES:
			raise K65PResolveError(f"prime id {prime_id} out of range 0..{N_PRIMES - 1}")
		return prime_id
	key = name.casefold()
	if key in SYMBOL_TO_ID:
		return SYMBOL_TO_ID[key]
	return key


def _resolve_tree(tree: SExpr) -> list | int | str:
	if isinstance(tree, Atom):
		return resolve_atom(tree)
	return [_resolve_tree(child) for child in tree]


def _atom_text(resolved: int | str) -> str:
	if isinstance(resolved, int):
		return str(resolved)
	return resolved


def linearize(tree: SExpr | str) -> str:
	"""Canonical (numeric) linear form: primes as ids, lexicon words as-is."""
	resolved = _resolve_tree(parse_k65p(tree) if isinstance(tree, str) else tree)

	def _walk(node: list | int | str) -> str:
		if isinstance(node, list):
			return "[" + " ".join(_walk(child) for child in node) + "]"
		return _atom_text(node)

	return _walk(resolved)


def render(tree: SExpr | str, lang: str) -> str:
	"""Rendering in one human language: primes as symbols, lexicon words as-is."""
	resolved = _resolve_tree(parse_k65p(tree) if isinstance(tree, str) else tree)

	def _walk(node: list | int | str) -> str:
		if isinstance(node, list):
			return "[" + " ".join(_walk(child) for child in node) + "]"
		if isinstance(node, int):
			return symbol_for(node, lang)
		return node

	return _walk(resolved)


def validate(tree: SExpr | str, lexicon: set[str] | None = None) -> list[str]:
	"""Validate a K-65P v0 expression. Returns error strings; empty = valid.

	Accepts canonical ids or any language rendering. If `lexicon` is given,
	atoms that are neither primes nor in the lexicon are reported.
	"""
	if isinstance(tree, str):
		try:
			tree = parse_k65p(tree)
		except SyntaxError as exc:
			return [str(exc)]

	errors: list[str] = []
	if isinstance(tree, Atom):
		return [f"root must be a clause, not the atom {tree.name!r}"]

	def _check_atom(atom: Atom, path: str) -> int | str | None:
		try:
			resolved = resolve_atom(atom)
		except K65PResolveError as exc:
			errors.append(f"{path}: {exc}")
			return None
		if lexicon is not None and isinstance(resolved, str) and resolved != GROUP and resolved not in lexicon:
			errors.append(f"{path}: word {resolved!r} not in the lexicon")
		return resolved

	def _check(node: SExpr, path: str) -> None:
		if isinstance(node, Atom):
			_check_atom(node, path)
			return
		if not node:
			errors.append(f"{path}: empty clause")
			return
		head, args = node[0], node[1:]
		if not isinstance(head, Atom):
			errors.append(f"{path}: operator must be an atom, not a clause")
			for index, arg in enumerate(args):
				_check(arg, f"{path}.{index}")
			return
		operator = _check_atom(head, path)
		if operator == GROUP:
			if not args:
				errors.append(f"{path}: group [G] without a head")
			for index, arg in enumerate(args):
				if isinstance(arg, Atom):
					_check_atom(arg, f"{path}.{index}")
				else:
					errors.append(f"{path}.{index}: group members must be atoms, not clauses")
			return
		if isinstance(operator, int):
			if operator in PREDICATES:
				low, high = PREDICATES[operator]
				if not low <= len(args) <= high:
					errors.append(f"{path}: {symbol_for(operator, 'en')} expects {low}-{high} arguments, got {len(args)}")
			elif operator in EVALUATORS:
				if len(args) != 1:
					errors.append(f"{path}: evaluator {symbol_for(operator, 'en')} is unary, got {len(args)}")
			elif operator in UNARY:
				if len(args) != 1:
					errors.append(f"{path}: operator {symbol_for(operator, 'en')} is unary, got {len(args)}")
				elif isinstance(args[0], Atom):
					errors.append(f"{path}: {symbol_for(operator, 'en')} operates on a clause, not the atom {args[0].name!r}")
			elif operator in BINARY:
				if len(args) != 2:
					errors.append(f"{path}: connector {symbol_for(operator, 'en')} is binary, got {len(args)}")
			else:
				errors.append(f"{path}: prime {symbol_for(operator, 'en')} is not an operator")
		elif operator is not None:
			# DL-018 (2026-09-02): las moléculas (palabras del léxico) valen
			# como cabezas UNARIAS — el mecanismo de compuesta/atribución.
			# [lobo peligro] = "un tipo de lobo, el peligroso" (compuesta, en
			# posición de átomo) o [peligro lobo] = "lobo está en peligro"
			# (predicación). La distinción es SEMÁNTICA (posición), no de
			# forma: la gramática solo exige exactamente 1 argumento.
			if len(args) != 1:
				errors.append(
					f"{path}: molecule head {operator!r} expects exactly 1 argument, got {len(args)}"
				)
		for index, arg in enumerate(args):
			_check(arg, f"{path}.{index}")

	_check(tree, "root")
	return errors


def is_valid(tree: SExpr | str, lexicon: set[str] | None = None) -> bool:
	return not validate(tree, lexicon=lexicon)
