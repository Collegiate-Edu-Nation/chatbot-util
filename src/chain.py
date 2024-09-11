import sys
import ollama

instruction = "If a question uses an abbreviation, use that abbreviation in your generated questions - NEVER MAKE UP A MEANING FOR AN ABBREVIATION. Generate 5 variations of the following question: "

def parse(response, phrases):
    """Parse lines from LLM and clean them before returning"""
    def remove_empty(lines):
        """Remove empty lines"""
        for line in lines:
            if line == '':
                lines.remove(line)
        return lines

    def remove_numbers(lines):
        """Remove numbers"""
        for i, line in enumerate(lines):
            if line[1] == ".":
                lines[i] = line[3:]
        return lines

    def remove_phrases(lines, phrases):
        for i, line in enumerate(lines):
            for phrase in phrases:
                line = line.replace(phrase[0], phrase[1])
            lines[i] = line
        return lines

    lines = response.strip().split("\n")
    nonempty_lines = remove_empty(lines)
    no_num_lines = remove_numbers(nonempty_lines)
    cleaned_lines = remove_phrases(no_num_lines, phrases)
    return cleaned_lines

def invoke(prompt, phrases):
    """Define chat model, then create the chain"""
    options = {"seed": 39}
    response = ollama.generate(
        model='mistral',
        prompt=prompt,
        options=options
    )
    cleaned_response = parse(response["response"], phrases)
    return cleaned_response

def generate(store, phrases):
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

    for topic in store:
        new_questions = []
        for question in store[topic]:
            progress(index, total)
            prompt = instruction + question
            new_questions.append(invoke(prompt, phrases))
            index += 1
        for new_sub_question in new_questions:
            for new_question in new_sub_question:
                store[topic].append(new_question)
    return store