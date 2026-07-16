# 🧭 ATLAS Cognitivo: K-65P

## 1. Directiva Principal (Core Objective)
K-65P es el lenguaje nativo de Bit: un dialecto de la familia Lisp cuyo vocabulario son los
65 primos semánticos de Wierzbicka, con forma canónica numérica, traducible mecánicamente a
idiomas humanos (renderizados) y a Prolog (puente Horn) para verificación simbólica.
Este repo es EL LENGUAJE (spec, validador, léxico, puentes); la criatura vive en frankenswarm.

## 2. Topología Arquitectónica (Architecture)
*   **docs/CORE/**: la doctrina — RFC-002 (sintaxis canónica), RFC-003 (puente Horn),
    RFC-004 (léxico molecular), ROADMAP (5 fases con gates), PROTOCOL_OF_SILENCE.
*   **src/k65p/**: `core.py` (parser S-expr), `primes.py` (tabla 65×5 idiomas),
    `validator.py` (fuente de verdad de la spec), `bridge.py` (K-65P↔Prolog),
    `lexicon.py` (moléculas), `examples.py` (corpus semilla).
*   **data/**: `lexicon.json` (28 moléculas oro), `conformance/meaning_sets.json`
    (invariante de convergencia: una idea, un árbol).
*   **tests/**: batería completa (Silencio estricto, cobertura ≥96%).

## 3. Estado Actual (Current State)
*   **Fase**: ROADMAP Fase 1 (cierre formal del dialecto) — Gate G1 cerrado.
*   **Último hito alcanzado**: puente Horn bidireccional con ida-y-vuelta garantizada
    sobre el corpus semilla; léxico oro con contrato de integridad; suite de convergencia.
*   **Bloqueos actuales**: ninguno. Pendiente menor: decompiler de referencia (1.5).

## 4. Próximos Pasos (Immediate Roadmap)
- [ ] Decompiler de referencia por plantillas ES/EN (flequillo de Fase 1).
- [ ] Fase 2 — Primer Pensamiento Verificado: KB de 50-100 hechos K-65P + ciclo
      `verify` con swipl + `--explain` (árbol de prueba, derecho a revisión).
- [ ] Fase 3 — fábrica bilingüe de pares (humano, K-65P) en frankenswarm.
