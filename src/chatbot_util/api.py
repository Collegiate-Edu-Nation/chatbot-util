# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""API routes and implementations for the uvicorn server launched in __main__"""

import ollama
from fastapi import FastAPI

from chatbot_util import __main__, chain

app = FastAPI()

allow_generate = True


@app.get("/health")
def health() -> dict[str, int]:
    """Health check for both uvicorn and ollama servers

    200 = uvicorn and ollama are ready\n
    500 = generic internal error encountered
    """
    status_code: int
    try:
        ollama.show("mistral")
        status_code = 200
    except Exception:
        status_code = 500

    return {"detail": status_code}


@app.post("/generate")
def generate() -> dict[str, int]:
    """Create chain, read info from files, append generated questions, then write to new file

    201 = successfully generated Permutated.csv\n
    429 = request denied because generation is in progress\n
    500 = generic internal error encountered
    """
    status_code: int
    try:
        global allow_generate
        if allow_generate:
            allow_generate = False
            __main__.start()
            allow_generate = True
            status_code = 201
        else:
            status_code = 429
    except Exception:
        status_code = 500

    return {"detail": status_code}


@app.get("/progress")
def progress() -> dict[str, int]:
    """Report on generation progress

    index = index of topic currently generating queries for,  [1-total]\n
    total = total number of topics to generate queries for
    """
    return {"index": chain.progress.index, "total": chain.progress.total}
