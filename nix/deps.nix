# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

{
  build =
    with pkgs;
    [
      makeWrapper
    ]
    ++ (with python314Packages; [
      # backend
      coloredlogs
      fastapi
      fastapi-cli
      ollama
      uvicorn
      python-multipart
    ]);

  dev =
    with pkgs;
    [
      # backend
      pyright

      # frontend
      nodejs

      # testing
      cypress

      # scripts
      build
      docs
      format
      launch

      # script deps
      boxes
      nixfmt
      prettier
      taplo
    ]
    ++ (with python314Packages; [
      # backend
      coverage
      mockito
      mkdocs
      mkdocs-material
      mkdocstrings
      mkdocstrings-python
      ruff
    ]);
}
