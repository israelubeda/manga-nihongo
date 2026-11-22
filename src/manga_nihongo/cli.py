"""Interfaz sencilla para Termux y otras terminales UTF-8."""
import argparse
import sys
from typing import List

from .data import ALL_CARDS, SCENES, Card
from .engine import Progress, correct, eligible, make_session, prompt, solution

try:
    import color_latam
except ImportError:
    color_latam = None


def paint(text: str, color: str, bold: bool = False) -> str:
    if color_latam is None or not sys.stdout.isatty():
        return text
    return color_latam.colorear(text, color, negrita=bold)


def say(text: str = "", color: str = "blanco", bold: bool = False) -> None:
    print(paint(text, color, bold))


def ask(text: str) -> str:
    return input(paint(text, "cian")).strip()


def section(title: str) -> None:
    say("\n" + "━" * 38, "magenta")
    say(title, "amarillo", True)
    say("━" * 38, "magenta")


def lesson(kind: str, level: int, page: int = 0) -> None:
    cards = eligible(kind, level)
    per_page = 12
    if not cards:
        say("No hay tarjetas en esta selección.", "amarillo")
        return
    pages = (len(cards) + per_page - 1) // per_page
    page = max(0, min(page, pages - 1))
    while True:
        section("Lección: {} · página {}/{}".format(kind, page + 1, pages))
        for card in cards[page * per_page:(page + 1) * per_page]:
            meaning = " · " + card.spanish if card.spanish else ""
            say("{:<12}  {:<18}{}".format(card.japanese, card.romaji, meaning))
            if card.note:
                say("  ↳ " + card.note, "azul")
        say("[s]iguiente  [a]nterior  [p]racticar  [q] salir", "cian")
        choice = ask("> ").lower()
        if choice == "s":
            page = min(page + 1, pages - 1)
        elif choice == "a":
            page = max(page - 1, 0)
        elif choice == "p":
            practice(cards[page * per_page:(page + 1) * per_page], 10, Progress())
        elif choice in ("q", "", "0"):
            return


def practice(cards: List[Card], count: int, progress: Progress,
             review_only: bool = False) -> None:
    pairs = make_session(cards, count, progress, review_only)
    if not pairs:
        say("No hay repasos pendientes. Prueba una práctica nueva.", "verde")
        return
    section("Repaso" if review_only else "Práctica")
    say("Escribe ? para una pista, / para saltar o q para salir.", "azul")
    hits = 0
    completed = 0
    for card, direction in pairs:
        say("\n{}/{} · {} · nivel {}".format(completed + 1, len(pairs), card.kind, card.level), "magenta")
        say(prompt(card, direction), "amarillo", True)
        answer = ask("> ")
        if answer.lower() == "q":
            break
        if answer == "?":
            say("Pista: " + (card.note or "Empieza con " + solution(card, direction)[:1]), "azul")
            answer = ask("> ")
        if answer.lower() == "q":
            break
        if answer == "/":
            say("Solución: " + solution(card, direction), "amarillo")
            progress.record(card, direction, False)
        else:
            ok = correct(card, direction, answer)
            hits += int(ok)
            progress.record(card, direction, ok)
            say("¡Correcto!" if ok else "Respuesta: " + solution(card, direction),
                "verde" if ok else "rojo", True)
        if card.note:
            say(card.note, "azul")
        completed += 1
    say("\nResultado: {}/{} aciertos".format(hits, completed), "cian", True)


def reading() -> None:
    section("Lectura de escenas originales")
    for i, scene in enumerate(SCENES, 1):
        say("{}. {}".format(i, scene.title))
    choice = ask("Escena (0 para volver): ")
    if not choice.isdigit() or not 1 <= int(choice) <= len(SCENES):
        return
    scene = SCENES[int(choice) - 1]
    section(scene.title)
    for jp, es, romaji, note in scene.lines:
        say("\n" + jp, "amarillo", True)
        ask("Enter para revelar... ")
        say(romaji + "  ·  " + es, "verde")
        say(note, "azul")


def search() -> None:
    term = ask("Busca japonés, español o romaji: ").casefold()
    if not term:
        return
    found = [c for c in ALL_CARDS if term in (c.japanese + c.spanish + c.romaji).casefold()]
    section("Diccionario · {} resultados".format(len(found)))
    for card in found[:30]:
        say("{} · {} · {} [{}]".format(card.japanese, card.romaji, card.spanish or "hiragana", card.kind))
    if len(found) > 30:
        say("Se muestran los primeros 30. Afina la búsqueda.", "azul")


def stats(progress: Progress) -> None:
    data = progress.summary()
    section("Tu progreso")
    for label, key in (("Tarjetas/direcciones practicadas", "practicadas"),
                       ("Intentos", "intentos"), ("Aciertos", "aciertos"),
                       ("Repasos pendientes", "pendientes")):
        say("{}: {}".format(label, data[key]))
    if data["intentos"]:
        say("Precisión: {:.0f}%".format(100 * data["aciertos"] / data["intentos"]), "verde")
    say("Guardado en " + str(progress.path), "azul")


def menu(progress: Progress) -> None:
    while True:
        section("漫画 NIHONGO · del hiragana al manga")
        say("1. Hiragana  2. Kanji  3. Vocabulario  4. Escenas")
        say("5. Práctica mixta  6. Repaso pendiente  7. Diccionario")
        say("8. Progreso  0. Salir")
        choice = ask("> ")
        if choice in ("1", "2", "3"):
            lesson({"1": "hiragana", "2": "kanji", "3": "vocabulario"}[choice], 3)
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
    args = parser.parse_args(argv)
    try:
        progress = Progress()
        if args.practicar or args.repasar:
            practice(eligible(args.practicar or "todos", args.nivel), args.cantidad,
                     progress, args.repasar)
        else:
            menu(progress)
    except (KeyboardInterrupt, EOFError):
        say("\nHasta pronto. またね！", "cian")


if __name__ == "__main__":
    main()

