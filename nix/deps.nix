# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

{
  build = with pkgs.python313Packages; [
    fastapi
    fastapi-cli
    ollama
    uvicorn
  ];
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
      verify
    ]
    ++ (with pkgs.python313Packages; [
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
