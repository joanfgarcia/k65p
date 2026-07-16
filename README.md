# 🧩 K-65P: Kernel of 65 Primes (K-65 Primos)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Protocol: Silence](https://img.shields.io/badge/Protocol-Silence-orange.svg)](docs/CORE/PROTOCOL_OF_SILENCE.md)

> **"We have been reading the paintings that others have left on the rocks..."**  
> K-65P is a dialect of the Lisp family whose vocabulary is bound to Anna Wierzbicka's Natural Semantic Metalanguage (NSM) primes, designed to run on a connectionist ternary sustrato (**BitNet**) through our cognitive model (**Bit**) and verified by a symbolic reasoning engine (**Prolog**).

---

## 1. The Core Vision: The Dartmouth-NSM Convergence

For decades, Artificial Intelligence has suffered from a fundamental split:
* **The Symbolic Path (GOFAI, McCarthy, Colmerauer)**: Rigorous, exact, and auditably checkable. But rigid, brittle, and unable to learn or scale under noise.
* **The Connectionist Path (LLMs, Deep Learning)**: Flexible, highly capable, and robust under noise. But opaque, unverifiable, and computationally bloated.

**K-65P merges these worlds.** It recognizes that Wierzbicka's 65 semantic primes (the foundational atoms of human thought) and John McCarthy's LISP S-Expressions (the mathematical representation of computation) are structurally isomorphic.

By constraining the vocabulary of an ultra-efficient ternary network (**BitNet**) to these 65 universal primes, we bypass the need for a model to learn thousands of natural languages' grammars. The AI (**Bit**) thinks in K-65P; compilers and decompilers translate to human tongues.

---

## 2. The Chemical Analogy of Meaning

Meaning in K-65P is represented structurally like physical chemistry:
*   **Atoms**: The 65 universal semantic primes (Wierzbicka's NSM). Examples: `I`, `YOU`, `WANT`, `GOOD`, `BAD`.
*   **Molecules**: Single concepts defined as 65-trit vectors $\in \{-1, 0, 1\}^{65}$ (e.g., `fire` is a molecule containing the active atoms `LIGHT`, `HOT`, and `BAD`).
*   **Compounds**: Nested S-expressions formed by concatenating molecules to represent rules, statements, or reasoning flows (e.g., `[IF [TOUCH SOMEONE FIRE] [HAPPEN SOMETHING BAD]]`).

---

## 3. Disentangling Bit and BitNet

We keep a clear distinction in our nomenclature:
*   **BitNet**: The 1.58-bit ternary quantization architecture introduced by Microsoft Research (BitNet b1.58). Our sustrato is an independent, from-scratch implementation of that architecture — hardware-friendly and MatMul-free, but not Microsoft's framework.
*   **Bit**: The specific cognitive agent model we train sequentially through the Sovereign School developmental curriculum on top of the K-65P semantic glyph structure.

---

## 4. Cognitive Architecture (System 1 & System 2)

K-65P splits cognition into two collaborative velocities:
* **System 1 (Neural Interpreter - Bit)**: A ternary-quantized interpreter that evaluates K-65P S-Expressions heuristically, generating logical proposals instantly. Bit grows by pain-driven neurogenesis, so any hand-written parameter count is stale by design — the living figure is in the Sovereign School state (`frankenswarm: school_state.json`).
* **System 2 (Symbolic Solver - Prolog)**: A formal reasoning solver (`PrologExpert`) that verifies System 1 proposals against a local Knowledge Base using pattern matching and resolution.

---

## 5. The Canonical Form (read this before writing K-65P)

**The canonical form of K-65P is numeric** — a prime is its id (0..64). Human languages are
mechanical, reversible *renderings* resolved through the 65-prime table; they exist so a human
can follow an example without memorizing the table, and they are never authoritative.
`[si ...]`, `[IF ...]` and `[48 ...]` are the same compound, and the reference validator
accepts all three. Every documented example follows the `Code:` + renderings block convention
and is generated with the toolchain:

```bash
python main.py validate "[si [tocar alguien fuego] [pasar [G algo malo] alguien]]"
python main.py canon    "[IF [TOUCH SOMEONE fuego] [HAPPEN [G SOMETHING BAD] SOMEONE]]"
python main.py render zh "[48 [24 2 60] [22 4 9]]"
```

Full specification: [RFC-002 K-65P Canonical Syntax](docs/CORE/RFC-002_K65P_SYNTAX.md).

## 6. Getting Started

Check the core documents to dive into the architecture and conventions:
* [Roadmap: from dialect to native mind](docs/CORE/ROADMAP.md)
* [RFC-002: Canonical Syntax & Reference Validator](docs/CORE/RFC-002_K65P_SYNTAX.md)
* [RFC-003: The Horn Bridge (K-65P ↔ Prolog)](docs/CORE/RFC-003_HORN_BRIDGE.md)
* [RFC-004: The Molecular Lexicon](docs/CORE/RFC-004_MOLECULAR_LEXICON.md)
* [Architecture Specifications](docs/CORE/ARCHITECTURE.md)
* [Coding Conventions](CONVENTIONS.md)
* [Protocol of Silence](docs/CORE/PROTOCOL_OF_SILENCE.md)
