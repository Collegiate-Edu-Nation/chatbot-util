import csv
from employees import employees

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

def create_answer(topic):
    """Update non-CEN topics to be their contact info"""
    if topic != 'CEN':
        temp = topic.split(' ')
        answer = f"{topic}, CEN's {employees[topic]}, can help with that. Their contact is {temp[0][0].lower()}{temp[1].lower()}@edu-nation.org"
    else:
        answer = topic
    return answer

def clean_entry(question, answer):
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

def write(filename, store):
    """Format questions and topics, write to csv file"""
    with open(filename, 'w') as csvfile:
        csvfile.write('"question","answer"\n')
        for topic in store:
            for question in store[topic]:
                # Write cleaned entry to csv
                answer = create_answer(topic)
                entry = clean_entry(question, answer)
                csvfile.write(entry)