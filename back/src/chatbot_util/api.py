# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""API routes and implementations for the uvicorn server launched in __main__"""

import os
import time

import ollama
from fastapi import FastAPI, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from chatbot_util import __main__, chain, file_io
from chatbot_util.file_io import FILENAMES

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
def health() -> None:
    """Health check for both uvicorn and ollama servers

    status\n
    200 = uvicorn and ollama are ready
    """
    ollama.show("mistral")


@app.post("/api/generate", status_code=status.HTTP_201_CREATED)
def generate(response: Response) -> dict[str, bool | None]:
    """Create chain, read info from files, append generated questions, then write to new file

    status\n
    201 = successfully generated Permutated.csv\n
    429 = request denied because generation is in progress\n\n
    verified\n
    True = verified\n
    False = unverified, check diff\n
    None = generation interrupted
    """

    # generate new Permutated.csv
    verified = None
    interrupted = False
    global allow_generate
    if allow_generate:
        allow_generate = False
        interrupted = __main__.start()
        allow_generate = True
    else:
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS

    # identify whether new Permutated.csv is verified, ignoring interruption case
    if not interrupted:
        verified = __main__.verify()

    return {"verified": verified}


@app.get("/api/progress")
def progress() -> dict[str, int]:
    """Report on generation progress

    status\n
    200 = successfully retrieved progress status\n\n
    index = index of topic currently generating queries for,  [1-total]\n
    total = total number of topics to generate queries for
    """
    return {"index": chain.progress.index, "total": chain.progress.total}


@app.get("/api/interrupt")
def interrupt() -> None:
    """Interrupt the current generation task

    200 = successfully interrupted generation of Permutated.csv
    """
    chain.interrupt = True
    while chain.progress.index != 0:
        time.sleep(0.1)


@app.post("/api/upload", status_code=status.HTTP_201_CREATED)
def upload(files: list[UploadFile]) -> dict[str, bool]:
    """Replace data files via upload and return list of status codes

    status\n
    201 = no errors encountered when replacing file(s)\n
    422 = validation error while processing file(s)\n\n
    uploaded\n
    True = succssfully replaced all files\n
    False = some files failed to be replaced
    """
    uploaded = True
    for f in files:
        if file_io.create_file(f) is not True:
            uploaded = False
            break

    return {"uploaded": uploaded}


@app.get("/api/files")
def files() -> dict[str, bool]:
    """Report on data file status

    status\n
    200 = no errors encountered while scanning for files\n
    present\n
    True = all files are present\n
    False = some files are missing
    """
    present = True
    filenames = [FILENAMES["faq"], FILENAMES["other"], FILENAMES["config"]]

    for f in filenames:
        if not os.path.exists(f):
            present = False
            break

    return {"present": present}


@app.get("/api/config")
def config() -> dict[str, str]:
    """Return CDN links to 'FAQ - Enter Here.csv' and 'Other.txt'

    status\n
    200 = no errors encountered while reading links from config\n\n
    faq = CDN link to 'FAQ - Enter Here.csv'\n
    other = CDN link to 'Other.txt'\n
    """
    return file_io.read_config()


# serve react frontend on root in production - DEV benefits from live reloads
# mounting order matters - 404 if we mount frontend before establishing api paths
# creating a separate app for the api is a common approach, but this seems to work
if not DEV:
    app.mount(
        "/",
        StaticFiles(directory=os.getenv("FRONT_DIR", "../front/dist"), html=True),
        name="frontend",
    )
