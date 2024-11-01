# chatbot-util
![Static Badge](https://img.shields.io/badge/Version-0.2-blue)
![Static Badge](https://img.shields.io/badge/Platforms-Linux,_macOS-green)
![Static Badge](https://img.shields.io/badge/Coverage-73%25-green)
![Static Badge](https://img.shields.io/badge/Powered_by_Nix-grey?logo=nixOS&logoColor=white)

Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format

## Setup
<b>Must install Ollama and flake-enabled Nix before running anything.</b>

Start Ollama server (second command only needs to be run if model has not already been installed):

    ollama serve
    ollama pull mistral

<i>Note: I recommend running Ollama as a system service to avoid needing to run 'ollama serve' every time I boot.</i>

## Usage
Before the FAQ can be extended by the LLM, the initial FAQ must be added to ~/.chatbot-util/

Also, an updated employee list must be included in ~/.chatbot-util/employees.txt, and likewise for cen_answers.txt, robotics_answers.txt, instr_answers.txt, and phrases.txt

Once there, run the app:

    nix run github:collegiate-edu-nation/chatbot-util

<i>*Note: Ollama must be running in the background in order for the app to actually get a response- see <b>Setup</b> for commands. It's also worthwhile to make sure the LLMs are running on your GPU, otherwise responses are unbearably slow</i>

This will create the extended FAQ in the same directory. Make sure to cover both CEN and Collegiate Edu-Nation as appropriate in cen_answers.txt, as Gemini gets confused.


## Advanced Usage
To edit the code itself:

    git clone https://github.com/camdenboren/chatbot-util.git
    modify files in src as desired (and add new files to setup.py)
    nix run /path/to/chatbot-util
