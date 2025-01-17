# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
import tempfile
from chatbot_util import file_io


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
        lines = [[], [], [], []]
        expected = {
            "cen_answers": {},
            "robotics_answers": [],
            "instr_answers": [],
            "reach_answers": [],
        }

        answers = file_io.read_answers(lines)
        self.assertEqual(answers, expected)

    def test_read_entries(self):
        lines = [
            "Person/Entity,Questions\n",
            "CEN,What is CEN?\n",
            ",\n",
            "Robotics,We need help\n",
            ",\n",
            "A Bcdef,We also need help\n",
            ",\n",
            "Instructional,We also also need help\n",
            ",\n",
            "Edu-Reach,We also also need help\n",
        ]
        with tempfile.NamedTemporaryFile() as temp_file:
            open(temp_file.name, "w", encoding="utf-8").writelines(lines)

            expected_store = {
                "CEN": ["What is CEN?"],
                "Robotics": ["We need help"],
                "A Bcdef": ["We also need help"],
                "Instructional": ["We also also need help"],
                "Edu-Reach": ["We also also need help"],
            }
            expected_nums = {
                "num_cen": 1,
                "num_robotics": 1,
                "num_instr": 1,
                "num_reach": 1,
            }

            store, nums = file_io.read_entries(temp_file.name)
            self.assertEqual(store, expected_store)
            self.assertEqual(nums, expected_nums)
            temp_file.close()
