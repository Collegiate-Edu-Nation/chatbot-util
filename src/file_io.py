import csv
import utils

def read(filename, employees_filename, cen_answers_filename):
    """Read questions from csv file, read employees and cen_answers from text files"""
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter="\n")
        store = {}
        cur_topic = ""
        num_cen = 0
        for i, line in enumerate(reader):
            if i != 0:
                if len(line) > 0:
                    split = line[0].split(",")
                    topic = split[0]
                    question = split[1]
                    if topic != "" and question != "":
                        cur_topic = topic
                        store[cur_topic] = []
                    if question != "":
                        store[cur_topic].append(question)
                        if cur_topic == "CEN":
                            num_cen += 1
    with open(employees_filename, "r") as employees_file:
        employees = {}
        lines = employees_file.readlines()
        for line in lines:
            if len(line) >= 3:
                employee, role = line[:-1].split(sep=":")
            else:
                employee, role = line.split(sep=":")
            employees[employee] = role
    with open(cen_answers_filename, "r") as cen_answers_file:
        cen_answers = {}
        lines = cen_answers_file.readlines()
        for i, line in enumerate(lines):
            if len(line) >= 3:
                part1, part2 = line[:-1].split(sep=":")
            else:
                part1, part2 = line.split(sep=":")
            cen_answers[f"cen_{i}"] = [part1, part2]
    return store, num_cen, employees, cen_answers

def write(filename, store, employees, cen_answers, num_cen):
    """Format questions and topics, write to csv file"""
    with open(filename, 'w') as csvfile:
        csvfile.write('"question","answer"\n')
        cen_index = 0
        for topic in store:
            for question in store[topic]:
                # Write cleaned entry to csv
                answer, cen_index = utils.create_answer(topic, question, employees, cen_answers, num_cen, cen_index)
                entry = utils.clean_entry(question, answer)
                csvfile.write(entry)