# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

let
  # read script by name and patch bash shebang for nix users
  # see https://ertt.ca/nix/shell-scripts/
  writePatchedScript =
    name:
    (pkgs.writeScriptBin name (builtins.readFile ../script/${name})).overrideAttrs (old: {
      buildCommand = "${old.buildCommand}\n patchShebangs $out";
    });
in
(final: prev: {
  build = writePatchedScript "build";
  format = writePatchedScript "format";
  launch = writePatchedScript "launch";
})
