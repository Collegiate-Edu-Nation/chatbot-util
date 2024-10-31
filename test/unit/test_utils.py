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
        question = "CEN"
        cen_answer = ["abc", "def"]
        expected = "abcCENdef"
        answer = utils.create_cen_answer_helper(question, cen_answer)
        self.assertTrue(answer == expected)