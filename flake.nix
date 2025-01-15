# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{
  description = "chatbot-util Development Environment and Package via Nix Flake";

  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
  };

  outputs =
    { nixpkgs, ... }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
      forEachSupportedSystem =
        function:
        nixpkgs.lib.genAttrs supportedSystems (
          system:
          function rec {
            pkgs = nixpkgs.legacyPackages.${system};
            deps = with pkgs.python312Packages; [
              ollama
            ];
          }
        );
    in
    {
      devShells = forEachSupportedSystem (
        { pkgs, deps }:
        {
          default = pkgs.mkShell {
            packages =
              with pkgs;
              [
                bashInteractive
                python312
                (writeShellScriptBin "verify" ''
                  mv ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup
                  python -m src
                  if ! [[ $(diff ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup) ]]; then
                    echo -e "verified\n"
                  elif ! [[ $(diff --strip-trailing-cr -y --suppress-common-lines ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup | grep ">\||") ]]; then
                    echo -e "verified\n"
                  else
                    echo -e "unverified, check diff\n"
                  fi
                  rm ~/.chatbot-util/Permutated.csv
                  mv ~/.chatbot-util/Permutated.csv.backup ~/.chatbot-util/Permutated.csv
                '')
              ]
              ++ (with pkgs.python312Packages; [
                coverage
                mockito
                mkdocs
                mkdocs-material
                mkdocstrings
                mkdocstrings-python
              ])
              ++ deps;

            shellHook = ''
              echo -e "\nchatbot-util Development Environment via Nix Flake\n"
              echo -e "run:    python -m src"
              echo -e "verify: verify"
              echo -e "test:   python -m unittest discover"
              echo -e "cov:    coverage run --source=src,test -m unittest discover"
              echo -e "docs:   mkdocs build, serve, or gh-deploy\n"
              python --version
            '';
          };
        }
      );
      packages = forEachSupportedSystem (
        { pkgs, deps }:
        {
          default = pkgs.python312Packages.buildPythonApplication {
            pname = "chatbot-util";
            version = "1.1";
            src = ./.;

            propagatedBuildInputs = deps;

            meta = {
              description = "Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format";
              maintainers = [ "camdenboren" ];
            };
          };
        }
      );
    };
}
