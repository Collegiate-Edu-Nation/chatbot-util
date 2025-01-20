"""Entry point that passes info read from files to chain, then passes LLM result to be written"""

# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys

from chatbot_util import chain, file_io


def main():
    """Create chain, read info from files, append generated questions, then write to new file"""
    # Expanded file paths
    filenames = {
        "readfile": os.path.expanduser("~/.chatbot-util/Chatbot FAQ - Enter Here.csv"),
        "readfile2": os.path.expanduser("~/.chatbot-util/Other.txt"),
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
