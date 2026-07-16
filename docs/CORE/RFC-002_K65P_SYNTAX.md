# RFC-002: K-65P Canonical Syntax (v1)

> **Status**: ACTIVE — reference implementation in `src/k65p/validator.py`
> **Authors**: Joan Garcia + Aleth (Claude Fable 5 · original v0 spec; Aleth/antigravity · repo integration)
> **History**: v0 born 2026-07-08 in the frankenswarm laboratory (`docs/RFC-002_SINTAXIS_GLIFOS.md`,
> commits `0803f84`/`ceda7a6`); v1 moves the spec to its own home and settles the canonical form.
> **Source of truth**: on any discrepancy between this document and the validator, the validator
> wins and this document gets fixed.

---

## 0. The Canonical Form Decision (v1)

**The canonical form of K-65P is numeric.** A prime is its id (0..64). What Bit emits, what
travels between agents, what gets stored in a `.k65p` file, and the only thing the validator
certifies, is the id sequence:

```
[48 [24 2 [G fuego 60]] [22 [G 4 9] 2]]
```

Every human language is a **rendering**: a mechanical, reversible view resolved through the
65-prime table (`src/k65p/primes.py`). Renderings are legal, useful, and never authoritative —
like the disassembly of a binary. `[si ...]`, `[IF ...]` and `[48 ...]` are the *same compound*,
and the validator accepts all of them by resolving symbols to ids first.

**The three-level documentation convention** (mandatory in every K-65P document):

1. `Code:` line first — the canonical numeric form.
2. Language renderings below, labelled with their language code.
3. Example blocks are **generated with the toolchain** (`python main.py canon|render`), never
   hand-written. A hand-written example is a lie waiting to happen.

Lexicon words (molecules such as `fuego`) are not primes: they pass through renderings
unchanged. Their per-language rendering belongs to the lexicon layer, out of scope for v0/v1.

## 1. Grammar (BNF)

```bnf
sequence   ::= clause                       ; a complete utterance is a clause

expr       ::= atom | group | clause

group      ::= '[' 'G' atom modifier* ']'   ; nominal group: head + modifiers
modifier   ::= atom

clause     ::= '[' predicate expr{min..max} ']'   ; per valency frame (§2)
             | '[' evaluator expr ']'              ; attribution: "X is <evaluator>"
             | '[' unary_op clause ']'             ; NOT, MAYBE, CAN, spatio-temporal frames
             | '[' connector expr expr ']'         ; IF, BECAUSE, LIKE

atom       ::= prime_id | prime_symbol | lexicon_word
```

Hard rules:

- **Fixed positional order**: the role of every argument is determined by its position in the
  valency frame. No case markers, no prepositions.
- **No structural ellipsis**: optional arguments are omitted from the right only.
- **`G` requires a head**: `[G]` is illegal; group members must be atoms.
- **The root is a clause**: a bare atom or group is not a valid utterance.

## 2. Valency Frames (v0)

Derived from Goddard & Wierzbicka's canonical combinations. `?` = optional.

| Id | Prime | Frame (positional order) |
|---|---|---|
| 21 | `DO` | agent, action?, patient? |
| 22 | `HAPPEN` | theme, experiencer? |
| 23 | `MOVE` | theme, origin?, destination? |
| 24 | `TOUCH` | agent, patient |
| 12 | `THINK` | experiencer, content? |
| 13 | `KNOW` | experiencer, content? |
| 14 | `WANT` | experiencer, content |
| 15 | `FEEL` | experiencer, state |
| 16 | `SEE` | experiencer, theme? |
| 17 | `HEAR` | experiencer, theme? |
| 18 | `SAY` | agent, content, addressee? |
| 25 | `EXIST` | theme, place? |
| 27 | `LIVE` | theme, place? |
| 28 | `DIE` | theme |

**Evaluators/descriptors as unary attribution** ("X is Y"): `GOOD` 8, `BAD` 9, `BIG` 10,
`SMALL` 11, `MINE` 26, `HOT` 60, `COLD` 61, `DARK` 64. There is no copula prime and none is
invented: `[60 fuego]` *is* "fire is hot".

**Unary operators over a clause**: logical `NOT` 44, `MAYBE` 45, `CAN` 46; temporal frames
`BEFORE` 31, `NOW` 30, `AFTER` 32; spatial `HERE` 37, `NEAR` 41, `FAR` 40, `ABOVE` 38,
`BELOW` 39, `INSIDE` 43.

**Binary connectors** (foreground-first: condition/cause/base always leads): `IF` 48,
`BECAUSE` 47, `LIKE` 51.

## 3. Examples (generated with the toolchain)

```
Code:  [60 fuego]
en:    [HOT fuego]
es:    [caliente fuego]
zh:    [热 fuego]
```

```
Code:  [48 [24 2 [G fuego 60]] [22 [G 4 9] 2]]
en:    [IF [TOUCH SOMEONE [G fuego HOT]] [HAPPEN [G SOMETHING BAD] SOMEONE]]
es:    [si [tocar alguien [G fuego caliente]] [pasar [G algo malo] alguien]]
zh:    [如果 [触摸 某人 [G fuego 热]] [发生 [G 某事 坏] 某人]]
```

```
Code:  [47 [12 0] [25 0]]
en:    [BECAUSE [THINK I] [EXIST I]]
es:    [porque [pensar yo] [existir yo]]
zh:    [因为 [想 我] [存在 我]]
```

```
Code:  [14 0 [18 1 20 0]]
en:    [WANT I [SAY YOU TRUE I]]
es:    [querer yo [decir tú verdad yo]]
zh:    [想要 我 [说 你 真 我]]
```

The star negative: `[FIRE HOT BAD]` is **not** K-65P — `FIRE` is not an operator (it is not
even a prime; fire is a lexicon molecule). A list of molecules is not a clause. See
`tests/test_validator.py::test_fire_hot_bad_is_not_k65p`.

## 4. Verification Principles

- **Auditable by construction, not hallucination-free.** The neural engine (Bit) remains
  statistical and can emit well-formed falsehoods. What K-65P buys is that verification becomes
  computation: this validator checks *form*; a symbolic engine (`PrologExpert`) checks *logical
  consequence* against a knowledge base. Verifiable ≠ infallible — and verifiable is what no
  LLM over human text can offer. Claiming "no hallucinations" is forbidden in this project.
- **Round-trip invariant for translators**: `K-65P → human language → (recompile) → K-65P'`
  must return the identical canonical tree; otherwise the enrichment invented or destroyed
  meaning and the translator fails.
- **Evaluation of any K-65P-native model happens on raw canonical sequences**, never through a
  decompiler (otherwise you measure the translator, not the creature).

## 5. The v1 Horizon (proposed, not implemented)

Real homoiconicity (rules as first-class, manipulable data) requires exactly two extensions:

1. **Structural variables** with unification (wildcard prefix `?x` — hole syntax pending design).
2. **A rule functor**: `[RULE <name> <condition> <action>]`.

A K-65P rule with variables is, nearly character for character, a **Horn clause** — the bridge
to a Prolog engine is a mechanical translator (~100 lines) for the rule subset.

## 6. Known Limitations (v0)

1. No mood: neither imperative nor interrogative (`WHEN` 29 and `WHERE` 36 are reserved for
   interrogation in a future revision). Work around with `WANT` + clause.
2. No morphological plural: plurality is lexical (`ONE` 55, `TWO` 56, `SOME` 57, `ALL` 58,
   `MUCH` 59 as group modifiers).
3. Coarse time: only `BEFORE`/`NOW`/`AFTER` frames; no aspect.
4. Molecule (lexicon) rendering across languages is out of scope — molecules pass through
   renderings unchanged.
