# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

import ollama
from mockito import (  # pyright: ignore [reportMissingTypeStubs]
    unstub,  # pyright: ignore [reportUnknownVariableType]
    when,  # pyright: ignore [reportUnknownVariableType]
)

from chatbot_util import chain


class TestChainGenerate(unittest.TestCase):
    def test_generate(self):
        # setup
        phrases = [["abc", "ABC"]]
        options = {"seed": 39}
        prompt = chain.INSTRUCTION + "def"
        prompt2 = chain.INSTRUCTION + "ghi"
        response = {"response": '"a"'}
        response2 = {"response": '"b"'}
        store = {"abc": ["def", "ghi"]}

        # mock
        when(ollama).generate(
            # pyright: ignore [reportUnknownMemberType]
            model="mistral",
            prompt=prompt,
            options=options,
        ).thenReturn(response)
        when(ollama).generate(
            # pyright: ignore [reportUnknownMemberType]
            model="mistral",
            prompt=prompt2,
            options=options,
        ).thenReturn(response2)

        expected = {"abc": ["def", "ghi", '"a"', '"b"']}
        result = chain.generate(store, phrases)
        self.assertEqual(result, expected)
        unstub()
