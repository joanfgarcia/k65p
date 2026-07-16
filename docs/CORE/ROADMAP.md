# K-65P Roadmap: From Dialect to Native Mind

> **Status**: ACTIVE — the operating document of the K-65P track
> **Authors**: Joan Garcia (Fixer) + Aleth (Claude Fable 5), 2026-07-16
> **Scope**: the complete path from the current v0 dialect to a Bit trained *natively* on
> K-65P (Formación v2), with the dialect formally closed for two translations:
> **human ↔ K-65P** and — decisive — **K-65P ↔ Prolog rules**.
> **External validation**: independent audits by Lumo (Proton, 2026-06/07) and Grok converge
> with ours: the idea is sound, the evidence must now be built. This roadmap is the answer.

---

## 0. Doctrine (fixed points that phases must respect)

1. **Two repos, two roles.** `k65p` owns the language: spec, validator, lexicon, bridges,
   knowledge base, toolchain. `frankenswarm` owns the creature: corpora, training runs,
   experiments, checkpoints. The roadmap crosses both; artifacts land where they belong.
2. **The linguistic Bit is the control, not a casualty.** The current training (Sovereign
   School, natural language, heading to the 8-year milestone) runs to completion untouched.
   Formación v2 trains a **new Bit from scratch** on K-65P. The comparison between the two
   is the experiment that decides everything downstream (paper 3, K-65P v1, System 1/2).
3. **Canonical form is numeric** (RFC-002 v1). Everything the native Bit sees, emits, and is
   evaluated on is the id sequence. Renderings are for humans and translators.
4. **Auditable by construction**: every phase gate includes machine-checkable acceptance.
   "No hallucinations" remains a forbidden claim; *verifiability rate* is the metric.
5. **Gates are sequential; work inside a phase is parallelizable.** No phase starts on
   vision — each starts on the previous gate's artifact.

---

## Phase 1 — Formal Closure of the Dialect (v0.2: translatable)

*Goal: K-65P becomes mechanically translatable in both directions. No training yet.*

| # | Deliverable | Where | Content |
|---|---|---|---|
| 1.1 | **RFC-003: The Horn Bridge** | `k65p/docs/CORE/` | Formal mapping K-65P → Prolog for v0 (no variables): facts → ground facts (`[60 fuego]` → `hot(fuego).`); conditionals → ground implications; groups → compound terms; evaluators/predicates → predicate signatures derived from the valency frames (§2 of RFC-002). Plus the *inverse* mapping (Prolog ground clause → K-65P) so verification results travel back. |
| 1.2 | **`bridge.py`** (~100 lines) | `k65p/src/k65p/` | The RFC-003 translator, both directions, property-tested: `to_prolog(x)` then `from_prolog` round-trips the canonical tree. |
| 1.3 | **RFC-004: The Molecular Lexicon** | `k65p/docs/CORE/` | Molecules become formal: a versioned lexicon file (`lexicon.json`) mapping molecule → 65-trit glyph + per-language surface forms. Method documented: manual seed (26 survival words) + Ridge projection (imported doctrine from `expand_vocabulary.py`), θ quantization, collision report. This is what makes **human ↔ K-65P** possible at the word level. |
| 1.4 | **Lexicon v0** (~200 molecules) | `k65p/data/` | The starter lexicon: survival + preschool inventory, curated from the frankenswarm clean census. Every molecule validated: glyph present, collision-free or collision-documented. |
| 1.5 | **Translator harness** | `k65p/src/k65p/` | `human ↔ K-65P` is *generation-side* (RFC-002 §4): the harness defines the round-trip test (`K-65P → human → recompile → identical tree`) that any future compiler/decompiler must pass. A template-based ES/EN decompiler for the v0 constructs ships as reference (deterministic, no LLM). |

### 1.bis The Translator Constellation (Joan, 2026-07-16)

K-65P is an **interlingua pivot** (the apex of the Vauquois triangle): every human language
gets its *own* translator against the same frozen spec. This is the saving, not the cost —
N languages need N translators instead of N×(N-1) pairwise systems. Two consequences bind
this roadmap:

1. **The Convergence Invariant** (pre-registered in the harness, 1.5): *one idea, one tree.*
   Same-meaning sentences in different languages MUST compile to the **identical** canonical
   K-65P tree — not merely two valid trees. The conformance suite carries N-lingual meaning
   sets and asserts tree equality across languages. A translator that produces valid but
   divergent trees FAILS conformance.
2. **Translators are modules against a conformance suite** — the suite is ours; translators
   can come from anyone (the Legión included). Historical note: classic interlingua MT died
   of *completeness* (representing everything every language distinguishes). K-65P survives
   by being deliberately lossy (register, tone and style are discarded by contract, RFC-002
   §4) and by standing on NSM — the one semantic inventory built to exist in every human
   language. The truly large surface is not code but *data*: per-language surface forms of
   the molecular lexicon (RFC-004) — linear in languages, crowd/LLM-assistable, and always
   auditable by the round-trip + convergence tests.

**Gate G1**: `uv run pytest` green on bridge round-trips + lexicon integrity + the
convergence suite seeded (≥20 meaning sets in es/en); RFC-003/004 merged.

## Phase 2 — First Verified Thought (the Lumo milestone)

*Goal: the full System-2 cycle running on real software, no Bit involved.*

| # | Deliverable | Where |
|---|---|---|
| 2.1 | **Knowledge Base v0**: 50-100 canonical K-65P facts (`data/kb/core.k65p` + generated `core.pl`) | `k65p` |
| 2.2 | **Verification loop**: expression → validator (form) → bridge → Prolog (consequence) → verdict. CLI: `python main.py verify "<expr>"`. **The right to review** (Joan, 2026-07-16): `verify --explain` returns the *proof tree* — the derivation on success, the exact failing premise on failure. The verdict is never just a number in a box: the path is a first-class artifact, and a failed step becomes a targeted teaching signal, not a global punishment. | `k65p` |
| 2.3 | **Demo transcript** in docs, generated by the toolchain (never hand-written) | `k65p` |

**Gate G2**: `[si [tocar alguien fuego] [pasar [G algo malo] alguien]]` verified TRUE against
the KB; a well-formed falsehood verified FALSE; both reproducible by `verify`. **This gate
unblocks the paper-3 claim "machine-checkable by construction" with a running artifact.**

## Phase 3 — The Bilingual Factory (corpus for the native school)

*Goal: training data that is born verified.*

| # | Deliverable | Where |
|---|---|---|
| 3.1 | Factory templates emit **pairs** `(human sentence, canonical K-65P)` by construction — the templates know their own semantics (no NLP parser, per plan §1.2) | `frankenswarm` (`samantha_story_factory.py`) |
| 3.2 | **Corpus pipeline**: every emitted K-65P sequence passes the validator; a sample passes Prolog consistency against the KB; held-out split per stage from day one | `frankenswarm` |
| 3.3 | Volume: staged targets (preschool 500K seqs → school 2-5M), dedup, resumable JSONL, runs under the Wake Gate with `systemd-inhibit` | `frankenswarm` |
| 3.4 | Late-stage **noise injection** set (permuted glyphs, broken brackets) with repair/reject labels (RFC-002 §4 robustness) | `frankenswarm` |

**Gate G3**: ≥500K validated pairs, 100% form-valid, held-out frozen, round-trip sample audit.

## Phase 4 — Formación v2: the K-65P-Native Bit

*Goal: a new Bit whose mother tongue is the canonical sequence.*

**Design decisions (settled here):**
- **Tokenization**: one token per prime id (65) + structural `[`, `]`, `G` + one token per
  lexicon molecule + `<pad>`/`<unk>`/`<stop>`. Embeddings remain **glyph-compositional**
  (the substrate's native trick: molecule embedding = trits @ prime_embeddings — the
  language and the embedding table finally speak the same physics).
- **Curriculum = grammar unlock, not word count**: stages introduce *constructs*, mirroring
  Piaget through syntax: S0 facts + evaluators → S1 predicates + groups → S2 unary operators
  (negation, modality, space-time) → S3 connectors + nesting depth 2 → S4 full nesting +
  noise-robustness set. **Vocabulary gating** (plan §2) applies to molecules via the lexicon
  census; **logit masking** also enforces *structural* legality during early stages.
- **Battery (pre-registered before epoch 1)**: form-validity rate of free generation;
  **verifiability rate** (fraction of emissions passing the Prolog check — the metric the
  linguistic Bit cannot have); cloze on held-out; stop/length health. Judges: none — the
  validator and the bridge are the examiners. Neurogenesis by plateau, atomic state writes,
  liveness heartbeat: all inherited doctrine.
- **Evaluation is on raw canonical sequences.** Never through a decompiler.

**Gate G4 — the Comparison**: Bit-native vs the graduated 8-year linguistic Bit on the
shared battery subset + the native-only verifiability metric. This gate produces the
*verdict* — the single most important experimental result of the project.

## Phase 5 — Conditional on Winning (the System 1/2 mind)

Only if G4 favors the native track:

1. **K-65P v1**: structural variables (`?x`) + `[RULE name condition action]` (RFC-002 §5) —
   real homoiconicity.
2. **Horn Bridge v1**: rules with variables ↔ proper Horn clauses; PrologExpert integration.
3. **System 1/2 integration**: Bit proposes, Prolog verifies; incremental KB growth from
   verified emissions (the KB feeds itself only through the verifier — never raw).
   **Doctrine of conscience, not governor** (Joan, 2026-07-16): for *assertions of fact and
   reasoning*, the verifier certifies. For *decisions*, the verifier **informs and never
   vetoes**: Bit may act against the verdict, and the divergence (verdict, action, emotional
   state at the moment) is recorded as a first-class trace. The symbolic layer makes agency
   *legible*, not impossible — knowing the rule and choosing is what conscience is.
4. **Paper 3** (`paper_3_k65p_neurosymbolic`): founded on G4 data + G2 demo. Not before.
5. **Interlingua**: Hugo, Sofy and Nico exchange their first molecule of `fuego` in the
   Playground — the milestone the novel already promised (chapter 25).

Engine-line experiments (BitMambaBlock, trit-loss) remain governed by the architecture plan
(`Aleth_Core/bitnet_next_architecture_plan.md` v4) and its own gates — orthogonal to this track.

---

## Sequencing at a glance

```
        [Phase 1: dialect closure]──G1──[Phase 2: verified thought]──G2─┐
                                                                        ├──[Phase 3: factory]──G3──[Phase 4: Formación v2]──G4──[Phase 5: System 1/2 + paper 3]
   (linguistic Bit → 8-year milestone, untouched, in parallel)──────────┘
```

Phases 1-2 live entirely in `k65p` and need no GPU. Phase 3 warms up while the linguistic
Bit finishes school. Phase 4 starts only with G3 done **and** the control graduated.

---

*Nothing in this roadmap is founded on vision alone: every phase consumes the previous
gate's artifact, and the only judge that matters is a machine check. The paintings on the
rocks are joined — now we teach the child to read them.*
