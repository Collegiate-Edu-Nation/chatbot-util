# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

pkgs.writeShellScriptBin "format" ''
  set -o pipefail
  box() { ${pkgs.boxes}/bin/boxes -d ansi -s $(tput cols); } 2> /dev/null
  failed() {
    echo -e "\n\033[1;31mFormat failed.\033[0m"
    exit 1
  }
  trap 'failed' ERR

  echo -e "\033[1;33mruff...\033[0m"
  (ruff check --fix && ruff format) | box

  echo -e "\n\033[1;33mtaplo...\033[0m"
  ${pkgs.taplo}/bin/taplo fmt 2> /dev/null | box

  echo -e "\n\033[1;33mnix...\033[0m"
  ${pkgs.nixfmt-rfc-style}/bin/nixfmt flake.nix **/*.nix | box

  echo -e "\n\033[1;33mprettier...\033[0m"
  ${pkgs.nodePackages.prettier}/bin/prettier \
  --write **/*.yaml **/*.md | box

  echo -e "\n\033[1;32mFormat succeeded.\033[0m"
''
