from typing import Any


class Atom:
	"""Represents a semantic prime or basic symbol in K-65P."""

	def __init__(self, name: str) -> None:
		self.name = name.strip()

	def __repr__(self) -> str:
		return self.name

	def __eq__(self, other: Any) -> bool:
		if not isinstance(other, Atom):
			return False
		return self.name == other.name


# An S-Expression in K-65P can be an Atom or a List of S-Expressions
SExpr = Atom | list[Any]


def parse_k65p(text: str) -> SExpr:
	"""Parses a K-65P S-expression string into Atoms and lists.

	Supports bracket syntax [a b c] and parenthesis syntax (a b c).
	"""
	text = text.replace("[", " ( ").replace("]", " ) ")
	text = text.replace("(", " ( ").replace(")", " ) ")
	tokens = text.split()

	def read_from_tokens(token_list: list[str]) -> SExpr:
		if not token_list:
			raise SyntaxError("Unexpected EOF while reading S-expression")
		token = token_list.pop(0)
		if token == "(":
			lst = []
			while token_list and token_list[0] != ")":
				lst.append(read_from_tokens(token_list))
			if not token_list:
				raise SyntaxError("Expected ')' or ']', got EOF")
			token_list.pop(0)  # pop ')'
			return lst
		elif token == ")":
			raise SyntaxError("Unexpected ')' or ']'")
		else:
			return Atom(token)

	parsed = read_from_tokens(tokens)
	if tokens:
		raise SyntaxError("Extra tokens after S-expression")
	return parsed
