# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""API routes and implementations for the uvicorn server launched in __main__"""

import os

import ollama
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from chatbot_util import __main__, chain

app = FastAPI()

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    return {"detail": 200}


# serve react frontend on root
# mounting order matters - 404 if we mount frontend before establishing api paths
# creating a separate app for the api is a common approach, but this seems to work
app.mount(
    "/",
    StaticFiles(directory=os.getenv("FRONT_DIR", "../front/build"), html=True),
    name="frontend",
)
