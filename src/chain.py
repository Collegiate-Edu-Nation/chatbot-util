from langchain_community.chat_models import ChatOllama
from parser import LineListOutputParser

instruction = "Knowing that CEN stands for Collegiate Edu-Nation, generate 5 variations of the following question: "

def create():
    """Define chat model, then create the chain"""
    model = ChatOllama(
        model='mistral',
        show_progress=False
    )
    chain = model | LineListOutputParser()
    return chain

def generate(store):
    """Generate and append new questions to store"""
    chain = create()
    for topic in store:
        new_questions = []
        for question in store[topic]:
            prompt = instruction + question
            new_questions.append(chain.invoke(prompt))
        for new_sub_question in new_questions:
            for new_question in new_sub_question:
                store[topic].append(new_question)
    return store