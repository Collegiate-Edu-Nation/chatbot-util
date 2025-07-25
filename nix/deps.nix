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
      fastapi
      fastapi-cli
      ollama
      uvicorn
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
