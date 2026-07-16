# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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
### [NEW]
- Initial scaffold of the sovereign project.
