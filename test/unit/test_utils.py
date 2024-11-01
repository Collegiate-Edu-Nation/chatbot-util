import unittest
from src import utils

class TestUtils(unittest.TestCase):
    def test_create_person_answer(self):
        topic = "A Bcdef"
        employees = {"A Bcdef": "G Hijk"}
        expected = "A Bcdef, CEN's G Hijk, can help with that. Their contact is abcdef@edu-nation.org"
        answer = utils.create_person_answer(topic, employees)
        self.assertTrue(answer == expected)

    def test_create_cen_answer_helper(self):
        # CEN
        question = "CEN"
        cen_answer = ["abc", "def"]
        expected = "abcCENdef"
        answer = utils.create_cen_answer_helper(question, cen_answer)
        self.assertTrue(answer == expected)

        # CEN w/ acryonym
        question = "CEN acronym"
        cen_answer = ["abc", "def"]
        expected = "abcCollegiate Edu-Nationdef"
        answer = utils.create_cen_answer_helper(question, cen_answer)
        self.assertTrue(answer == expected)

        # Collegiate Edu-Nation
        question = "Collegiate Edu-Nation"
        cen_answer = ["abc", "def"]
        expected = "abcCollegiate Edu-Nationdef"
        answer = utils.create_cen_answer_helper(question, cen_answer)
        self.assertTrue(answer == expected)

    def test_create_cen_answer(self):
        question = "CEN"
        cen_answers = {"cen_0": ["abc", "def"]}
        expected = "abcCENdef"
        expected_i = 1
        answer, index = utils.create_cen_answer(question, cen_answers, 1, 0)
        self.assertTrue(answer == expected)
        self.assertTrue(index == expected_i)

    def test_create_other_answer(self):
        answers = ["abc"]
        num = 1
        index = 0
        expected = "abc"
        expected_i = 1
        answer, index = utils.create_other_answer(answers, num, index)
        self.assertTrue(answer == expected)
        self.assertTrue(index == expected_i)
