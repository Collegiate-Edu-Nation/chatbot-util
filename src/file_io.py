import csv
from src import utils


def read(filenames):
    """Read questions from csv file, read employees and cen_answers from text files"""
    with open(filenames["readfile"], "r") as f:
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
    with open(filenames["employees_filename"], "r") as employees_file:
        employees = {}
        lines = employees_file.readlines()
        for line in lines:
            if len(line) >= 3:
                employee, role = line[:-1].split(sep=":")
            else:
                employee, role = line.split(sep=":")
            employees[employee] = role
    with open(filenames["phrases_filename"], "r") as phrases_file:
        phrases = []
        lines = phrases_file.readlines()
        for line in lines:
            find, replace = line.split(sep=":")
            replace = replace.strip("\n")
            phrases.append([find, replace])
    with open(filenames["cen_answers_filename"], "r") as cen_answers_file:
        cen_answers = {}
        lines = cen_answers_file.readlines()
        for i, line in enumerate(lines):
            if len(line) >= 3:
                part1, part2 = line[:-1].split(sep=":")
            else:
                part1, part2 = line.split(sep=":")
            cen_answers[f"cen_{i}"] = [part1, part2]
    with open(filenames["robotics_answers_filename"], "r") as robotics_answers_file:
        robotics_answers = []
        lines = robotics_answers_file.readlines()
        for line in lines:
            clean_line = line.strip("\n")
            robotics_answers.append(clean_line)
    with open(filenames["instr_answers_filename"], "r") as instr_answers_file:
        instr_answers = []
        lines = instr_answers_file.readlines()
        for line in lines:
            clean_line = line.strip("\n")
            instr_answers.append(clean_line)
    answers = {
        "cen_answers": cen_answers,
        "robotics_answers": robotics_answers,
        "instr_answers": instr_answers,
    }
    return store, employees, phrases, answers, nums


def write(filenames, store, employees, answers, nums):
    """Format questions and topics, write to csv file"""
    with open(filenames["writefile"], "w") as csvfile:
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
