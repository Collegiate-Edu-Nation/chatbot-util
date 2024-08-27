def create_person_answer(topic, employees):
    """Update non-CEN topics to be their contact info"""
    temp = topic.split(' ')
    answer = f"{topic}, CEN's {employees[topic]}, can help with that. Their contact is {temp[0][0].lower()}{temp[1].lower()}@edu-nation.org"
    return answer

def create_cen_answer_helper(question, cen_answer, cen_index):
    """Format answer and increment cen_index"""
    if "CEN" in question:
        answer = f"{cen_answer[0]}CEN{cen_answer[1]}"
    else:
        answer = f"{cen_answer[0]}Collegiate Edu-Nation{cen_answer[1]}"
    cen_index += 1
    return answer, cen_index

def create_cen_answer(question, cen_answers, num_cen, cen_index):
    """Update CEN topics to be the relevant answer"""
    if (cen_index in set(range(2))) or (cen_index in set(range(num_cen,num_cen+10))):
        answer, cen_index = create_cen_answer_helper(question, cen_answers["cen_0"], cen_index)
    elif ((cen_index in set(range(2,4))) and (num_cen >= 4)) or (cen_index in set(range(num_cen+10,num_cen+20))):
        answer, cen_index = create_cen_answer_helper(question, cen_answers["cen_1"], cen_index)
    elif ((cen_index in set(range(4,6))) and (num_cen >= 6)) or (cen_index in set(range(num_cen+20,num_cen+30))):
        answer, cen_index = create_cen_answer_helper(question, cen_answers["cen_2"], cen_index)
    elif ((cen_index in set(range(6,8))) and (num_cen >= 8)) or (cen_index in set(range(num_cen+30,num_cen+40))):
        answer, cen_index = create_cen_answer_helper(question, cen_answers["cen_3"], cen_index)
    elif ((cen_index in set(range(8,10))) and (num_cen >= 10)) or (cen_index in set(range(num_cen+40,num_cen+50))):
        answer, cen_index = create_cen_answer_helper(question, cen_answers["cen_4"], cen_index)
    return answer, cen_index

def create_answer(topic, question, employees, cen_answers, num_cen, cen_index):
    """Convert topics to answers depending on whether the topic is a person or CEN"""
    if topic != 'CEN':
        answer = create_person_answer(topic, employees)
    else:
        answer, cen_index = create_cen_answer(question, cen_answers, num_cen, cen_index)
    return answer, cen_index

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