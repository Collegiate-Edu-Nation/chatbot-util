# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from mockito import when, unstub
import ollama
from src import chain


class TestChain(unittest.TestCase):
    def test_parse(self):
        # setup
        phrases = [["abc", "ABC"]]

        # empty
        response = ""
        expected = []
        cleaned = chain.parse(response, expected)
        self.assertEqual(cleaned, expected)

        # numbers
        response = "1. a"
        expected = ["a"]
        cleaned = chain.parse(response, phrases)
        self.assertEqual(cleaned, expected)

        # phrases
        response = "abc"
        expected = ["ABC"]
        cleaned = chain.parse(response, phrases)
        self.assertEqual(cleaned, expected)

    def test_invoke(self):
        # setup
        phrases = [["abc", "ABC"]]
        options = {"seed": 39}
        prompt = ""
        response = {"response": ""}

        # mock
        when(ollama).generate(
            model="mistral",
            prompt=prompt,
            options=options,
        ).thenReturn(response)

        expected = []
        result = chain.invoke(prompt, phrases)
        self.assertEqual(result, expected)
        unstub()
