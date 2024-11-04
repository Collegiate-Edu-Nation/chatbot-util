"""Reads csv, employees, and answers, and writes generated result to csv"""

import csv
from src import utils


def read_entries(filename):
    """read and return topics and basic answers"""
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\n")
        store = {}
        cur_topic = ""
        nums = {
            "num_cen": 0,
            "num_robotics": 0,
            "num_instr": 0,
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

    return store, nums


def read_employees(filename):
    """read and return employee list"""
    with open(filename, "r", encoding="utf-8") as employees_file:
        employees = {}
        lines = employees_file.readlines()
        for line in lines:
            if len(line) >= 3:
                employee, role = line[:-1].split(sep=":")
            else:
                employee, role = line.split(sep=":")
            employees[employee] = role

    return employees


def read_phrases(filename):
    """read and return phrases to find and replace"""
    with open(filename, "r", encoding="utf-8") as phrases_file:
        phrases = []
        lines = phrases_file.readlines()
        for line in lines:
            find, replace = line.split(sep=":")
            replace = replace.strip("\n")
            phrases.append([find, replace])

    return phrases


def read_cen(filename):
    """read and return cen_answers"""
    with open(filename, "r", encoding="utf-8") as cen_answers_file:
        cen_answers = {}
        lines = cen_answers_file.readlines()
        for i, line in enumerate(lines):
            if len(line) >= 3:
                part1, part2 = line[:-1].split(sep=":")
            else:
                part1, part2 = line.split(sep=":")
            cen_answers[f"cen_{i}"] = [part1, part2]

    return cen_answers


def read_robotics(filename):
    """read and return robotics answers"""
    with open(filename, "r", encoding="utf-8") as robotics_answers_file:
        robotics_answers = []
        lines = robotics_answers_file.readlines()
        for line in lines:
            clean_line = line.strip("\n")
            robotics_answers.append(clean_line)

    return robotics_answers


def read_instr(filename):
    """read and return instructional team answers"""
    with open(filename, "r", encoding="utf-8") as instr_answers_file:
        instr_answers = []
        lines = instr_answers_file.readlines()
        for line in lines:
            clean_line = line.strip("\n")
            instr_answers.append(clean_line)

    return instr_answers


def read_answers(filenames):
    """read and return answers for cen, robotics, instr"""
    cen_answers = read_cen(filenames["cen_answers_filename"])
    robotics_answers = read_robotics(filenames["robotics_answers_filename"])
    instr_answers = read_instr(filenames["instr_answers_filename"])

    answers = {
        "cen_answers": cen_answers,
        "robotics_answers": robotics_answers,
        "instr_answers": instr_answers,
    }
    return answers


def read(filenames):
    """Read questions from csv file, read employees, phrases and answers from text files"""
    store, nums = read_entries(filenames["readfile"])
    employees = read_employees(filenames["employees_filename"])
    phrases = read_phrases(filenames["phrases_filename"])
    answers = read_answers(filenames)

    return store, employees, phrases, answers, nums


def write(filenames, store, employees, answers, nums):
    """Format questions and topics, write to csv file"""
    with open(filenames["writefile"], "w", encoding="utf-8") as csvfile:
        csvfile.write('"question","answer"\n')
        indices = {
            "cen_index": 0,
            "robotics_index": 0,
            "instr_index": 0,
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
