# SPDX-FileCopyrightText: 2024 Collegiate Edu-Nation
#
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup

setup(
    name="chatbot-util",
    version="1.0",
    packages=["src"],
    scripts=[
        "src/chain.py",
        "src/file_io.py",
        "src/utils.py",
    ],
    entry_points={"console_scripts": ["chatbot-util = src.__main__:main"]},
)
