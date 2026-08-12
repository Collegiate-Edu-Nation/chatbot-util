# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from mockito import (  # pyright: ignore [reportMissingTypeStubs]
    ANY,  # pyright: ignore [reportUnknownVariableType]
    mock,  # pyright: ignore [reportUnknownVariableType]
    unstub,  # pyright: ignore [reportUnknownVariableType]
    when,  # pyright: ignore [reportUnknownVariableType]
)
from ollama import Client

from chatbot_util import chain


class TestChainGenerate(unittest.TestCase):
    def test_generate(self):
        # setup
        client = mock(Client)
        phrases = [["abc", "ABC"]]
        options = {"seed": 39}
        prompt = chain.INSTRUCTION + "def"
        prompt2 = chain.INSTRUCTION + "ghi"
        response = {"response": '"a"'}
        response2 = {"response": '"b"'}
        store = {"abc": ["def", "ghi"]}

        # mocks
        when(chain).Client(host=ANY(str)).thenReturn(client)  # pyright: ignore [reportUnknownMemberType]
        when(client).generate(
            # pyright: ignore [reportUnknownMemberType]
            model="mistral",
            prompt=prompt,
            options=options,
        ).thenReturn(response)
        when(client).generate(
            # pyright: ignore [reportUnknownMemberType]
            model="mistral",
            prompt=prompt2,
            options=options,
        ).thenReturn(response2)

        expected = {"abc": ["def", "ghi", '"a"', '"b"']}
        result = chain.generate(store, phrases)
        self.assertEqual(result, expected)
        unstub()
