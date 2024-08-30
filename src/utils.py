def create_person_answer(topic, employees):
    """Update person topics to be their contact info"""
    temp = topic.split(' ')
    answer = f"{topic}, CEN's {employees[topic]}, can help with that. Their contact is {temp[0][0].lower()}{temp[1].lower()}@edu-nation.org"
    return answer

def create_cen_answer_helper(question, cen_answer):
    """Format answer and increment cen_index"""
    if ("CEN" in question) and ("acronym" not in question) and ("abbreviation" not in question):
        answer = f"{cen_answer[0]}CEN{cen_answer[1]}"
    else:
        answer = f"{cen_answer[0]}Collegiate Edu-Nation{cen_answer[1]}"
    return answer

def create_cen_answer(question, cen_answers, num_cen, cen_index):
    """Update CEN topics to be the relevant answer"""
    if (cen_index in set(range(2))) or (cen_index in set(range(num_cen,num_cen+10))):
        answer = create_cen_answer_helper(question, cen_answers["cen_0"])
    elif ((cen_index in set(range(2,4))) and (num_cen >= 4)) or (cen_index in set(range(num_cen+10,num_cen+20))):
        answer = create_cen_answer_helper(question, cen_answers["cen_1"])
    elif ((cen_index in set(range(4,6))) and (num_cen >= 6)) or (cen_index in set(range(num_cen+20,num_cen+30))):
        answer = create_cen_answer_helper(question, cen_answers["cen_2"])
    elif ((cen_index in set(range(6,8))) and (num_cen >= 8)) or (cen_index in set(range(num_cen+30,num_cen+40))):
        answer = create_cen_answer_helper(question, cen_answers["cen_3"])
    elif ((cen_index in set(range(8,10))) and (num_cen >= 10)) or (cen_index in set(range(num_cen+40,num_cen+50))):
        answer = create_cen_answer_helper(question, cen_answers["cen_4"])
    cen_index += 1
    return answer, cen_index

def create_other_answer(answers, num, index):
    """Update other topics to be the relevant answer"""
    answer = None
    i = 0
    while not answer:
        if ((index == i) or (index in set(range(num+(i*5), num+((i+1)*5))))):
            answer = answers[i]
        i += 1
    return answer, index

def create_answer(topic, question, employees, answers, nums, indices):
    """Convert topics to answers depending on whether the topic is a person, CEN, or other"""
    if topic == 'CEN':
        answer, indices["cen_index"] = create_cen_answer(
            question, 
            answers["cen_answers"], 
            nums["num_cen"], 
            indices["cen_index"]
        )
    elif topic == 'Robotics':
        answer, indices["robotics_index"] = create_other_answer(
            answers["robotics_answers"], 
            nums["num_robotics"], 
            indices["robotics_index"]
        )
    elif topic == 'Instructional':
        answer, indices["instr_index"] = create_other_answer(
            answers["instr_answers"], 
            nums["num_instr"], 
            indices["instr_index"]
        )
    else:
        answer = create_person_answer(topic, employees)
    return answer, indices

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