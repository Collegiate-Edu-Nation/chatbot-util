# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from chatbot_util import utils


class TestUtils(unittest.TestCase):
    def test_create_person_answer(self):
        topic = "A Bcdef"
        employees = {"A Bcdef": "G Hijk"}
        expected = "A Bcdef, CEN's G Hijk, can help with that. Their contact is abcdef@edu-nation.org"
        answer = utils.create_person_answer(topic, employees)
        self.assertEqual(answer, expected)

    def test_create_cen_answer_helper(self):
        # CEN
        question = "CEN"
        cen_answer = ["abc", "def"]
        expected = "abcCENdef"
        answer = utils.create_cen_answer_helper(question, cen_answer)
        self.assertEqual(answer, expected)

        # CEN w/ acryonym
        question = "CEN acronym"
        cen_answer = ["abc", "def"]
        expected = "abcCollegiate Edu-Nationdef"
        answer = utils.create_cen_answer_helper(question, cen_answer)
        self.assertEqual(answer, expected)

        # Collegiate Edu-Nation
        question = "Collegiate Edu-Nation"
        cen_answer = ["abc", "def"]
        expected = "abcCollegiate Edu-Nationdef"
        answer = utils.create_cen_answer_helper(question, cen_answer)
        self.assertEqual(answer, expected)

    def test_create_cen_answer(self):
        question = "CEN"
        cen_answers = {"cen_0": ["abc", "def"]}
        expected = "abcCENdef"
        expected_i = 1
        answer, index = utils.create_cen_answer(question, cen_answers, 1, 0)
        self.assertEqual(answer, expected)
        self.assertEqual(index, expected_i)

    def test_create_other_answer(self):
        answers = ["abc"]
        num = 1
        index = 0
        expected = "abc"
        expected_i = 1
        answer, index = utils.create_other_answer(answers, num, index)
        self.assertEqual(answer, expected)
        self.assertEqual(index, expected_i)

    def test_create_answer(self):
        # setup
        employees = {"A Bcdef": "G Hijk"}
        answers = {
            "cen_answers": {"cen_0": ["abc", "def"]},
            "robotics_answers": ["abc"],
            "instr_answers": ["abc"],
        }
        nums = {
            "num_cen": 1,
            "num_robotics": 1,
            "num_instr": 1,
        }
        indices = {
            "cen_index": 0,
            "robotics_index": 0,
            "instr_index": 0,
        }

        # CEN
        topic = "CEN"
        question = "CEN"
        expected = "abcCENdef"
        expected_indices = indices
        expected_indices["cen_index"] += 1
        answer, rec_indices = utils.create_answer(
            topic, question, employees, answers, nums, indices
        )
        self.assertEqual(answer, expected)
        self.assertEqual(rec_indices, expected_indices)

        # Robotics
        topic = "Robotics"
        question = "abc"
        expected = "abc"
        expected_indices = indices
        expected_indices["robotics_index"] += 1
        answer, rec_indices = utils.create_answer(
            topic, question, employees, answers, nums, indices
        )
        self.assertEqual(answer, expected)
        self.assertEqual(rec_indices, expected_indices)

        # Instructional
        topic = "Instructional"
        expected_indices = indices
        expected_indices["instr_index"] += 1
        answer, rec_indices = utils.create_answer(
            topic, question, employees, answers, nums, indices
        )
        self.assertEqual(answer, expected)
        self.assertEqual(rec_indices, expected_indices)

        # Other
        topic = "A Bcdef"
        expected = "A Bcdef, CEN's G Hijk, can help with that. Their contact is abcdef@edu-nation.org"
        expected_indices = indices
        answer, rec_indices = utils.create_answer(
            topic, question, employees, answers, nums, indices
        )
        self.assertEqual(answer, expected)
        self.assertEqual(rec_indices, expected_indices)

    def test_clean_entry(self):
        answer = "abc"
        expected = '" ","abc"\n'

        # case 1
        question = '" "'
        entry = utils.clean_entry(question, answer)
        self.assertEqual(entry, expected)

        # case 2
        question = '" '
        entry = utils.clean_entry(question, answer)
        self.assertEqual(entry, expected)

        # case 3
        question = ' "'
        entry = utils.clean_entry(question, answer)
        self.assertEqual(entry, expected)

        # case 4
        question = " "
        entry = utils.clean_entry(question, answer)
        self.assertEqual(entry, expected)
