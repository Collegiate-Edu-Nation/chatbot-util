# chatbot-util
![Static Badge](https://img.shields.io/badge/Version-0.2-blue)
![Static Badge](https://img.shields.io/badge/Platforms-Linux,_macOS-green)
![Static Badge](https://img.shields.io/badge/Coverage-90%25-green)
![Static Badge](https://img.shields.io/badge/Powered_by_Nix-grey?logo=nixOS&logoColor=white)

Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format

Docs deployed at https://collegiate-edu-nation.github.io/chatbot-util<br>
<i>Docs cover instructions and source code reference</i>

## Setup
<b>Must install Ollama and flake-enabled Nix before running anything.</b>

Start Ollama server (second command only needs to be run if model has not already been installed):

    ollama serve
    ollama pull mistral

<i>Note: I recommend running Ollama as a system service to avoid needing to run 'ollama serve' every time I boot.</i>

## Usage
Before the FAQ can be extended by the LLM, the initial FAQ must be added to ~/.chatbot-util/

A list of employees, phrases to substitute, and answers must also be included in ~/.chatbot-util/Other.txt (see docs for more explanation)

Once there, run the app

    nix run github:collegiate-edu-nation/chatbot-util

<i>*Note: Ollama must be running in the background in order for the app to actually get a response- see <b>Setup</b> for commands. It's also worthwhile to make sure the LLMs are running on your GPU, otherwise responses are unbearably slow</i>

This will create the extended FAQ in the same directory

## Advanced Usage
### Verify results
flake.nix contains a basic script for verifying that the output of running chatbot-util either exactly matches the preexisting Permutated.csv, or only contains new and unmodified entries. This is very helpful for ensuring deterministic output over time

Run this command to verify. If successful, 'verified' will be printed to console

    nix develop github:collegiate-edu-nation/chatbot-util --command bash -c "verify"

### Modifications
To edit the code itself, clone this repo

    git clone https://github.com/collegiate-edu-nation/chatbot-util.git

Modify src as desired and commit the changes

Run the app

    nix run /path/to/chatbot-util