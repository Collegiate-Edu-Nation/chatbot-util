# chatbot-util

![Static Badge](https://img.shields.io/badge/Version-1.1-blue)
![Static Badge](https://img.shields.io/badge/Platforms-Linux,_macOS-forestgreen)
![Static Badge](https://img.shields.io/badge/Coverage-90%25-forestgreen)
![Static Badge](https://img.shields.io/badge/Powered_by_Nix-grey?logo=nixOS&logoColor=white)

Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format

Docs deployed at https://collegiate-edu-nation.github.io/chatbot-util<br>
_Docs cover instructions and source code reference_

## Setup

**Must install Ollama and flake-enabled Nix before running anything**

Start Ollama server (second command only needs to be run if model has not already been installed):

```shell
{
ollama serve
ollama pull mistral
}
```

_I recommend running Ollama as a system service to avoid needing to run 'ollama serve' every time I boot_

## Usage

Before the FAQ can be extended by the LLM, the initial FAQ must be added to `~/.chatbot-util/`

A list of employees, phrases to substitute, and answers must also be included in `~/.chatbot-util/Other.txt` (see docs for more explanation)

Once there, run the app

```shell
nix run github:collegiate-edu-nation/chatbot-util
```

This will create the extended FAQ in the same directory

## Advanced Usage

### Verify results

`flake.nix` contains a basic script for verifying that the output of running `chatbot-util` either exactly matches the preexisting `Permutated.csv`, or only contains new and unmodified entries. This is very helpful for ensuring deterministic output over time

Run this command to verify. If successful, `verified` will be printed to console

```shell
nix develop github:collegiate-edu-nation/chatbot-util --command bash -c "verify"
```

### Modifications

To edit the code itself, clone this repo

```shell
git clone https://github.com/collegiate-edu-nation/chatbot-util.git
```

Modify `src` as desired and add the changes

Run the app

```shell
nix run /path/to/chatbot-util
```

### License

[GPLv3](COPYING)
