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
            pkgs = nixpkgs.legacyPackages.${system}.extend (import ./nix/overlay.nix { inherit pkgs; });
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
                build
                format
                verify
              ]
              ++ (with pkgs.python312Packages; [
                coverage
                mockito
                mkdocs
                mkdocs-material
                mkdocstrings
                mkdocstrings-python
                ruff
              ])
              ++ deps;

            shellHook = import ./nix/shellHook.nix;
          };
        }
      );
      packages = forEachSupportedSystem (
        { pkgs, deps }:
        {
          default = pkgs.python312Packages.buildPythonApplication {
            pname = "chatbot-util";
            version = "1.1";
            pyproject = true;
            src = ./.;

            build-system = with pkgs.python312Packages; [ setuptools ];
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
