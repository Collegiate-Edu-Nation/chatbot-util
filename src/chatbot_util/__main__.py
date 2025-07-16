# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Entry point that passes info read from files to chain, then passes LLM result to be written"""

import os
import subprocess
import sys

from fastapi import FastAPI

from chatbot_util import chain, file_io

app = FastAPI()


@app.get("/")
async def root():
    return {"status": 200}


@app.post("/generate")
async def generate() -> int:
    """Create chain, read info from files, append generated questions, then write to new file

    201 = successfully generated Permutated.csv\n
    500 = generic error
    """
    status_code: int
    try:
        main()
        status_code = 201
    except Exception:
        status_code = 500

    return status_code


@app.post("/verify")
async def verify():
    """Executes the verify script and returns one of the following:

    "verified"\n
    "unverified"\n
    "error"\n
    """
    exit_code = subprocess.run("verify").returncode

    status: str
    if exit_code == 0:
        status = "verified"
    elif exit_code == 3:
        status = "unverified"
    else:
        status = "error"

    return {"status": status}


def main() -> None:
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
