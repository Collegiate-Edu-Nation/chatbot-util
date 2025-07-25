# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Entry point that launches a uvicorn server and connects the backend reading, generation, and writing functionalities"""

import os
import subprocess
import sys

import uvicorn

from chatbot_util import chain, file_io


def main() -> None:
    """Start uvicorn server"""
    host = "127.0.0.1"
    port = 8080

    print(f"Starting server on {host}:{port}...\n")
    uvicorn.run(
        "chatbot_util.api:app",
        host=host,
        port=port,
    )


def start() -> None:
    """Create chain, read info from files, append generated questions, then write to new file"""

    def handle_interrupt() -> bool:
        """Helper to reset chain state if interrupted"""
        interrupted = False
        if chain.interrupt:
            chain.interrupt = False
            chain.progress = chain.Progress(0)
            print("\nInterrupted.\n")
            interrupted = True

        return interrupted

    filenames = {
        "readfile": os.path.expanduser("~/.chatbot-util/Chatbot FAQ - Enter Here.csv"),
        "readfile2": os.path.expanduser("~/.chatbot-util/Other.txt"),
        "writefile": os.path.expanduser("~/.chatbot-util/Permutated.csv"),
    }

    # Check interrupt status between operations to avoid undesired behavior
    if handle_interrupt():
        return

    # Read topics and organic questions
    print("\nReading topics, questions, employees, and answers...")
    store, employees, phrases, answers, nums = file_io.read(filenames)

    if handle_interrupt():
        return

    # Generate synthetic questions
    permutated_store = chain.generate(store, phrases)

    if handle_interrupt():
        return

    # Recreate Permutated.csv w/ synthetic questions appended
    print(f'\nWriting to "{filenames["writefile"]}"...')
    file_io.write(filenames, permutated_store, employees, answers, nums)
    print("Done.\n")


def verify() -> int:
    """Determine whether the updated Permutated.csv has any modified or missing entries (and not just new ones)"""
    return_code: int
    writefile = os.path.expanduser("~/.chatbot-util/Permutated.csv")
    backupfile = writefile + ".backup"

    # pipe the diff into grep to ignore added entries
    diff = subprocess.run(
        [
            "diff",
            "--strip-trailing-cr",
            "-y",
            "--suppress-common-lines",
            writefile,
            backupfile,
        ],
        stdout=subprocess.PIPE,
    )
    return_code = subprocess.run(
        ["grep", ">\\||"],
        input=diff.stdout,
        stdout=subprocess.PIPE,
    ).returncode

    if return_code == 1:
        verified_code = 201
    else:
        verified_code = 409

    return verified_code


if __name__ == "__main__":
    sys.exit(main())
