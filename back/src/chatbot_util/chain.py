# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Setup language model and output parser, then generate and append new questions"""

import ollama

from chatbot_util import __main__


class Progress:
    """Representation of generation progress with utility methods for updating and displaying"""

    index: int = 0
    total: int

    def __init__(self, total: int) -> None:
        self.total = total

    def update(self, index: int) -> None:
        """Update generation progress"""
        self.index = index
        __main__.logger.info(
            f"Generating similar queries for: {self.index}/{self.total}."
        )


progress: Progress = Progress(0)
interrupt: bool = False
INSTRUCTION = """If a question uses an abbreviation, use that abbreviation \
in your generated questions - NEVER MAKE UP A MEANING FOR AN ABBREVIATION. \
Generate 5 variations of the following question: """


def parse(response: str, phrases: list[list[str]]) -> list[str]:
    """Parse lines from LLM and clean them before returning"""

    def remove_empty(lines: list[str]) -> list[str]:
        """Remove empty lines"""
        for line in lines:
            if line == "":
                lines.remove(line)
        return lines

    def remove_numbers(lines: list[str]) -> list[str]:
        """Remove numbers"""
        for i, line in enumerate(lines):
            if line[1] == ".":
                lines[i] = line[3:]
        return lines

    def remove_phrases(lines: list[str], phrases: list[list[str]]) -> list[str]:
        for i, line in enumerate(lines):
            for phrase in phrases:
                line = line.replace(phrase[0], phrase[1])
            lines[i] = line
        return lines

    lines = response.strip().split("\n")
    nonempty_lines = remove_empty(lines)
    no_num_lines = remove_numbers(nonempty_lines)
    cleaned_lines = remove_phrases(no_num_lines, phrases)
    return cleaned_lines


def invoke(prompt: str, phrases: list[list[str]]) -> list[str]:
    """Define chat model, then create the chain"""
    options = {"seed": 39}
    response = ollama.generate(
        model="mistral",
        prompt=prompt,
        options=options,
    )

    cleaned_response = parse(response["response"], phrases)
    return cleaned_response


def generate(
    store: dict[str, list[str]], phrases: list[list[str]]
) -> dict[str, list[str]]:
    """Generate and append new questions to store"""

    # Calculate total number of questions to generate
    index, total = 1, 0
    for topic in store:
        for question in store[topic]:
            total += 1

    # Init progress
    global progress
    progress = Progress(total)

    # Iterate over each topic (e.g., 'Reach', 'CEN', etc.)
    for topic in store:
        new_questions: list[list[str]] = []

        # Iterate over each question in the topic, generating 5 new ones / question
        for question in store[topic]:
            # return early if interrupted
            if interrupt:
                return store

            progress.update(index)
            prompt = INSTRUCTION + question
            new_questions.append(invoke(prompt, phrases))
            index += 1

        # Append synthetic questions for each organic question in this topic
        for new_sub_question in new_questions:
            for new_question in new_sub_question:
                store[topic].append(new_question)

    # Reset progress
    progress = Progress(0)
    return store
