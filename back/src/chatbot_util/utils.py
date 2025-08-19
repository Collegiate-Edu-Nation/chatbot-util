# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Utilities for creating and cleaning answers based on file content"""

from typing import TypedDict


class Answers(TypedDict):
    """Representation of the answer dict variants expected for each topic"""

    cen_answers: dict[str, list[str]]
    instr_answers: list[str]
    reach_answers: list[str]


def create_person_answer(topic: str, employees: dict[str, list[str]]) -> str:
    """Update person topics to be their contact info"""
    temp = topic.split(" ")
    answer = (
        f"{topic}, CEN's {employees[topic][0]}, can help with that. "
        f"{employees[topic][1]} contact is {temp[0][0].lower()}{temp[1].lower()}@edu-nation.org"
    )
    return answer


def create_cen_answer_helper(question: str, cen_answer: list[str]) -> str:
    """Format answer based on question content"""
    if (
        ("CEN" in question)
        and ("acronym" not in question)
        and ("abbreviation" not in question)
    ):
        answer = f"{cen_answer[0]}CEN{cen_answer[1]}"
    else:
        answer = f"{cen_answer[0]}Collegiate Edu-Nation{cen_answer[1]}"
    return answer


def create_cen_answer(
    question: str, cen_answers: dict[str, list[str]], num_cen: int, cen_index: int
) -> tuple[str, int]:
    """Update CEN topics to be the relevant answer"""
    answer = None
    i = 0
    while not answer:
        if (
            ((cen_index in set(range(i * 2, (i + 1) * 2))) and (num_cen >= (i + 1) * 2))
            or (cen_index == 0 and num_cen == 1)
            or (cen_index in set(range(num_cen + (i * 10), num_cen + ((i + 1) * 10))))
        ):
            answer = create_cen_answer_helper(question, cen_answers[f"cen_{i}"])
        i += 1
    cen_index += 1
    return answer, cen_index


def create_other_answer(answers: list[str], num: int, index: int) -> tuple[str, int]:
    """Update other topics to be the relevant answer"""
    answer = None
    i = 0
    while not answer:
        if (index == i) or (index in set(range(num + (i * 5), num + ((i + 1) * 5)))):
            answer = answers[i]
        i += 1
    index += 1
    return answer, index


def create_answer(
    topic: str,
    question: str,
    employees: dict[str, list[str]],
    answers: Answers,
    nums: dict[str, int],
    indices: dict[str, int],
) -> tuple[str, dict[str, int]]:
    """Convert topics to answers depending on whether the topic is a person, CEN, or other"""
    if topic == "CEN":
        answer, indices["cen_index"] = create_cen_answer(
            question,
            answers["cen_answers"],
            nums["num_cen"],
            indices["cen_index"],
        )
    elif topic == "Instructional":
        answer, indices["instr_index"] = create_other_answer(
            answers["instr_answers"],
            nums["num_instr"],
            indices["instr_index"],
        )
    elif topic == "Edu-Reach":
        answer, indices["reach_index"] = create_other_answer(
            answers["reach_answers"],
            nums["num_reach"],
            indices["reach_index"],
        )
    else:
        answer = create_person_answer(topic, employees)
    return answer, indices


def clean_entry(question: str, answer: str) -> str:
    """Clean up unnecessary quotes"""
    if question[0] == '"' and question[-1] == '"':
        entry = f'{question},"{answer}"\n'
    elif question[0] == '"':
        entry = f'{question}","{answer}"\n'
    elif question[-1] == '"':
        entry = f'"{question},"{answer}"\n'
    else:
        entry = f'"{question}","{answer}"\n'
    return entry
