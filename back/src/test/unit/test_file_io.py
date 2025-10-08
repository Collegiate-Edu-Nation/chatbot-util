# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import tempfile
import unittest

from chatbot_util import file_io, utils


class TestFileIO(unittest.TestCase):
    def test_read_employees(self):
        lines = ["A Bcdef:G Hi:His\n", "::\n"]
        expected = {"A Bcdef": ["G Hi", "His"], "": ["", ""]}

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
        lines: list[list[str]] = [[], [], [], []]
        expected: utils.Answers = {
            "cen_answers": {},
            "other_answers": [[], []],
        }

        answers = file_io.read_answers(lines)
        self.assertEqual(answers, expected)

    def test_read_entries(self):
        lines = [
            "Person/Entity,Questions\n",
            "CEN,What is CEN?\n",
            ",\n",
            "A Bcdef,We also need help\n",
            ",\n",
            "Instructional,We also also need help\n",
            ",\n",
            "Edu-Reach,We also also need help\n",
        ]
        teams = ["Instructional", "Edu-Reach"]
        with tempfile.NamedTemporaryFile() as temp_file:
            open(temp_file.name, "w", encoding="utf-8").writelines(lines)

            expected_store = {
                "CEN": ["What is CEN?"],
                "A Bcdef": ["We also need help"],
                "Instructional": ["We also also need help"],
                "Edu-Reach": ["We also also need help"],
            }
            expected_nums = {
                "num_cen": 1,
                "num_other": [1, 1],
            }

            store, nums = file_io.read_entries(temp_file.name, teams)
            self.assertEqual(store, expected_store)
            self.assertEqual(nums, expected_nums)
            temp_file.close()
