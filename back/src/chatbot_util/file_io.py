# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Reads toml config, csv, employees, and answers, and writes generated result to csv"""

import csv
import os
import platform
import tomllib
from typing import TypedDict

import fastapi

from chatbot_util import utils

DEV = True if os.getenv("DEV", "false") == "true" else False
LINUX_DATA_HOME = "/var/lib/chatbot-util"
DARWIN_DATA_HOME = "/Library/Application Support/chatbot-util"
DIR = (
    (os.path.expanduser("~/.chatbot-util") if DEV else LINUX_DATA_HOME)
    if platform.system() == "Linux"
    else (os.path.expanduser(f"~{DARWIN_DATA_HOME}") if DEV else DARWIN_DATA_HOME)
)
CFG_DIR = os.path.expanduser("~/.config/chatbot-util") if DEV else "/etc/chatbot-util"
FAQ = "FAQ - Enter Here.csv"
OTHER = "Other.txt"
PERMUTATED = "Permutated.csv"
CONFIG = "config.toml"
FILENAMES = {
    "faq": f"{DIR}/{FAQ}",
    "other": f"{DIR}/{OTHER}",
    "permutated": f"{DIR}/{PERMUTATED}",
    "config": f"{CFG_DIR}/{CONFIG}",
}


class Config(TypedDict):
    """Resolved application configuration model"""

    host: str
    port: int
    url: str
    faq: str
    other: str


def read_config() -> Config:
    """Read and resolve application configuration"""
    cfg: Config = {
        "host": "127.0.0.1",
        "port": 8080,
        "url": "http://127.0.0.1:11434",
        "faq": "",
        "other": "",
    }

    try:
        with open(FILENAMES["config"], "rb") as f:
            config = tomllib.load(f)

        # parse the toml one section at a time so
        # that we don't throw everything away if a
        # specific section is missing (e.g., what if
        # your ollama server needs to be specified
        # but you're using the modules to specify the
        # port/host)
        #
        # main area of improvement here is to parse
        # each specific entry, but this works for now
        values: dict[str, object] = {}
        for section in ("server", "ollama", "links"):
            try:
                section_values: dict[str, object] = config[section]
                values.update(section_values)
            except Exception:
                pass

        # convert the toml's values to type-safe config entries
        for key in ("host", "url", "faq", "other"):
            value = values.get(key)
            if isinstance(value, str):
                cfg[key] = value

        configured_port = values.get("port")
        if isinstance(configured_port, int):
            cfg["port"] = configured_port

    except Exception:
        utils.logger.warning("Failed to load config.toml")

    # Environment variables override config.toml when present.
    host = os.getenv("HOST")
    ollama_url = os.getenv("OLLAMA_URL")
    faq_url = os.getenv("FAQ_URL")
    other_url = os.getenv("OTHER_URL")
    port = os.getenv("PORT")

    if host is not None:
        cfg["host"] = host
    if ollama_url is not None:
        cfg["url"] = ollama_url
    if faq_url is not None:
        cfg["faq"] = faq_url
    if other_url is not None:
        cfg["other"] = other_url
    if port is not None:
        cfg["port"] = int(port)

    return cfg


def create_file(f: fastapi.UploadFile) -> bool | None:
    """Create or replace a data file"""
    # determine whether anything should be done with the uploaded file
    created: bool | None = True
    filename: str | None = None
    if str(f.filename) == FAQ:
        filename = FILENAMES["faq"]
    elif str(f.filename) == OTHER:
        filename = FILENAMES["other"]
    elif str(f.filename) == CONFIG:
        filename = FILENAMES["config"]

    # try to replace the relevant file bytewise
    if filename is not None:
        try:
            contents = f.file.read()

            # create the data dir if it doesn't exist
            if not os.path.exists(DIR):
                os.makedirs(DIR)

            # move the old file if it exists
            if os.path.exists(filename):
                os.rename(
                    filename,
                    filename + ".backup",
                )

            with open(filename, "wb") as openfile:
                openfile.write(contents)

        except Exception:
            created = False
    else:
        created = None

    return created


def read_teams(lines: list[str]) -> list[str]:
    """Read and return teams"""
    return [line.strip() for line in lines]


def read_entries(
    filename: str, teams: list[str]
) -> tuple[dict[str, list[str]], utils.Nums]:
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
        nums: utils.Nums = {
            "num_cen": 0,
            "num_other": [0] * len(teams),
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
                        elif cur_topic in teams:
                            nums["num_other"][teams.index(cur_topic)] += 1

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
    """Read and return `cen_answers`"""
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
    """Read and return answers for cen and teams"""
    cen_answers = read_cen(lines[0])
    other_answers = [read_basic(lines[1]), read_basic(lines[2])]

    answers: utils.Answers = {
        "cen_answers": cen_answers,
        "other_answers": other_answers,
    }
    return answers


def read_other(
    filename: str,
) -> tuple[list[str], dict[str, list[str]], list[list[str]], utils.Answers]:
    """Read and return employees, phrases, and answers"""
    with open(filename, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()
        lines: list[list[str]] = [[], [], [], [], [], [], []]

        cur = 0
        for raw_line in raw_lines:
            if raw_line == "\n":
                cur += 1
                continue
            lines[cur].append(raw_line)

    teams = read_teams(lines[0])
    employees = read_employees(lines[1])
    phrases = read_phrases(lines[2])
    answers = read_answers(lines[3:])
    return teams, employees, phrases, answers


def read() -> tuple[
    dict[str, list[str]],
    list[str],
    dict[str, list[str]],
    list[list[str]],
    utils.Answers,
    utils.Nums,
]:
    """Read questions from csv file, read teams, employees, phrases and answers from text files"""
    teams, employees, phrases, answers = read_other(FILENAMES["other"])
    store, nums = read_entries(FILENAMES["faq"], teams)

    return store, teams, employees, phrases, answers, nums


def write(
    store: dict[str, list[str]],
    teams: list[str],
    employees: dict[str, list[str]],
    answers: utils.Answers,
    nums: utils.Nums,
) -> None:
    """Format questions and topics, write to csv file"""
    if os.path.exists(FILENAMES["permutated"]):
        os.rename(FILENAMES["permutated"], FILENAMES["permutated"] + ".backup")

    with open(FILENAMES["permutated"], "w", encoding="utf-8") as csvfile:
        csvfile.write('"question","answer"\n')
        indices: utils.Indices = {
            "cen_index": 0,
            "other_index": [0] * len(teams),
        }
        for topic in store:
            for question in store[topic]:
                # Write cleaned entry to csv
                answer, indices = utils.create_answer(
                    topic,
                    question,
                    teams,
                    employees,
                    answers,
                    nums,
                    indices,
                )
                entry = utils.clean_entry(question, answer)
                csvfile.write(entry)
