# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Reads csv, employees, and answers, and writes generated result to csv"""

import csv
import os

from chatbot_util import utils


def read_entries(filename: str) -> tuple[dict[str, list[str]], dict[str, int]]:
    """Read and return topics and basic answers"""

    with open(filename, "r", encoding="utf-8") as f:
        # it seems as though the delimiter doesn't actually
        # matter as long as it's not the default: ",". updating
        # to 3.13 broke "\n", and alternative approaches (e.g.,
        # topic = line[0] w/ delimiter = ",") broke Ollama's
        # determinism
        reader = csv.reader(f, delimiter="\t")
        store: dict[str, list[str]] = {}
        cur_topic = ""
        nums = {
            "num_cen": 0,
            "num_robotics": 0,
            "num_instr": 0,
            "num_reach": 0,
        }

        for i, line in enumerate(reader):
            if i != 0:
                if len(line) > 0:
                    topic = line[0].split(",")[0]
                    question = line[0].removeprefix(topic + ",")
                    if topic != "" and question != "":
                        cur_topic = topic
                        store[cur_topic] = []
                    if question != "":
                        store[cur_topic].append(question)
                        if cur_topic == "CEN":
                            nums["num_cen"] += 1
                        elif cur_topic == "Robotics":
                            nums["num_robotics"] += 1
                        elif cur_topic == "Instructional":
                            nums["num_instr"] += 1
                        elif cur_topic == "Edu-Reach":
                            nums["num_reach"] += 1

    return store, nums


def read_employees(lines: list[str]) -> dict[str, list[str]]:
    """Read and return employee list"""
    employees: dict[str, list[str]] = {}
    for line in lines:
        if len(line) >= 3:
            employee, role, pronoun = line[:-1].split(sep=":")
        else:
            employee, role, pronoun = line.split(sep=":")
        employees[employee] = [role, pronoun]

    return employees


def read_phrases(lines: list[str]) -> list[list[str]]:
    """Read and return phrases to find and replace"""
    phrases: list[list[str]] = []
    for line in lines:
        find, replace = line.split(sep=":")
        replace = replace.strip("\n")
        phrases.append([find, replace])

    return phrases


def read_cen(lines: list[str]) -> dict[str, list[str]]:
    """Read and return cen_answers"""
    cen_answers: dict[str, list[str]] = {}
    for i, line in enumerate(lines):
        if len(line) >= 3:
            part1, part2 = line[:-1].split(sep=":")
        else:
            part1, part2 = line.split(sep=":")
        cen_answers[f"cen_{i}"] = [part1, part2]

    return cen_answers


def read_basic(lines: list[str]) -> list[str]:
    """Read and return basic answers for topics other than CEN"""
    basic_answers: list[str] = []
    for line in lines:
        clean_line = line.strip("\n")
        basic_answers.append(clean_line)

    return basic_answers


def read_answers(lines: list[list[str]]) -> utils.Answers:
    """Read and return answers for cen, robotics, instr"""
    cen_answers = read_cen(lines[0])
    robotics_answers = read_basic(lines[1])
    instr_answers = read_basic(lines[2])
    reach_answers = read_basic(lines[3])

    answers: utils.Answers = {
        "cen_answers": cen_answers,
        "robotics_answers": robotics_answers,
        "instr_answers": instr_answers,
        "reach_answers": reach_answers,
    }
    return answers


def read_other(
    filename: str,
) -> tuple[dict[str, list[str]], list[list[str]], utils.Answers]:
    """Read and return employees, phrases, and answers"""
    with open(filename, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()
        lines: list[list[str]] = [[], [], [], [], [], []]

        cur = 0
        for raw_line in raw_lines:
            if raw_line == "\n":
                cur += 1
                continue
            lines[cur].append(raw_line)

    employees = read_employees(lines[0])
    phrases = read_phrases(lines[1])
    answers = read_answers(lines[2:])
    return employees, phrases, answers


def read(
    filenames: dict[str, str],
) -> tuple[
    dict[str, list[str]],
    dict[str, list[str]],
    list[list[str]],
    utils.Answers,
    dict[str, int],
]:
    """Read questions from csv file, read employees, phrases and answers from text files"""
    store, nums = read_entries(filenames["readfile"])
    employees, phrases, answers = read_other(filenames["readfile2"])

    return store, employees, phrases, answers, nums


def write(
    filenames: dict[str, str],
    store: dict[str, list[str]],
    employees: dict[str, list[str]],
    answers: utils.Answers,
    nums: dict[str, int],
) -> None:
    """Format questions and topics, write to csv file"""
    os.rename(filenames["writefile"], filenames["writefile"] + ".backup")
    with open(filenames["writefile"], "w", encoding="utf-8") as csvfile:
        csvfile.write('"question","answer"\n')
        indices = {
            "cen_index": 0,
            "robotics_index": 0,
            "instr_index": 0,
            "reach_index": 0,
        }
        for topic in store:
            for question in store[topic]:
                # Write cleaned entry to csv
                answer, indices = utils.create_answer(
                    topic,
                    question,
                    employees,
                    answers,
                    nums,
                    indices,
                )
                entry = utils.clean_entry(question, answer)
                csvfile.write(entry)
