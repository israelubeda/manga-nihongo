"""Selección de ejercicios, corrección y repaso espaciado."""
import json
import os
import random
import unicodedata
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .data import ALL_CARDS, Card


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().strip()
    # No descomponer japonés: NFD + quitar marcas fusionaría か y が.
    value = value.translate(str.maketrans("áéíóúü", "aeiouu"))
    return " ".join(value.split())


def accepted(card: Card, direction: str) -> Tuple[str, ...]:
    if direction == "romaji":
        return (card.romaji,)
    if direction == "es_jp":
        return (card.japanese,)
    if direction == "jp_es":
        return tuple(part.strip() for part in card.spanish.split(";"))
    raise ValueError(direction)


def correct(card: Card, direction: str, answer: str) -> bool:
    return normalize(answer) in {normalize(x) for x in accepted(card, direction)}


def eligible(kind: str = "todos", level: int = 3) -> List[Card]:
    return [c for c in ALL_CARDS if c.level <= level
            and (kind == "todos" or c.kind == kind)]


def directions(card: Card) -> Tuple[str, ...]:
    if card.kind == "hiragana":
        return ("romaji", "es_jp")
    return ("jp_es", "es_jp", "romaji")


def prompt(card: Card, direction: str) -> str:
    if direction == "romaji":
        return "Escribe en romaji: " + card.japanese
    if direction == "jp_es":
        return "Traduce al español: " + card.japanese
    if card.kind == "hiragana":
        return "Escribe en hiragana: " + card.romaji
    return "Escribe en japonés: " + card.spanish.split(";")[0]


def solution(card: Card, direction: str) -> str:
    if direction == "romaji":
        return card.romaji
    if direction == "jp_es":
        return card.spanish
    return card.japanese


class Progress:
    def __init__(self, path: Optional[Path] = None) -> None:
        base = os.environ.get("MANGA_NIHONGO_HOME")
        self.path = path or Path(base or Path.home() / ".manga-nihongo") / "progreso.json"
        self.cards: Dict[str, dict] = {}
        if self.path.exists():
            try:
                payload = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(payload, dict) and isinstance(payload.get("cards"), dict):
                    self.cards = payload["cards"]
            except (OSError, ValueError):
                backup = self.path.with_suffix(".json.danado")
                try:
                    self.path.replace(backup)
                except OSError:
                    pass

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"version": 1, "cards": self.cards},
                                  ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def record(self, card: Card, direction: str, success: bool) -> dict:
        key = card.id + ":" + direction
        state = self.cards.get(key, {"attempts": 0, "correct": 0, "streak": 0, "interval": 0})
        state["attempts"] += 1
        if success:
            state["correct"] += 1
            state["streak"] += 1
            state["interval"] = min(60, max(1, state["interval"] * 2))
        else:
            state["streak"] = 0
            state["interval"] = 1
        state["due"] = (date.today() + timedelta(days=state["interval"])).isoformat()
        self.cards[key] = state
        self.save()
        return state

    def due(self, cards: Iterable[Card]) -> List[Tuple[Card, str]]:
        today = date.today().isoformat()
        return [(card, direction) for card in cards for direction in directions(card)
                if card.id + ":" + direction in self.cards
                and self.cards[card.id + ":" + direction].get("due", "") <= today]

    def summary(self) -> dict:
        states = list(self.cards.values())
        return {
            "practicadas": len(states),
            "intentos": sum(s.get("attempts", 0) for s in states),
            "aciertos": sum(s.get("correct", 0) for s in states),
            "pendientes": sum(s.get("due", "") <= date.today().isoformat() for s in states),
        }


def make_session(cards: List[Card], count: int, progress: Progress,
                 review_only: bool = False, rng: Optional[random.Random] = None
                 ) -> List[Tuple[Card, str]]:
    rng = rng or random.Random()
    if review_only:
        pairs = progress.due(cards)
    else:
        pairs = [(card, direction) for card in cards for direction in directions(card)]
        due = set((c.id, d) for c, d in progress.due(cards))
        rng.shuffle(pairs)
        pairs.sort(key=lambda p: (p[0].id, p[1]) not in due)
    return pairs[:max(1, count)]

