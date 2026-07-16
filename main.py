"""Command-line entry point for the K-65P toolchain.

Usage:
	python main.py validate "<expr>"
	python main.py canon    "<expr>"
	python main.py render   <lang> "<expr>"
"""

import sys

from k65p.validator import linearize, render, validate


def main() -> int:
	args = sys.argv[1:]
	if len(args) >= 2 and args[0] == "validate":
		errors = validate(args[1])
		for error in errors:
			print(error)
		print("valid K-65P" if not errors else f"{len(errors)} error(s)")
		return 0 if not errors else 1
	if len(args) >= 2 and args[0] == "canon":
		print(linearize(args[1]))
		return 0
	if len(args) >= 3 and args[0] == "render":
		print(render(args[2], args[1]))
		return 0
	print(__doc__)
	return 2


if __name__ == "__main__":
	sys.exit(main())
