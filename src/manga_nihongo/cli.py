"""Interfaz sencilla para Termux y otras terminales UTF-8."""
import argparse
import os
import shutil
import sys
import unicodedata
from typing import List

from .data import ALL_CARDS, SCENES, Card
from .engine import Progress, correct, eligible, make_session, prompt, solution

try:
    import color_latam
except ImportError:
    color_latam = None


PALETTE = {"acento": "#B799FF", "cian": "#70D9D2", "oro": "#FFD38A",
           "verde": "#91E6B1", "rojo": "#FF8D9A", "suave": "#AAB2C7",
           "blanco": "#F4F4FA"}
COLOR_ENABLED = True


def width() -> int:
    return max(24, min(76, shutil.get_terminal_size((56, 20)).columns - 2))


def visual_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def fit(text: str, limit: int) -> str:
    if visual_width(text) <= limit:
        return text
    result = ""
    for char in text:
        if visual_width(result + char + "…") > limit:
            break
        result += char
    return result + "…"


def wrapped(text: str, limit: int) -> List[str]:
    lines: List[str] = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if current and visual_width(candidate) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    lines.append(current)
    return [fit(line, limit) for line in lines]


def paint(text: str, color: str = "blanco", bold: bool = False) -> str:
    if color_latam is None or not COLOR_ENABLED or not sys.stdout.isatty() or os.getenv("NO_COLOR"):
        return text
    return color_latam.color_hex(text, PALETTE[color], negrita=bold)


def say(text: str = "", color: str = "blanco", bold: bool = False) -> None:
    print(paint(text, color, bold))


def ask(text: str) -> str:
    return input(paint("  " + text + " › ", "cian", True)).strip()


def section(title: str) -> None:
    if sys.stdout.isatty() and os.getenv("TERM") != "dumb":
        print("\033[2J\033[H", end="")
    else:
        print()
    say("  " + fit("漫画  M A N G A   N I H O N G O", width() - 2), "acento", True)
    say("  " + "─" * min(37, width() - 2), "suave")
    say("  " + fit(title.upper(), width() - 2), "oro", True)
    say()


def panel(title: str, lines: List[str], color: str = "acento") -> None:
    inside = width() - 4
    say("╭" + "─" * (inside + 2) + "╮", color)
    label = fit(title, inside)
    print(paint("│ ", color) + paint(label, "oro", True)
          + " " * (inside - visual_width(label)) + paint(" │", color))
    say("├" + "─" * (inside + 2) + "┤", color)
    for line in lines:
        for part in wrapped(line, inside):
            print(paint("│ ", color) + part
                  + " " * (inside - visual_width(part)) + paint(" │", color))
    say("╰" + "─" * (inside + 2) + "╯", color)


def progress_bar(done: int, total: int) -> str:
    filled = round(16 * done / max(1, total))
    return "━" * filled + "·" * (16 - filled)


def menu_item(number: str, title: str, detail: str) -> None:
    print(paint("  " + number + "  ", "cian", True) + paint(title, "blanco", True))
    for part in wrapped(detail, width() - 6):
        say("      " + part, "suave")


def lesson(kind: str, level: int, progress: Progress, page: int = 0) -> None:
    cards = eligible(kind, level)
    per_page = 8
    if not cards:
        say("No hay tarjetas en esta selección.", "oro")
        return
    pages = (len(cards) + per_page - 1) // per_page
    page = max(0, min(page, pages - 1))
    while True:
        section("{}  ·  página {}/{}".format(kind, page + 1, pages))
        subset = cards[page * per_page:(page + 1) * per_page]
        for card in subset:
            meaning = " · " + card.spanish if card.spanish else ""
            for part in wrapped("{}  /  {}{}".format(card.japanese, card.romaji, meaning), width() - 2):
                say("  " + part, "blanco", True)
            if card.note:
                for part in wrapped("↳ " + card.note, width() - 6):
                    say("      " + part, "suave")
        say()
        say("  [s] siguiente   [a] anterior", "cian")
        say("  [p] practicar esta página   [q] volver", "cian")
        choice = ask("Opción").lower()
        if choice == "s":
            page = min(page + 1, pages - 1)
        elif choice == "a":
            page = max(page - 1, 0)
        elif choice == "p":
            practice(subset, 10, progress)
        elif choice in ("q", "", "0"):
            return


def practice(cards: List[Card], count: int, progress: Progress,
             review_only: bool = False) -> None:
    pairs = make_session(cards, count, progress, review_only)
    if not pairs:
        section("Repaso al día")
        panel("¡BIEN HECHO!", ["No hay tarjetas pendientes por ahora."], "verde")
        ask("Enter para volver")
        return
    hits = 0
    completed = 0
    labels = {"romaji": "LECTURA EN ROMAJI", "es_jp": "ESPAÑOL → JAPONÉS",
              "jp_es": "JAPONÉS → ESPAÑOL"}
    for card, direction in pairs:
        section("{}  ·  {}/{}".format("Repaso" if review_only else "Práctica",
                                     completed + 1, len(pairs)))
        say("  " + progress_bar(completed, len(pairs)), "acento")
        say("  {}  ·  nivel {}".format(card.kind, card.level), "suave")
        say("  " + labels[direction], "cian", True)
        say()
        panel("TU RETO", [prompt(card, direction)])
        say("  ? pista     / revelar     q salir", "suave")
        answer = ask("Tu respuesta")
        if answer.lower() == "q":
            break
        if answer == "?":
            say("  Pista: " + (card.note or "Empieza con " + solution(card, direction)[:1]), "oro")
            answer = ask("Tu respuesta")
        if answer.lower() == "q":
            break
        ok = answer != "/" and correct(card, direction, answer)
        hits += int(ok)
        progress.record(card, direction, ok)
        say()
        if ok:
            panel("¡CORRECTO!", [solution(card, direction)], "verde")
        else:
            panel("SIGUE PRACTICANDO", ["Respuesta: " + solution(card, direction)], "rojo")
        if card.note:
            say("  " + card.note, "suave")
        completed += 1
        if completed < len(pairs):
            ask("Enter para continuar")
    section("Sesión terminada")
    say("  " + progress_bar(completed, len(pairs)) + "  {} tarjetas".format(completed), "acento")
    say()
    panel("RESULTADO", ["{} de {} aciertos".format(hits, completed),
                        "Tu avance quedó guardado en el dispositivo."], "verde")
    ask("Enter para volver")


def reading() -> None:
    section("Escenas · lee antes de revelar")
    for i, scene in enumerate(SCENES, 1):
        menu_item("0" + str(i), scene.title, "{} viñetas".format(len(scene.lines)))
    say()
    choice = ask("Escena · 0 para volver")
    if not choice.isdigit() or not 1 <= int(choice) <= len(SCENES):
        return
    scene = SCENES[int(choice) - 1]
    for i, (jp, es, romaji, note) in enumerate(scene.lines, 1):
        section("{}  ·  viñeta {}/{}".format(scene.title, i, len(scene.lines)))
        panel("LEE EN JAPONÉS", [jp])
        ask("Enter para revelar")
        panel("SIGNIFICADO", [romaji, es], "verde")
        say("  " + note, "suave")
        ask("Enter para continuar")


def search() -> None:
    section("Diccionario")
    say("  Busca japonés, español o romaji.", "suave")
    term = ask("Buscar").casefold()
    if not term:
        return
    found = [c for c in ALL_CARDS if term in (c.japanese + c.spanish + c.romaji).casefold()]
    section("{} resultados para «{}»".format(len(found), term))
    for card in found[:20]:
        say("  {}  /  {}".format(card.japanese, card.romaji), "blanco", True)
        say("    {}  ·  {}".format(card.spanish or "hiragana", card.kind), "suave")
    if len(found) > 20:
        say("  Se muestran 20. Afina la búsqueda.", "oro")
    ask("Enter para volver")


def stats(progress: Progress) -> None:
    data = progress.summary()
    section("Tu progreso")
    precision = round(100 * data["aciertos"] / data["intentos"]) if data["intentos"] else 0
    panel("RESUMEN", [
        "Tarjetas y direcciones: {}".format(data["practicadas"]),
        "Intentos: {}  ·  Aciertos: {}".format(data["intentos"], data["aciertos"]),
        "Precisión: {}%".format(precision),
        "Repasos pendientes: {}".format(data["pendientes"]),
    ])
    say("  Progreso guardado en " + str(progress.path), "suave")
    ask("Enter para volver")


def menu(progress: Progress) -> None:
    while True:
        data = progress.summary()
        section("Lee manga en japonés")
        panel("HOY", ["{} repasos pendientes  ·  {} aciertos acumulados".format(
            data["pendientes"], data["aciertos"])])
        say()
        menu_item("01", "Hiragana", "Reconoce y escribe sus sonidos")
        menu_item("02", "Kanji", "Significados y lecturas frecuentes")
        menu_item("03", "Vocabulario", "Palabras útiles para manga")
        menu_item("04", "Escenas", "Diálogos originales guiados")
        say("  " + "─" * min(35, width() - 2), "suave")
        menu_item("05", "Práctica mixta", "Japonés, español y romaji")
        menu_item("06", "Repaso pendiente", "Refuerza lo aprendido")
        menu_item("07", "Diccionario", "Busca una palabra")
        menu_item("08", "Mi progreso", "Estadísticas de estudio")
        say("  0   Salir", "suave")
        choice = ask("Elige una opción").lstrip("0") or "0"
        if choice in ("1", "2", "3"):
            lesson({"1": "hiragana", "2": "kanji", "3": "vocabulario"}[choice], 3, progress)
        elif choice == "4":
            reading()
        elif choice == "5":
            practice(eligible(), 15, progress)
        elif choice == "6":
            practice(eligible(), 15, progress, True)
        elif choice == "7":
            search()
        elif choice == "8":
            stats(progress)
        elif choice in ("0", "q"):
            return


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Aprende japonés para leer manga")
    parser.add_argument("--practicar", choices=["hiragana", "kanji", "vocabulario", "todos"])
    parser.add_argument("--repasar", action="store_true")
    parser.add_argument("--nivel", type=int, choices=[1, 2, 3], default=3)
    parser.add_argument("--cantidad", type=int, default=15)
    parser.add_argument("--sin-color", action="store_true", help="Desactiva colores ANSI")
    args = parser.parse_args(argv)
    global COLOR_ENABLED
    COLOR_ENABLED = not args.sin_color
    try:
        progress = Progress()
        if args.practicar or args.repasar:
            practice(eligible(args.practicar or "todos", args.nivel), args.cantidad,
                     progress, args.repasar)
        else:
            menu(progress)
    except (KeyboardInterrupt, EOFError):
        say("\n  Hasta pronto. またね！", "cian")


if __name__ == "__main__":
    main()

