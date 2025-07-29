# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""API routes and implementations for the uvicorn server launched in __main__"""

import os
import time

import ollama
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from chatbot_util import __main__, chain

app = FastAPI()

DEV = True if os.getenv("DEV", "false") == "true" else False
FRONT_PORT = 5173 if DEV else 8080

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{FRONT_PORT}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

allow_generate = True


@app.get("/api/health")
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


@app.post("/api/generate")
def generate() -> dict[str, int]:
    """Create chain, read info from files, append generated questions, then write to new file

    "detail"\n
    201 = successfully generated Permutated.csv\n
    429 = request denied because generation is in progress\n
    500 = generic internal error encountered\n\n
    "verified"\n
    201 = verified\n
    409 = unverified, check diff\n
    500 = generic internal error encountered
    """

    status_code: int
    verified_code: int

    # generate new Permutated.csv
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

    # identify whether new Permutated.csv is verified
    try:
        verified_code = __main__.verify()
    except Exception:
        verified_code = 500

    return {"detail": status_code, "verified": verified_code}


@app.get("/api/progress")
def progress() -> dict[str, int]:
    """Report on generation progress

    index = index of topic currently generating queries for,  [1-total]\n
    total = total number of topics to generate queries for
    """
    return {"index": chain.progress.index, "total": chain.progress.total}


@app.get("/api/interrupt")
def interrupt() -> dict[str, int]:
    """Interrupt the current generation task

    200 = successfully interrupted generation of Permutated.csv\n
    500 = generic internal error encountered
    """
    chain.interrupt = True
    while chain.progress.index != 0:
        time.sleep(0.1)
    return {"detail": 200}


# serve react frontend on root in production - DEV benefits from live reloads
# mounting order matters - 404 if we mount frontend before establishing api paths
# creating a separate app for the api is a common approach, but this seems to work
if not DEV:
    app.mount(
        "/",
        StaticFiles(directory=os.getenv("FRONT_DIR", "../front/dist"), html=True),
        name="frontend",
    )
