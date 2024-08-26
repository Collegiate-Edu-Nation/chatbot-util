# Employee list for position lookup
employees = {
    "Cam Boren": "Robotics and Programming Coordinator",
    "Dan Boren": "STEM Consultant",
    "Brittany Williams": "Chief Partnerships Officer",
    "Kelly Springfield": "Director of P-TECH",
    "Katie Daugherty": "AmeriCorps Program Coordinator",
    "Katy Cade": "School Action Director",
    "Andy Wilson": "Program Director",
    "Chantel Schulz": "CTE Instructional Specialist",
    "Tracy Rickerson": "Math Instructional Coach",
    "Kimberley Mouser": "Instructional Coach",
    "Michelle Smith": "Chief of Schools"
}

# Pre-baked responses for questions about CEN
cen_1 = "is a non-profit organization engaging whole communities to reinvigorate education, revitalize local economies, and reimagine what's possible for rural America. We're preparing rural communities to connect and thrive in a fast-moving future."
cen_2 = "will help reinvigorate your school, revitalize your local economy, and reimagine what's possible in your rural community."
cen_3 = ""
cen_4 = ""
cen_5 = ""

def create_person_answer(topic):
    """Update non-CEN topics to be their contact info"""
    temp = topic.split(' ')
    answer = f"{topic}, CEN's {employees[topic]}, can help with that. Their contact is {temp[0][0].lower()}{temp[1].lower()}@edu-nation.org"
    return answer

def create_cen_answer(question, num_cen, cen_index):
    """Update CEN topics to be the relevant answer"""
    # Original questions for first 5 statements, generated for last 5
    if (cen_index in set(range(2))):
        if "CEN" in question:
            answer = f"CEN {cen_1}"
        else:
            answer = f"Collegiate Edu-Nation {cen_1}"
        cen_index += 1
    elif (cen_index in set(range(2,4))) and (num_cen >= 4):
        if "CEN" in question:
            answer = f"Joining CEN {cen_2}"
        else:
            answer = f"Joining Collegiate Edu-Nation {cen_2}"
        cen_index += 1
    elif (cen_index in set(range(4,6))) and (num_cen >= 6):
        if "CEN" in question:
            answer = f"CEN {cen_3}"
        else:
            answer = f"Collegiate Edu-Nation {cen_3}"
        cen_index += 1
    elif (cen_index in set(range(6,8))) and (num_cen >= 8):
        if "CEN" in question:
            answer = f"CEN {cen_4}"
        else:
            answer = f"Collegiate Edu-Nation {cen_4}"
        cen_index += 1
    elif (cen_index in set(range(8,10))) and (num_cen >= 10):
        if "CEN" in question:
            answer = f"CEN {cen_5}"
        else:
            answer = f"Collegiate Edu-Nation {cen_5}"
        cen_index += 1
    elif (cen_index in set(range(num_cen,num_cen+10))):
        if "CEN" in question:
            answer = f"CEN {cen_1}"
        else:
            answer = f"Collegiate Edu-Nation {cen_1}"
        cen_index += 1
    elif (cen_index in set(range(num_cen+10,num_cen+20))):
        if "CEN" in question:
            answer = f"Joining CEN {cen_2}"
        else:
            answer = f"Joining Collegiate Edu-Nation {cen_2}"
        cen_index += 1
    elif (cen_index in set(range(num_cen+20,num_cen+30))):
        if "CEN" in question:
            answer = f"CEN {cen_3}"
        else:
            answer = f"Collegiate Edu-Nation {cen_3}"
        cen_index += 1
    elif (cen_index in set(range(num_cen+30,num_cen+40))):
        if "CEN" in question:
            answer = f"CEN {cen_4}"
        else:
            answer = f"Collegiate Edu-Nation {cen_4}"
        cen_index += 1
    elif (cen_index in set(range(num_cen+40,num_cen+50))):
        if "CEN" in question:
            answer = f"CEN {cen_5}"
        else:
            answer = f"Collegiate Edu-Nation {cen_5}"
        cen_index += 1

    return answer, cen_index

def create_answer(topic, question, num_cen, cen_index):
    """Convert topics to answers depending on whether the topic is a person or CEN"""
    if topic != 'CEN':
        answer = create_person_answer(topic)
    else:
        answer, cen_index = create_cen_answer(question, num_cen, cen_index)
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