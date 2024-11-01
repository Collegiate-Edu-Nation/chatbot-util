"""Entry point that passes info read from files to chain, then passes LLM result to be written"""

import os
import sys
from src import chain, file_io


def main():
    """Create chain, read info from files, append generated questions, then write to new file"""
    # Expanded file paths
    filenames = {
        "readfile": os.path.expanduser("~/.chatbot-util/Chatbot FAQ - Enter Here.csv"),
        "employees_filename": os.path.expanduser("~/.chatbot-util/employees.txt"),
        "phrases_filename": os.path.expanduser("~/.chatbot-util/phrases.txt"),
        "cen_answers_filename": os.path.expanduser("~/.chatbot-util/cen_answers.txt"),
        "robotics_answers_filename": os.path.expanduser(
            "~/.chatbot-util/robotics_answers.txt"
        ),
        "instr_answers_filename": os.path.expanduser(
            "~/.chatbot-util/instr_answers.txt"
        ),
        "writefile": os.path.expanduser("~/.chatbot-util/Permutated.csv"),
    }

    # Read info, generate questions, then write final output
    print("\nReading topics, questions, employees, and answers...")
    store, employees, phrases, answers, nums = file_io.read(filenames)
    permutated_store = chain.generate(store, phrases)
    print(f'\nWriting to "{filenames["writefile"]}"...')
    file_io.write(filenames, permutated_store, employees, answers, nums)
    print("Done.\n")


if __name__ == "__main__":
    sys.exit(main())
