# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### [ARCH]
- Phase 1 of the roadmap (dialect closure): RFC-003 Horn Bridge (K-65P ↔ Prolog, both directions, round-trip guaranteed over the seed corpus; executable form for the engine) and RFC-004 Molecular Lexicon (gold tier: the 28 hand-crafted survival molecules, integrity-checked).
- The Convergence Invariant seeded: `data/conformance/meaning_sets.json` (20 meaning sets, es/en/zh) with `test_conformance.py` asserting one idea, one tree.
### [ARCH]
- The canonical form of K-65P is settled as numeric (prime ids); human languages are mechanical renderings (RFC-002 v1, three-level documentation convention).
### [NEW]
- 65-prime multilingual table (`primes.py`: en/es/zh/fr/de) with conflict-checked symbol resolution.
- RFC-002 reference validator (`validator.py`): valency frames, groups, connectors — ported from frankenswarm and re-keyed by prime id; accepts any rendering.
- Toolchain CLI (`main.py`): `validate`, `canon`, `render <lang>` — documented examples are generated, never hand-written.
- RFC-002 v1 specification moves to its home (`docs/CORE/RFC-002_K65P_SYNTAX.md`).
### [FIX]
- CI/pytest could not import the package (missing `pythonpath`); the suite (61 tests, 99% coverage) now actually runs.
- README truths: living parameter count instead of a stale figure; exact BitNet attribution (independent implementation of Microsoft Research's architecture).
### [QA]
- `[FIRE HOT BAD]` demoted from blessed example to star negative test.
### [DOCS]
- `PROTOCOL_OF_SILENCE.md` written (it was an empty title): the eight rules, their enforcement, and their why.
- General consistency pass: `ARCHITECTURE.md` aligned with RFC-002 v1 (canonical examples, Horn bridge marked implemented, exact BitNet attribution), `.agent/ATLAS.md` filled with the real project atlas, `pyproject.toml` description de-placeholdered, ROADMAP Phase 1 status: Gate G1 closed (open remainder: reference decompiler).
### [NEW]
- Initial scaffold of the sovereign project.
