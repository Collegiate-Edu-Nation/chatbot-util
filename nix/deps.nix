# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

{
  build =
    with pkgs;
    [
      makeWrapper
    ]
    ++ (with python313Packages; [
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

      # scripts
      build
      docs
      format
      launch

      # script deps
      boxes
      nixfmt-rfc-style
      nodePackages.prettier
      taplo
    ]
    ++ (with python313Packages; [
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
