# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Entry point that launches a uvicorn server and connects the backend reading, generation, and writing functionalities"""

import os
import sys

import uvicorn

from chatbot_util import chain, file_io


def start() -> None:
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


def main() -> None:
    """Start uvicorn server"""
    host = "127.0.0.1"
    port = 8000

    print(f"Starting server on {host}:{port}...\n")
    uvicorn.run(
        "chatbot_util.api:app",
        host=host,
        port=port,
    )


if __name__ == "__main__":
    sys.exit(main())
