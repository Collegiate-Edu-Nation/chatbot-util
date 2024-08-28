#!/usr/bin/env python
 
import os
import chain
import file_io

# Expanded file paths
filenames = {
    "readfile": os.path.expanduser("~/.chatbot-util/Chatbot FAQ - Enter Here.csv"),
    "employees_filename": os.path.expanduser("~/.chatbot-util/employees.txt"),
    "cen_answers_filename": os.path.expanduser("~/.chatbot-util/cen_answers.txt"),
    "robotics_answers_filename": os.path.expanduser("~/.chatbot-util/robotics_answers.txt"),
    "instr_answers_filename": os.path.expanduser("~/.chatbot-util/instr_answers.txt"),
    "writefile": os.path.expanduser("~/.chatbot-util/Permutated.csv")
}

def main():
    """Create chain and read info from files, then append generated questions to store and write to new file"""
    print(f'\nReading topics, questions, employees, and answers...')
    store, employees, answers, nums = file_io.read(filenames)
    print('Generating and appending similar questions...')
    permutated_store = chain.generate(store)
    print(f'Writing to "{filenames["writefile"]}"...')
    file_io.write(filenames, permutated_store, employees, answers, nums)
    print('Done.\n')

if __name__ == '__main__':
    main()