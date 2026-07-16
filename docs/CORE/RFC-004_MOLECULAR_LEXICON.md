# RFC-004: The Molecular Lexicon

> **Status**: ACTIVE (v0: gold tier) — reference implementation in `src/k65p/lexicon.py`,
> data in `data/lexicon.json`
> **Authors**: Joan Garcia + Aleth (Claude Fable 5), 2026-07-16
> **Source of truth**: the loader's integrity checks win over this document.

---

## 1. What a molecule is

Primes are the atoms; **molecules are named 65-trit glyphs** — compositions of atoms that
name a concept (`fuego` = `LIGHT+1, HOT+1, GOOD+1, BAD+1, SEE+1, DIE+1, SOMETHING+1`: useful
AND dangerous, the duality hand-carved into the trits). Molecules are the open part of the
vocabulary: primes are 65 forever; molecules grow with the creature's world.

## 2. The lexicon file

`data/lexicon.json`, versioned, one entry per molecule:

```json
"fuego": {"tier": "gold", "glyph": [65 trits], "renderings": {"es": "fuego"}}
```

- **`tier: gold`** — hand-crafted glyphs, semantically exact. v0 ships the 28 survival
  molecules (phases 0-3 of Bit's original world), imported verbatim from frankenswarm's
  `glyph_vocabulary.py` (provenance recorded in the file).
- **`tier: derived`** — Ridge-projected glyphs (method: manual seed + Ridge regression +
  θ-quantization, as documented in frankenswarm's `expand_vocabulary.py`). Derived entries
  arrive with the factory (ROADMAP Phase 3), flagged as such, with their collision report.
- **`renderings`** — per-language surface forms. This is where the *translator
  constellation* cost really lives (ROADMAP §1.bis): linear in languages, data not code,
  always auditable by the convergence suite.

## 3. Integrity contract (enforced by `load_lexicon`)

1. A molecule name may not collide with any prime symbol in any language (casefold).
2. A molecule name may not use a bridge-reserved name (`truth`, `not_`, `neg`, `implies`, `g`).
3. Every glyph has exactly 65 trits, each in {-1, 0, 1}.

`molecule_names()` feeds the validator's `lexicon=` argument: with it, K-65P certification
becomes closed-world — an atom is a prime, a molecule, or an error.

## 4. Growth discipline

Inherited from the School v3 census doctrine: molecules enter by **need** (the corpus or the
KB demands them), never by imported frequency lists — that road ends in a 57.8% ghost
vocabulary, and we have the scar to prove it. Every addition re-runs the integrity suite.
