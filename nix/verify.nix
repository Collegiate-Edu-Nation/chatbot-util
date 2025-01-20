# SPDX-FileCopyrightText: 2024-2025 Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

pkgs.writeShellScriptBin "verify" ''
  mv ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup
  python -m src.chatbot_util
  if ! [[ $(diff ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup) ]]; then
    echo -e "verified\n"
  elif ! [[ $(diff --strip-trailing-cr -y --suppress-common-lines ~/.chatbot-util/Permutated.csv ~/.chatbot-util/Permutated.csv.backup | grep ">\||") ]]; then
    echo -e "verified\n"
  else
    echo -e "unverified, check diff\n"
  fi
  rm ~/.chatbot-util/Permutated.csv
  mv ~/.chatbot-util/Permutated.csv.backup ~/.chatbot-util/Permutated.csv
''
