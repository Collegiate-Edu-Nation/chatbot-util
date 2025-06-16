# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

{
  build = with pkgs.python312Packages; [ ollama ];
  dev =
    with pkgs;
    [
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
    ]);
}
