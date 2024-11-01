import unittest
from mockito import when, unstub
import ollama
from src import chain


class TestChainGenerate(unittest.TestCase):
    def test_generate(self):
        # setup
        phrases = [["abc", "ABC"]]
        options = {"seed": 39}
        prompt = chain.INSTRUCTION + "def"
        response = {"response": '"a"'}
        store = {"abc": ["def"]}

        # mock
        when(ollama).generate(
            model="mistral",
            prompt=prompt,
            options=options,
        ).thenReturn(response)

        expected = {"abc": ["def", '"a"']}
        result = chain.generate(store, phrases)
        self.assertEqual(result, expected)
        unstub()
