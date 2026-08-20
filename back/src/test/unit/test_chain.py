# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

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
        response = ""

        # mock
        when(chain.ollama_client).generate(prompt, options).thenReturn(  # pyright: ignore [reportUnknownMemberType]
            response
        )

        expected: list[str] = []
        result = chain.invoke(prompt, phrases)
        self.assertEqual(result, expected)
        unstub()
