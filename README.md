# chatbot-util

![Static Badge](https://img.shields.io/badge/Platforms-Linux,_macOS-forestgreen?style=for-the-badge)
[![built with garnix](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fgarnix.io%2Fapi%2Fbadges%2FCollegiate-Edu-Nation%2Fchatbot-util%3Fbranch%3Dmain&style=for-the-badge&color=grey&labelColor=grey)](https://garnix.io/repo/Collegiate-Edu-Nation/chatbot-util)
![Static Badge](https://img.shields.io/badge/Powered_by_Nix-grey?logo=nixOS&logoColor=white&style=for-the-badge)

Utility for generating similar FAQ's a la rag-fusion in a structured format ready for Google's Conversational Agents

Docs deployed at https://collegiate-edu-nation.github.io/chatbot-util<br>
_Docs cover instructions and source code reference_

## Showcase

<img width="1763" alt="Image" src="https://storage.googleapis.com/chatbot_util/chatbot-util.png" />

## Setup

**Must install Ollama before running anything**

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

Before the FAQ can be extended by the LLM, download the initial FAQ and a list of teams, employees, phrases to substitute, and answers. An optional configuration file can also be downloaded to enable faster access in the future (see docs for more explanation)

Once downloaded, create the extended FAQ in `~/.chatbot-util/` by

- Launching both the back and frontends (follow one of [Nix](#nix) or [Non-Nix](#non-nix))
- Navigating to http://localhost:8080
- Then upload these files and click `Generate`

Once the operation completes, the extended FAQ will be available to upload via Google Cloud Console

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

## Installation

### Nix

Add the following to your `flake.nix`

```nix
inputs = {
  nixpkgs = {
    url = "github:nixos/nixpkgs/nixos-unstable";
  };
  chatbot-util = {
    url = "github:collegiate-edu-nation/chatbot-util";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  ...
}
```

Then, add alc-calc to your packages

> For system wide installation in `configuration.nix`

```nix
environment.systemPackages = with pkgs; [
  inputs.chatbot-util.packages.${system}.default
];
```

> For user level installation in `home.nix`

```nix
home.packages = with pkgs; [
  inputs.chatbot-util.packages.${system}.default
];
```

### Non-Nix

As this is currently just an internal tool, we don't have plans to streamline the installation process for non-Nix users

However, wrapping the backend's python executable with the location of the built `FRONT_DIR` before adding it to your path should do the trick. See the `postInstall` script in [package.nix] for further reference

## Advanced Usage

### Verification

After `Generate` finishes, `chatbot-util` will automatically display a toast message if any previous entries in the extended FAQ are missing or modified, indicating the new FAQ is not verified

This can be very helpful for identifying regressions when you're just intending on adding new teams, employees, and/or questions

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
[package.nix]: nix/package.nix
