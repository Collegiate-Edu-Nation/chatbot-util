from setuptools import setup

setup(
    name='chatbot-util',
    version='0.1',
    packages=["src"],
    scripts=[
        "src/chain.py",
        "src/file_io.py",
        "src/parser.py",
        "src/utils.py"
    ],
    entry_points={
        "console_scripts": [
            "chatbot-util = src.__main__:main"
        ]
    },
)