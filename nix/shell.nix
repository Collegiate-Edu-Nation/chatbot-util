# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

{
  default = pkgs.mkShell {
    packages = deps.dev;
    buildInputs = deps.build;

    shellHook = ''
      export DEV=true
      echo -e "\nchatbot-util DevShell via Nix Flake\n"

      echo -e "┌───────────────────────────────────────────────────┐"
      echo -e "│                  Useful Commands                  │"
      echo -e "├──────────────┬────────────────────────────────────┤"
      echo -e "│ Launch       │ $ launch                           │"
      echo -e "│ Build        │ $ build                            │"
      echo -e "│ Docs         │ $ docs                             │"
      echo -e "│ Format       │ $ format                           │"
      echo -e "│ Run (Back)   │ $ python -m src.chatbot_util       │"
      echo -e "│ Test (Back)  │ $ python -m unittest               │"
      echo -e "│ Run (Front)  │ $ npm run dev                      │"
      echo -e "│ Test (Front) │ $ npm test                         │"
      echo -e "│ Coverage     │ $ coverage run -m unittest         │"
      echo -e "│ mkDocs       │ $ mkdocs {build, serve, gh-deploy} │"
      echo -e "└──────────────┴────────────────────────────────────┘"
    '';
  };
}
