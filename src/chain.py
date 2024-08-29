import sys
from langchain_community.chat_models import ChatOllama
from parser import LineListOutputParser

instruction = "Knowing that CEN stands for Collegiate Edu-Nation, generate 5 variations of the following question: "

def create():
    """Define chat model, then create the chain"""
    model = ChatOllama(
        model='mistral'
    )
    chain = model | LineListOutputParser()
    return chain

def generate(store):
    """Generate and append new questions to store"""
    def progress(index, total):
        """Updates generation progress"""
        sys.stdout.write(f"\rGenerating similar queries for: {index}/{total}...")
        sys.stdout.flush()

    # Calculate total number of questions to generate
    index, total = 1, 0
    for topic in store:
        for question in store[topic]:
            total += 1

    chain = create()
    for topic in store:
        new_questions = []
        for question in store[topic]:
            progress(index, total)
            prompt = instruction + question
            new_questions.append(chain.invoke(prompt))
            index += 1
        for new_sub_question in new_questions:
            for new_question in new_sub_question:
                store[topic].append(new_question)
    return store