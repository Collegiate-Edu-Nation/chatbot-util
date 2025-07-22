# chatbot-util

![Static Badge](https://img.shields.io/badge/Platforms-Linux,_macOS-forestgreen?style=for-the-badge)
[![built with garnix](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fgarnix.io%2Fapi%2Fbadges%2FCollegiate-Edu-Nation%2Fchatbot-util%3Fbranch%3Dmain&style=for-the-badge&color=grey&labelColor=grey)](https://garnix.io/repo/Collegiate-Edu-Nation/chatbot-util)
![Static Badge](https://img.shields.io/badge/Powered_by_Nix-grey?logo=nixOS&logoColor=white&style=for-the-badge)

Utility for generating similar FAQ's a la rag-fusion in a structured format ready for Google's Conversational Agents

Docs deployed at https://collegiate-edu-nation.github.io/chatbot-util<br>
_Docs cover instructions and source code reference_

## Setup

**Must install Ollama and flake-enabled Nix before running anything**

Start Ollama server<br>
_I recommend running Ollama as a system service to avoid running this all the time_

```shell
ollama serve
```

Download the LLM<br>
_Only needs to be run if `mistral` has not already been downloaded_

```shell
ollama pull mistral
```

## Usage

Before the FAQ can be extended by the LLM, the initial FAQ must be added to `~/.chatbot-util/`

A list of employees, phrases to substitute, and answers must also be included in `~/.chatbot-util/Other.txt` (see docs for more explanation)

Once there, create the extended FAQ in the same directory by launching both the back and frontends (follow one of [Nix](#nix) or [Non-Nix](#non-nix))

And navigating to http://localhost:8080

### Nix

```shell
nix run github:collegiate-edu-nation/chatbot-util
```

Leverage the binary cache by adding [Garnix] to your nix-config

```nix
nix.settings.substituters = [ "https://cache.garnix.io" ];
nix.settings.trusted-public-keys = [ "cache.garnix.io:CTFPyKSLcx5RMJKfLo5EEPUObbA78b0YQ2DTCJXqr9g=" ];
```

### Non-Nix

Build the frontend (tested with node v22.14.0)

```shell
{
cd front
npm i
npm run build
cd ..
}
```

Then build and launch the backend (tested with python v3.13.3)

```shell
{
cd back
pip install .
chatbot-util
}
```

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

Modify `src` as desired and add the changes<br>
_The `build` and `format` scripts will be helpful here_

### Parallelism

This app intentionally submits requests to Ollama in a sequential manner as, in my testing, parallelism breaks Ollama's determinism in unpredictable ways

If this isn't important for your use-case, leverage the `feat-concurrent-requests` branch for an ~80% speedup (this figure was observed on an M2 Pro w/ `OLLAMA_NUM_PARALLEL` set to 8)

## License

[GPLv3]

[Garnix]: https://garnix.io/
[GPLv3]: COPYING
