# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

import ollama
from mockito import (  # pyright: ignore [reportMissingTypeStubs]
    unstub,  # pyright: ignore [reportUnknownVariableType]
    when,  # pyright: ignore [reportUnknownVariableType]
)

from chatbot_util import chain


class TestChain(unittest.TestCase):
    def test_parse(self):
        # setup
        phrases = [["abc", "ABC"]]

        # empty
        response = ""
        expected: list[str] = []
        cleaned = chain.parse(response, phrases)
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
            # pyright: ignore [reportUnknownMemberType]
            model="mistral",
            prompt=prompt,
            options=options,
        ).thenReturn(response)

        expected: list[str] = []
        result = chain.invoke(prompt, phrases)
        self.assertEqual(result, expected)
        unstub()
