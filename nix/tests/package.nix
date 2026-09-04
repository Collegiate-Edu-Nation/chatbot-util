# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

pkgs.writeShellScriptBin "chatbot-util" ''
  set -eu

  printf '%s\n' "$HOST:$PORT" > module-test
  exec ${pkgs.coreutils}/bin/sleep infinity
''
