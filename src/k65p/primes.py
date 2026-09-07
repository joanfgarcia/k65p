"""The 65 semantic primes: the periodic table of K-65P.

The canonical form of K-65P is the numeric one — a prime is its id (0..64).
Every human language column here is a *rendering*: a mechanical, reversible
view generated from this table, legal for humans and never authoritative.

Multi-word symbols use underscores so every symbol is a single token
(display documents may show natural spacing; token forms live here).
"""

LANGUAGES: tuple[str, ...] = ("en", "es", "zh", "fr", "de")

# One row per prime id, columns in LANGUAGES order.
PRIMES: tuple[tuple[str, str, str, str, str], ...] = (
	("I", "yo", "我", "je", "ich"),
	("YOU", "tú", "你", "tu", "du"),
	("SOMEONE", "alguien", "某人", "quelqu'un", "jemand"),
	("PEOPLE", "gente", "人们", "les_gens", "Menschen"),
	("SOMETHING", "algo", "某事", "quelque_chose", "etwas"),
	("THING", "cosa", "东西", "chose", "Ding"),
	("BODY", "cuerpo", "身体", "corps", "Körper"),
	("PART", "parte", "部分", "partie", "Teil"),
	("GOOD", "bueno", "好", "bon", "gut"),
	("BAD", "malo", "坏", "mauvais", "schlecht"),
	("BIG", "grande", "大", "grand", "groß"),
	("SMALL", "pequeño", "小", "petit", "klein"),
	("THINK", "pensar", "想", "penser", "denken"),
	("KNOW", "saber", "知道", "savoir", "wissen"),
	("WANT", "querer", "想要", "vouloir", "wollen"),
	("FEEL", "sentir", "感觉", "sentir", "fühlen"),
	("SEE", "ver", "看见", "voir", "sehen"),
	("HEAR", "oír", "听见", "entendre", "hören"),
	("SAY", "decir", "说", "dire", "sagen"),
	("WORD", "palabra", "词", "mot", "Wort"),
	("TRUE", "verdad", "真", "vrai", "wahr"),
	("DO", "hacer", "做", "faire", "tun"),
	("HAPPEN", "pasar", "发生", "arriver", "geschehen"),
	("MOVE", "mover", "移动", "bouger", "bewegen"),
	("TOUCH", "tocar", "触摸", "toucher", "berühren"),
	("EXIST", "existir", "存在", "exister", "existieren"),
	("MINE", "mío", "我的", "le_mien", "mein"),
	("LIVE", "vivir", "活", "vivre", "leben"),
	("DIE", "morir", "死", "mourir", "sterben"),
	("WHEN", "cuándo", "什么时候", "quand", "wann"),
	("NOW", "ahora", "现在", "maintenant", "jetzt"),
	("BEFORE", "antes", "以前", "avant", "vorher"),
	("AFTER", "después", "以后", "après", "nachher"),
	("LONG_TIME", "mucho_tiempo", "很久", "longtemps", "lange_Zeit"),
	("SHORT_TIME", "poco_tiempo", "一会儿", "peu_de_temps", "kurze_Zeit"),
	("MOMENT", "momento", "时刻", "moment", "Moment"),
	("WHERE", "dónde", "哪里", "où", "wo"),
	("HERE", "aquí", "这里", "ici", "hier"),
	("ABOVE", "arriba", "上面", "au-dessus", "oben"),
	("BELOW", "abajo", "下面", "au-dessous", "unten"),
	("FAR", "lejos", "远", "loin", "weit"),
	("NEAR", "cerca", "近", "près", "nah"),
	("SIDE", "lado", "旁边", "côté", "Seite"),
	("INSIDE", "dentro", "里面", "dedans", "innen"),
	("NOT", "no", "不", "ne_pas", "nicht"),
	("MAYBE", "quizá", "也许", "peut-être", "vielleicht"),
	("CAN", "poder", "能", "pouvoir", "können"),
	("BECAUSE", "porque", "因为", "parce_que", "weil"),
	("IF", "si", "如果", "si", "wenn"),
	("VERY", "muy", "很", "très", "sehr"),
	("MORE", "más", "更多", "plus", "mehr"),
	("LIKE", "como", "像", "comme", "wie"),
	("THIS", "este", "这个", "ceci", "dies"),
	("SAME", "mismo", "同一个", "même", "gleich"),
	("OTHER", "otro", "另一个", "autre", "ander"),
	("ONE", "uno", "一", "un", "eins"),
	("TWO", "dos", "二", "deux", "zwei"),
	("SOME", "algunos", "一些", "quelques", "einige"),
	("ALL", "todo", "所有", "tout", "alle"),
	("MUCH", "mucho", "多", "beaucoup", "viel"),
	("HOT", "caliente", "热", "chaud", "heiß"),
	("COLD", "frío", "冷", "froid", "kalt"),
	("WATER", "agua_prima", "水", "eau", "Wasser"),
	("LIGHT", "luz", "光", "lumière", "Licht"),
	("DARK", "oscuro", "黑暗", "sombre", "dunkel"),
)

N_PRIMES = len(PRIMES)

# Structural group functor: not a prime, part of the syntax alphabet.
GROUP = "G"
NAME = "N"  # DL-021: marcador de nombre propio — [N partes...] = un símbolo
QMARK = "Q"  # DL-023: marcador de intención interrogativa — [Q cláusula].
# Su glifo diseñado arrastra la intención NSM: querer+saber (preguntar = querer saber)


def _build_symbol_map() -> dict[str, int]:
	"""Casefolded symbol -> prime id, across every language.

	The same word may appear in several languages only if it maps to the
	same prime (e.g. 'si' is IF in both Spanish and French). A conflicting
	duplicate would corrupt resolution, so it fails loudly at import time.
	"""
	mapping: dict[str, int] = {}
	for prime_id, row in enumerate(PRIMES):
		for symbol in row:
			key = symbol.casefold()
			if mapping.get(key, prime_id) != prime_id:
				raise ValueError(f"symbol {symbol!r} maps to primes {mapping[key]} and {prime_id}")
			mapping[key] = prime_id
	return mapping


SYMBOL_TO_ID: dict[str, int] = _build_symbol_map()


def symbol_for(prime_id: int, lang: str) -> str:
	"""Rendering of a prime id in one language."""
	if lang not in LANGUAGES:
		raise ValueError(f"unknown language {lang!r}; expected one of {LANGUAGES}")
	return PRIMES[prime_id][LANGUAGES.index(lang)]
