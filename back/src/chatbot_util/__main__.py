# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Entry point that launches a uvicorn server and connects the backend reading, generation, and writing functionalities"""

import logging
import os
import subprocess
import sys

import coloredlogs  # pyright: ignore [reportMissingTypeStubs]
import uvicorn

from chatbot_util import chain, file_io

# override logger's config in order to show non-uvicorn entries while attaching to it.
# setting the formatting and colors make it match for info msgs
format = "%(levelname)s:     chatbot_util    - %(message)s"
logging.basicConfig(level=logging.INFO, format=format)
logger = logging.getLogger("fastapi")
colors = coloredlogs.DEFAULT_FIELD_STYLES
colors["levelname"] = {"bold": False, "color": "green"}
coloredlogs.install(level="INFO", fmt=format, field_styles=colors)  # pyright: ignore [reportUnknownMemberType]

# not interested in info logs for httpx or ollama
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("ollama").setLevel(logging.WARNING)


def main() -> None:
    """Start uvicorn server"""
    host = "127.0.0.1"
    port = 8080

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
            logger.info("Interrupted")
            interrupted = True

        return interrupted

    # Check interrupt status between operations to avoid undesired behavior
    if handle_interrupt():
        return True

    # Read topics and organic questions
    logger.info("Reading topics, questions, employees, and answers.")
    store, teams, employees, phrases, answers, nums = file_io.read()

    if handle_interrupt():
        return True

    # Generate synthetic questions
    permutated_store = chain.generate(store, phrases)

    if handle_interrupt():
        return True

    # Recreate Permutated.csv w/ synthetic questions appended
    logger.info(f'Writing to "{file_io.FILENAMES["permutated"]}."')
    file_io.write(permutated_store, teams, employees, answers, nums)
    logger.info("Done")

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
