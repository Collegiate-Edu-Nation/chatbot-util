#!/usr/bin/env python
 
import os
import chain
import file_io

# Expanded file paths
readfile = os.path.expanduser("~/.chatbot-util/Chatbot FAQ - Enter Here.csv")
employees_filename = os.path.expanduser("~/.chatbot-util/employees.txt")
cen_answers_filename = os.path.expanduser("~/.chatbot-util/cen_answers.txt")
robotics_answers_filename = os.path.expanduser("~/.chatbot-util/robotics_answers.txt")
instr_answers_filename = os.path.expanduser("~/.chatbot-util/instr_answers.txt")
writefile = os.path.expanduser("~/.chatbot-util/Permutated.csv")

def main():
    """Create chain and read info from files, then append generated questions to store and write to new file"""
    print(f'\nReading topics, questions, employees, and cen_answers...')
    store, num_cen, num_robotics, num_instr, employees, cen_answers, robotics_answers, instr_answers = file_io.read(readfile, employees_filename, cen_answers_filename, robotics_answers_filename, instr_answers_filename)
    print('Generating and appending similar questions...')
    permutated_store = chain.generate(store)
    print(f'Writing to "{writefile}"...')
    file_io.write(writefile, permutated_store, employees, cen_answers, num_cen, robotics_answers, num_robotics, instr_answers, num_instr)
    print('Done.\n')

if __name__ == '__main__':
    main()