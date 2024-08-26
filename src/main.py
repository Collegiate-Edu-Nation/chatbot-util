#!/usr/bin/env python
 
import os
import chain
import file_io

readfile = "~/.chatbot-util/Chatbot FAQ - Enter Here.csv"
writefile = "~/.chatbot-util/Permutated.csv"

def main():
    """Create chain and read store from file, then append generated questions to store and write to new file"""
    print(f'\nReading topics and questions from "{readfile}"...')
    store, num_cen = file_io.read(os.path.expanduser(readfile))
    print('Generating and appending similar questions...')
    permutated_store = chain.generate(store)
    print(f'Writing to "{writefile}"...')
    file_io.write(os.path.expanduser(writefile), permutated_store, num_cen)
    print('Done.\n')

if __name__ == '__main__':
    main()