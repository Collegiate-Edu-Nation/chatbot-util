import csv
import utils

def read(filename):
    """Read questions from csv file"""
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
    return store, num_cen

def write(filename, store, num_cen):
    """Format questions and topics, write to csv file"""
    with open(filename, 'w') as csvfile:
        csvfile.write('"question","answer"\n')
        cen_index = 0
        for topic in store:
            for question in store[topic]:
                # Write cleaned entry to csv
                answer, cen_index = utils.create_answer(topic, question, num_cen, cen_index)
                entry = utils.clean_entry(question, answer)
                csvfile.write(entry)