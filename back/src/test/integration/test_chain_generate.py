# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

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
        response = '"a"'
        response2 = '"b"'
        store = {"abc": ["def", "ghi"]}

        # mocks
        when(chain.ollama_client).generate(prompt, options).thenReturn(  # pyright: ignore [reportUnknownMemberType]
            response
        )
        when(chain.ollama_client).generate(prompt2, options).thenReturn(  # pyright: ignore [reportUnknownMemberType]
            response2
        )

        expected = {"abc": ["def", "ghi", '"a"', '"b"']}
        result = chain.generate(store, phrases)
        self.assertEqual(result, expected)
        unstub()
