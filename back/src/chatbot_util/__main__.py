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


def start() -> bool:
    """Create chain, read info from files, append generated questions, then write to new file, indicating whether the run was interrupted"""

    def handle_interrupt() -> bool:
        """Helper to reset chain state if interrupted"""
        interrupted = False
        if chain.interrupt:
            chain.interrupt = False
            chain.progress = chain.Progress(0)
            print("\nInterrupted.\n")
            interrupted = True

        return interrupted

    # Check interrupt status between operations to avoid undesired behavior
    if handle_interrupt():
        return True

    # Read topics and organic questions
    print("\nReading topics, questions, employees, and answers...")
    store, teams, employees, phrases, answers, nums = file_io.read()

    if handle_interrupt():
        return True

    # Generate synthetic questions
    permutated_store = chain.generate(store, phrases)

    if handle_interrupt():
        return True

    # Recreate Permutated.csv w/ synthetic questions appended
    print(f'\nWriting to "{file_io.FILENAMES["permutated"]}"...')
    file_io.write(permutated_store, teams, employees, answers, nums)
    print("Done.\n")

    return False


def verify() -> bool:
    """Determine whether the updated Permutated.csv has any modified or missing entries (and not just new ones)"""
    verified = True
    writefile = file_io.FILENAMES["permutated"]
    backupfile = writefile + ".backup"

    # return early when there's nothing to verify against
    if not os.path.exists(backupfile):
        return verified

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

    if return_code != 1:
        verified = False

    return verified


if __name__ == "__main__":
    sys.exit(main())
