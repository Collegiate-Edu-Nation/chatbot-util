# chatbot-util

Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format.

Powered by Nix ❄️

<details>
<summary><b>Setup</b></summary>
<b>Important: Linux, MacOS, and WSL are supported. Must install Ollama and flake-enabled Nix before running anything.</b>

Start Ollama server (second command only needs to be run if model has not already been installed):

    ollama serve
    ollama pull mistral

<i>Note: I recommend running Ollama as a system service to avoid needing to run 'ollama serve' every time I boot.</i>
</details>

<details>
<summary><b>Usage</b></summary>
Before the FAQ can be extended by the LLM, the initial FAQ must be added to ~/.chatbot-util/

Also, an updated employee list must be included in ~/.chatbot-util/employees.txt, and likewise for cen_answers.txt, robotics_answers.txt, instr_answers.txt, and phrases.txt

Once there, run the app:

    nix run github:collegiate-edu-nation/chatbot-util

<i>*Note: Ollama must be running in the background in order for the app to actually get a response- see <b>Setup</b> for commands. It's also worthwhile to make sure the LLMs are running on your GPU, otherwise responses are unbearably slow</i>

This will create the extended FAQ in the same directory. Make sure to cover both CEN and Collegiate Edu-Nation as appropriate in cen_answers.txt, as Gemini gets confused.
</details>

<details>
<summary><b>Advanced Usage</b></summary>
To edit the code itself:

    git clone https://github.com/camdenboren/chatbot-util.git
    modify files in src as desired (and add new files to setup.py)
    nix run /path/to/chatbot-util
</details>
