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

def create_person_answer(topic):
    """Update non-CEN topics to be their contact info"""
    temp = topic.split(' ')
    answer = f"{topic}, CEN's {employees[topic]}, can help with that. Their contact is {temp[0][0].lower()}{temp[1].lower()}@edu-nation.org"
    return answer

def create_cen_answer(question, num_cen):
    """Update CEN topics to be the relevant answer"""
    if (num_cen in (set(range(2)) | set(range(4,14)))):
        if "CEN" in question:
            answer = f"CEN {cen_1}"
        else:
            answer = f"Collegiate Edu-Nation {cen_1}"
        num_cen += 1
    elif (num_cen in (set(range(2,4)) | set(range(14,24)))):
        if "CEN" in question:
            answer = f"Joining CEN {cen_2}"
        else:
            answer = f"Joining Collegiate Edu-Nation {cen_2}"
        num_cen += 1
    else:
        answer = "CEN"
    return answer, num_cen

def create_answer(topic, question, num_cen):
    """Convert topics to answers depending on whether the topic is a person or CEN"""
    if topic != 'CEN':
        answer = create_person_answer(topic)
    else:
        answer, num_cen = create_cen_answer(question, num_cen)
    return answer, num_cen

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