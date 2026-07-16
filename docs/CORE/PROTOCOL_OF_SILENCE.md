# Protocol of Silence

> **Status**: Enforced — automatically, by `ruff check` and `tests/test_sound_of_silence.py`
> **Scope**: every line of code in this repository, whoever writes it — human or agent.
> *Silence is elegance.*

---

## 1. Why

This codebase is read by more agents than humans. For an agent, every line is context it
must load and reason about: noise in the code is noise in every future mind that touches it.
The protocol optimizes for **signal density** — a file should contain exactly what it does,
why it must be that way, and nothing else. A reader who finds a line should never have to
wonder whether it matters. It matters, or it is not there.

## 2. The Rules

| # | Rule | Standard |
|---|---|---|
| 1 | **Indentation** | Tabs only, never spaces. (YAML is the standard exception.) |
| 2 | **Dead code** | Forbidden. No commented-out blocks, no unreachable branches, no placeholder stubs, no decorative separator lines. If the validator makes a branch unreachable, the branch does not exist. |
| 3 | **Comments** | Only *why*, never *what*. A comment states a constraint the code cannot show (a collision escaped, an invariant preserved). Decision rationale belongs in the RFCs or the changelog, not inline. |
| 4 | **Imports** | Grouped stdlib → third-party → local; no mid-file module-level imports. |
| 5 | **Docstrings** | Required on public modules, classes and functions. Tab-indented. One honest sentence beats a template paragraph. |
| 6 | **Naming** | `lowercase_with_underscores` for code, `UPPERCASE.md` under `docs/`. Full conventions in `CONVENTIONS.md`. |
| 7 | **Examples in docs** | Generated with the toolchain, never hand-written (RFC-002 §0). A hand-written example is a lie waiting to happen. |
| 8 | **Coverage** | ≥96% enforced. An untested line is an unverified claim — and this is the repository of verifiable claims. |

## 3. Enforcement

- `ruff check src/ tests/` — style, imports, naming, simplification (config in `pyproject.toml`).
- `mypy src/` — types.
- `tests/test_sound_of_silence.py` — runs ruff *inside* the test suite: silence violations
  fail the build, locally and in CI, with no separate step to forget.
- `pytest --cov-fail-under=96` — the coverage gate.

## 4. Spirit

The protocol is not bureaucracy; it is the same doctrine the language itself follows.
K-65P has no ambient ambiguity — every token earns its position. The code that implements
it holds itself to the identical standard: no ambient noise, every line earns its place.
The language and its house are built from the same material.
