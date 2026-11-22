import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from manga_nihongo.data import ALL_CARDS, KANA, KANJI, VOCAB
from manga_nihongo.engine import Progress, correct, directions, eligible, make_session


class ContentTests(unittest.TestCase):
    def test_content_is_unique_and_complete(self):
        self.assertEqual(len(KANA), 71)
        self.assertGreaterEqual(len(KANJI), 70)
        self.assertGreaterEqual(len(VOCAB), 60)
        self.assertEqual(len({card.id for card in ALL_CARDS}), len(ALL_CARDS))
        self.assertTrue(all(card.romaji and card.japanese for card in ALL_CARDS))

    def test_both_translation_directions_and_romaji(self):
        card = next(c for c in VOCAB if c.japanese == "猫")
        self.assertEqual(directions(card), ("jp_es", "es_jp", "romaji"))
        self.assertTrue(correct(card, "jp_es", " GÁTO "))
        self.assertTrue(correct(card, "es_jp", "猫"))
        self.assertTrue(correct(card, "romaji", "NEKO"))
        self.assertFalse(correct(card, "romaji", "inu"))
        self.assertTrue(correct(KANA[0], "es_jp", "あ"))
        voiced = next(c for c in KANA if c.japanese == "が")
        self.assertFalse(correct(voiced, "es_jp", "か"))

    def test_level_filter(self):
        self.assertTrue(all(c.level == 1 for c in eligible(level=1)))
        self.assertTrue(all(c.kind == "kanji" for c in eligible("kanji")))


class ProgressTests(unittest.TestCase):
    def test_persistence_and_due_interval(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "progreso.json"
            progress = Progress(path)
            card = KANA[0]
            first = progress.record(card, "romaji", True)
            self.assertEqual(first["interval"], 1)
            second = progress.record(card, "romaji", True)
            self.assertEqual(second["interval"], 2)
            self.assertEqual(second["due"], (date.today() + timedelta(days=2)).isoformat())
            self.assertEqual(Progress(path).summary()["aciertos"], 2)
            self.assertEqual(progress.due([card]), [])
            failed = progress.record(card, "romaji", False)
            self.assertEqual(failed["streak"], 0)
            self.assertEqual(failed["interval"], 1)

    def test_review_selects_only_due_directions(self):
        with tempfile.TemporaryDirectory() as folder:
            progress = Progress(Path(folder) / "progreso.json")
            card = KANA[0]
            self.assertEqual(make_session([card], 10, progress, True), [])
            progress.record(card, "romaji", False)
            progress.cards[card.id + ":romaji"]["due"] = date.today().isoformat()
            self.assertEqual(make_session([card], 10, progress, True), [(card, "romaji")])


if __name__ == "__main__":
    unittest.main()

