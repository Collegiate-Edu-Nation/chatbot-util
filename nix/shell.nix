# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

{
  default = pkgs.mkShell {
    packages = deps.dev;
    buildInputs = deps.build;

    shellHook = ''
      echo -e "\nchatbot-util DevShell via Nix Flake\n"

      echo -e "┌───────────────────────────────────────────────┐"
      echo -e "│                Useful Commands                │"
      echo -e "├──────────┬────────────────────────────────────┤"
      echo -e "│ Build    │ $ build                            │"
      echo -e "│ Format   │ $ format                           │"
      echo -e "│ Verify   │ $ verify                           │"
      echo -e "│ Run      │ $ python -m src.chatbot_util       │"
      echo -e "│ Test     │ $ python -m unittest               │"
      echo -e "│ Coverage │ $ coverage run -m unittest         │"
      echo -e "│ Docs     │ $ mkdocs {build, serve, gh-deploy} │"
      echo -e "└──────────┴────────────────────────────────────┘"
    '';
  };
}
