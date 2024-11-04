import unittest
from src import file_io


class TestFileIO(unittest.TestCase):
    def test_read_employees(self):
        lines = ["A Bcdef:G Hi\n", ":\n"]
        expected = {"A Bcdef": "G Hi", "": "\n"}

        employees = file_io.read_employees(lines)
        self.assertEqual(employees, expected)

    def test_read_phrases(self):
        lines = ["Common Table Expressions (CTE):CTE\n"]
        expected = [["Common Table Expressions (CTE)", "CTE"]]

        phrases = file_io.read_phrases(lines)
        self.assertEqual(phrases, expected)

    def test_read_cen(self):
        lines = ["Joining:will help\n", ":\n"]
        expected = {"cen_0": ["Joining", "will help"], "cen_1": ["", "\n"]}

        cen_answers = file_io.read_cen(lines)
        self.assertEqual(cen_answers, expected)

    def test_read_basic(self):
        lines = ["A Bcd can help with that\n"]
        expected = ["A Bcd can help with that"]

        basic_answers = file_io.read_basic(lines)
        self.assertEqual(basic_answers, expected)

    def test_read_answers(self):
        lines = [[], [], []]
        expected = {"cen_answers": {}, "robotics_answers": [], "instr_answers": []}

        answers = file_io.read_answers(lines)
        self.assertEqual(answers, expected)
