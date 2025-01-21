# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

pkgs.writeShellScriptBin "verify" ''
  set -e

  # rename old output and execute
  mv ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup
  python -m src.chatbot_util

  # verify new output
  if ! [[ $(diff ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup) ]]; then
    echo -e "\033[1;32mVerified.\033[0m"
  elif ! [[ $(diff --strip-trailing-cr -y --suppress-common-lines ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup | grep ">\||") ]]; then
    echo -e "\033[1;32mVerified.\033[0m"
  else
    echo -e "\033[1;31mUnverified, check diff.\033[0m"
  fi

  # replace new output with old
  rm ~/.chatbot-util/Permutated.csv
  mv ~/.chatbot-util/Permutated.csv.backup ~/.chatbot-util/Permutated.csv
''
