import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from manga_nihongo.cli import fit, menu, panel, visual_width, wrapped
from manga_nihongo.engine import Progress


class LayoutTests(unittest.TestCase):
    def test_japanese_width_and_truncation(self):
        self.assertEqual(visual_width("猫a"), 3)
        self.assertLessEqual(visual_width(fit("日本語を読む", 6)), 6)
        self.assertEqual(wrapped("hola mundo manga", 10), ["hola mundo", "manga"])

    def test_panel_fits_narrow_terminal(self):
        output = io.StringIO()
        with patch("manga_nihongo.cli.width", return_value=24), redirect_stdout(output):
            panel("LEE EN JAPONÉS", ["猫はどこ？", "Una frase bastante larga para el móvil"])
        lines = output.getvalue().splitlines()
        self.assertTrue(lines)
        self.assertTrue(all(visual_width(line) <= 24 for line in lines))

    def test_menu_can_exit_without_studying(self):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as folder:
            progress = Progress(Path(folder) / "progreso.json")
            with patch("builtins.input", return_value="0"), redirect_stdout(output):
                menu(progress)
        self.assertIn("Hiragana", output.getvalue())
        self.assertIn("HOY", output.getvalue())


if __name__ == "__main__":
    unittest.main()

