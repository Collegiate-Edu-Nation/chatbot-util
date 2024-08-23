import csv
import utils

def read(filename):
    """Read questions from csv file"""
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter="\n")
        store = {}
        cur_topic = ""
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
    return store

def write(filename, store):
    """Format questions and topics, write to csv file"""
    with open(filename, 'w') as csvfile:
        csvfile.write('"question","answer"\n')
        num_cen = 0
        for topic in store:
            for question in store[topic]:
                # Write cleaned entry to csv
                answer, num_cen = utils.create_answer(topic, question, num_cen)
                entry = utils.clean_entry(question, answer)
                csvfile.write(entry)