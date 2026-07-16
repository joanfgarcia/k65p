"""The RFC-002 §3 seed corpus: 20 hand-compiled examples (Spanish rendering).

Spec data, not test fixtures: every example is valid K-65P v0 by definition,
and every tool in the chain (validator, renderer, bridge) must agree on it.
"""

SEED_EXAMPLES: tuple[str, ...] = (
	"[ver yo algo]",
	"[oír tú agua]",
	"[caliente fuego]",
	"[malo [G fuego caliente]]",
	"[si [tocar alguien [G fuego caliente]] [pasar [G algo malo] alguien]]",
	"[porque [mover tú lejos] [sentir yo malo]]",
	"[querer yo agua]",
	"[querer yo [hacer yo beber agua]]",
	"[quizá [pasar lluvia]]",
	"[poder [mover yo]]",
	"[no [ver yo algo]]",
	"[saber yo [bueno agua]]",
	"[querer yo [decir tú verdad yo]]",
	"[vivir gente aquí]",
	"[antes [pequeño yo]]",
	"[después [pasar [G algo malo]]]",
	"[como [G cosa este] agua]",
	"[morir [G gente todo]]",
	"[porque [pensar yo] [existir yo]]",
	"[si [tocar tú [G agua frío]] [sentir tú frío]]",
)
