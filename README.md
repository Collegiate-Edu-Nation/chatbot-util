# chatbot-util

![Static Badge](https://img.shields.io/badge/Platforms-Linux,_macOS-blue?style=for-the-badge)
![Dynamic Badge](https://img.shields.io/github/actions/workflow/status/Collegiate-Edu-Nation/chatbot-util/build.yaml?branch=main&style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Powered_by_Nix-grey?logo=nixOS&logoColor=white&style=for-the-badge)

Utility for generating similar FAQs a la [RAG-Fusion] in a structured format ready for Google's Conversational Agents

Docs deployed at https://collegiate-edu-nation.github.io/chatbot-util<br>
_Docs cover instructions and source code reference_

## Screenshot

<img width="1763" alt="Screenshot of chatbot-util user interface" src="https://storage.googleapis.com/chatbot_util/chatbot-util.png" />

## Setup

**Must install Ollama (or at least have access to a valid installation at a remote URL) before running anything**

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

Before the FAQ can be extended by the LLM, download the initial FAQ and a list of teams, employees, phrases to substitute, and answers. An optional configuration file can also be downloaded to enable both remote Ollama servers and faster document access in the future (see docs for more explanation)

Once downloaded, create the extended FAQ in the OS-specific data directory by

- Launching both the back and frontends (follow one of [Nix](#nix) or [Non-Nix](#non-nix))
- Navigating to http://localhost:8080
- Uploading these files
- Clicking `Generate`

Once the operation completes, the extended FAQ will be available to upload via Google Cloud Console

### Nix

For a one-off run, first create the data directory with access for your current user (substituting `/var/lib` -> `/Library/Application Support` on macOS):

```shell
sudo install -d -m 0750 -o "$(id -un)" -g "$(id -gn)" /etc/chatbot-util
sudo install -d -m 0750 -o "$(id -un)" -g "$(id -gn)" /var/lib/chatbot-util
```

Then launch chatbot-util:

```shell
nix run github:collegiate-edu-nation/chatbot-util
```

Leverage our binary cache by adding [Cachix] to your nix-config

```nix
nix.settings.substituters = [ "https://edu-nation.cachix.org" ];
nix.settings.trusted-public-keys = [ "edu-nation.cachix.org-1:S2s7ZDuLeFrV2qhfzXWNt+/XlnGxUjvUHv0WI+BvM+0=" ];
```

### Non-Nix

After creating the relevant directories per [Nix](#nix), build the frontend (tested with node v24.18.1)

```shell
{
cd front
npm i
npm run build
cd ..
}
```

Then build and launch the backend (tested with python v3.14.6)

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

Then, add chatbot-util as a system service

> On NixOS

```nix
{
  imports = [ inputs.chatbot-util.nixosModules.default ];
  services.chatbot-util = {
    enable = true;
    host = "0.0.0.0";
    port = 9090;
  };
}
```

> On nix-darwin

```nix
{
  imports = [ inputs.chatbot-util.darwinModules.default ];
  services.chatbot-util = {
    enable = true;
    host = "0.0.0.0";
    port = 9090;
  };
}
```

After rebuilding the system, the service is available on the configured port.

The Nix module options supply `HOST` and `PORT`, so they take precedence over `[server].host` and `[server].port` in `/etc/chatbot-util/config.toml`.

This enables publicizing the server configuration w/o exposing links to sensitive files (e.g., the FAQ)

### Non-Nix

As this is currently just an internal tool, we don't have plans to streamline the installation process for non-Nix users

However, wrapping the backend's python executable with the location of the built `FRONT_DIR` before adding it to your path should do the trick. See the `postInstall` script in [package.nix] for further reference. The process must also have read/write access to `/etc/chatbot-util/`

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

[RAG-Fusion]: https://arxiv.org/abs/2402.03367
[Cachix]: https://www.cachix.org/
[GPLv3]: COPYING
[package.nix]: nix/package.nix
