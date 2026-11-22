"""Contenido original y básico; las frases no proceden de mangas comerciales."""
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Card:
    id: str
    kind: str
    level: int
    japanese: str
    spanish: str
    romaji: str
    note: str = ""


_KANA_ROWS = (
    ("あいうえお", "a i u e o"),
    ("かきくけこ", "ka ki ku ke ko"),
    ("さしすせそ", "sa shi su se so"),
    ("たちつてと", "ta chi tsu te to"),
    ("なにぬねの", "na ni nu ne no"),
    ("はひふへほ", "ha hi fu he ho"),
    ("まみむめも", "ma mi mu me mo"),
    ("やゆよ", "ya yu yo"),
    ("らりるれろ", "ra ri ru re ro"),
    ("わをん", "wa wo n"),
    ("がぎぐげご", "ga gi gu ge go"),
    ("ざじずぜぞ", "za ji zu ze zo"),
    ("だぢづでど", "da ji zu de do"),
    ("ばびぶべぼ", "ba bi bu be bo"),
    ("ぱぴぷぺぽ", "pa pi pu pe po"),
)

KANA = tuple(
    Card("h-" + char, "hiragana", 1 if row < 10 else 2, char, "", syllable)
    for row, (chars, sounds) in enumerate(_KANA_ROWS)
    for char, syllable in zip(chars, sounds.split())
)

_KANJI = (
    ("人", "persona", "hito", "También: jin, nin"),
    ("日", "día; sol", "hi", "También: nichi"),
    ("月", "luna; mes", "tsuki", "También: getsu"),
    ("火", "fuego", "hi", "También: ka"),
    ("水", "agua", "mizu", "También: sui"),
    ("木", "árbol", "ki", "También: moku"),
    ("金", "oro; dinero", "kane", "También: kin"),
    ("土", "tierra", "tsuchi", "También: do"),
    ("山", "montaña", "yama", "También: san"),
    ("川", "río", "kawa", "También: sen"),
    ("田", "campo de arroz", "ta", "También: den"),
    ("口", "boca", "kuchi", "También: kou"),
    ("目", "ojo", "me", "También: moku"),
    ("耳", "oreja", "mimi", "También: ji"),
    ("手", "mano", "te", "También: shu"),
    ("足", "pie; pierna", "ashi", "También: soku"),
    ("力", "fuerza", "chikara", "También: ryoku"),
    ("心", "corazón; mente", "kokoro", "También: shin"),
    ("上", "arriba", "ue", "También: jou"),
    ("下", "abajo", "shita", "También: ka"),
    ("中", "dentro; centro", "naka", "También: chuu"),
    ("大", "grande", "ookii", "También: dai"),
    ("小", "pequeño", "chiisai", "También: shou"),
    ("本", "libro; origen", "hon", "También: moto"),
    ("学", "estudio", "gaku", "En 学校: gakkou"),
    ("校", "escuela", "kou", "En 学校: gakkou"),
    ("生", "vida; nacer", "sei", "En 先生: sensei"),
    ("先", "antes; delante", "saki", "En 先生: sensei"),
    ("友", "amigo", "tomo", "En 友達: tomodachi"),
    ("女", "mujer", "onna", "También: jo"),
    ("男", "hombre", "otoko", "También: dan"),
    ("子", "niño", "ko", "También: shi"),
    ("名", "nombre", "na", "También: mei"),
    ("何", "qué", "nani", "También: nan"),
    ("今", "ahora", "ima", "También: kon"),
    ("時", "tiempo; hora", "toki", "También: ji"),
    ("行", "ir", "iku", "También: kou"),
    ("来", "venir", "kuru", "También: rai"),
    ("見", "ver", "miru", "También: ken"),
    ("聞", "oír; preguntar", "kiku", "También: bun"),
    ("言", "decir", "iu", "También: gen"),
    ("話", "hablar", "hanasu", "También: wa"),
    ("読", "leer", "yomu", "También: doku"),
    ("書", "escribir", "kaku", "También: sho"),
    ("食", "comer", "taberu", "También: shoku"),
    ("飲", "beber", "nomu", "También: in"),
    ("買", "comprar", "kau", "También: bai"),
    ("会", "encontrarse", "au", "También: kai"),
    ("出", "salir", "deru", "También: shutsu"),
    ("入", "entrar", "hairu", "También: nyuu"),
    ("家", "casa", "ie", "También: ka"),
    ("国", "país", "kuni", "También: koku"),
    ("道", "camino", "michi", "También: dou"),
    ("車", "vehículo", "kuruma", "También: sha"),
    ("電", "electricidad", "den", "En 電車: densha"),
    ("気", "ánimo; energía", "ki", "En 元気: genki"),
    ("元", "origen", "gen", "En 元気: genki"),
    ("新", "nuevo", "atarashii", "También: shin"),
    ("古", "antiguo", "furui", "También: ko"),
    ("白", "blanco", "shiro", "También: haku"),
    ("黒", "negro", "kuro", "También: koku"),
    ("赤", "rojo", "aka", "También: seki"),
    ("青", "azul", "ao", "También: sei"),
    ("雨", "lluvia", "ame", "También: u"),
    ("空", "cielo", "sora", "También: kuu"),
    ("夜", "noche", "yoru", "También: ya"),
    ("朝", "mañana", "asa", "También: chou"),
    ("王", "rey", "ou", "Frecuente en fantasía"),
    ("魔", "demonio; magia", "ma", "En 魔法: mahou"),
    ("法", "método; ley", "hou", "En 魔法: mahou"),
    ("剣", "espada", "ken", "También: tsurugi"),
    ("敵", "enemigo", "teki", "Frecuente en acción"),
    ("命", "vida; destino", "inochi", "También: mei"),
    ("強", "fuerte", "tsuyoi", "También: kyou"),
    ("弱", "débil", "yowai", "También: jaku"),
)
KANJI = tuple(Card("k-" + jp, "kanji", 2 if i < 34 else 3, jp, es, ro, note)
              for i, (jp, es, ro, note) in enumerate(_KANJI))

_VOCAB = (
    ("こんにちは", "hola", "konnichiwa", "Saludo de día"),
    ("ありがとう", "gracias", "arigatou", ""),
    ("ごめん", "perdón", "gomen", "Informal"),
    ("はい", "sí", "hai", ""),
    ("いいえ", "no", "iie", ""),
    ("私", "yo", "watashi", ""),
    ("あなた", "tú", "anata", "Puede omitirse"),
    ("友達", "amigo", "tomodachi", ""),
    ("先生", "profesor", "sensei", ""),
    ("学校", "escuela", "gakkou", ""),
    ("本", "libro", "hon", ""),
    ("漫画", "manga", "manga", "Historieta japonesa"),
    ("猫", "gato", "neko", ""),
    ("犬", "perro", "inu", ""),
    ("家", "casa", "ie", ""),
    ("水", "agua", "mizu", ""),
    ("ご飯", "comida; arroz cocido", "gohan", ""),
    ("今日", "hoy", "kyou", ""),
    ("明日", "mañana", "ashita", ""),
    ("昨日", "ayer", "kinou", ""),
    ("今", "ahora", "ima", ""),
    ("ここ", "aquí", "koko", ""),
    ("そこ", "ahí", "soko", ""),
    ("どこ", "dónde", "doko", ""),
    ("何", "qué", "nani", ""),
    ("誰", "quién", "dare", ""),
    ("なぜ", "por qué", "naze", ""),
    ("大丈夫", "está bien", "daijoubu", "Puede ser pregunta o afirmación"),
    ("元気", "bien; con energía", "genki", ""),
    ("好き", "gustar", "suki", "Se usa con が"),
    ("嫌い", "desagradar", "kirai", ""),
    ("怖い", "dar miedo", "kowai", ""),
    ("強い", "fuerte", "tsuyoi", ""),
    ("弱い", "débil", "yowai", ""),
    ("速い", "rápido", "hayai", ""),
    ("遅い", "lento", "osoi", ""),
    ("見る", "ver", "miru", ""),
    ("読む", "leer", "yomu", ""),
    ("行く", "ir", "iku", ""),
    ("来る", "venir", "kuru", ""),
    ("待つ", "esperar", "matsu", ""),
    ("食べる", "comer", "taberu", ""),
    ("飲む", "beber", "nomu", ""),
    ("逃げる", "huir", "nigeru", ""),
    ("戦う", "luchar", "tatakau", ""),
    ("助ける", "ayudar", "tasukeru", ""),
    ("守る", "proteger", "mamoru", ""),
    ("敵", "enemigo", "teki", ""),
    ("仲間", "compañero", "nakama", "De un grupo"),
    ("魔法", "magia", "mahou", ""),
    ("剣", "espada", "ken", ""),
    ("勇者", "héroe", "yuusha", "Fantasía"),
    ("約束", "promesa", "yakusoku", ""),
    ("秘密", "secreto", "himitsu", ""),
    ("本当", "verdad", "hontou", ""),
    ("嘘", "mentira", "uso", ""),
    ("まさか", "no puede ser", "masaka", "Sorpresa"),
    ("やめて", "para", "yamete", "Orden informal"),
    ("急いで", "date prisa", "isoide", ""),
    ("危ない", "peligroso", "abunai", "Advertencia"),
    ("すごい", "increíble", "sugoi", ""),
    ("かわいい", "lindo", "kawaii", ""),
    ("うるさい", "ruidoso", "urusai", "Puede ser brusco"),
    ("行こう", "vamos", "ikou", "Invitación informal"),
    ("帰る", "volver a casa", "kaeru", ""),
    ("知る", "saber", "shiru", ""),
    ("分かる", "entender", "wakaru", ""),
    ("できる", "poder hacer", "dekiru", ""),
    ("終わり", "fin", "owari", ""),
)
VOCAB = tuple(Card("v-" + jp, "vocabulario", 2 if i < 36 else 3, jp, es, ro, note)
              for i, (jp, es, ro, note) in enumerate(_VOCAB))

@dataclass(frozen=True)
class Scene:
    title: str
    lines: Tuple[Tuple[str, str, str, str], ...]


SCENES = (
    Scene("El gato perdido", (
        ("猫はどこ？", "¿Dónde está el gato?", "neko wa doko?", "は marca el tema y se pronuncia wa."),
        ("ここにいるよ。", "Está aquí.", "koko ni iru yo", "いる expresa existencia de seres vivos."),
        ("よかった！", "¡Qué alivio!", "yokatta!", "Reacción frecuente en diálogos."),
    )),
    Scene("Antes de la batalla", (
        ("敵が来る！", "¡Viene el enemigo!", "teki ga kuru!", "が señala quién realiza la acción."),
        ("みんな、逃げて！", "¡Todos, huyan!", "minna, nigete!", "Forma て para pedir una acción."),
        ("私が守る。", "Yo los protegeré.", "watashi ga mamoru", "El presente japonés puede expresar futuro."),
    )),
    Scene("Un libro misterioso", (
        ("これは何？", "¿Qué es esto?", "kore wa nani?", "これ significa esto."),
        ("古い本だ。", "Es un libro antiguo.", "furui hon da", "だ es una cópula informal."),
        ("読んでみよう。", "Intentemos leerlo.", "yonde miyou", "〜てみる significa intentar hacer algo."),
    )),
)

ALL_CARDS = KANA + KANJI + VOCAB

