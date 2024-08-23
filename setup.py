#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='chatbot-util',
    version='0.1',
    # Modules to import from other scripts:
    packages=find_packages(),
    # Executables
    scripts=[
        "src/chain.py",
        "src/employees.py",
        "src/file_io.py",
        "src/main.py",
        "src/parser.py"
    ]
)