import unittest
from src import chain

class TestUtils(unittest.TestCase):
    def test_parse(self):
        # setup
        phrases = [['abc', 'ABC']]

        # empty
        response = ''
        expected = []
        cleaned = chain.parse(response, expected)
        self.assertEqual(cleaned, expected)

        # numbers
        response = '1. a'
        expected = ['a']
        cleaned = chain.parse(response, phrases)
        self.assertEqual(cleaned, expected)

        # phrases
        response = 'abc'
        expected = ['ABC']
        cleaned = chain.parse(response, phrases)
        self.assertEqual(cleaned, expected)

