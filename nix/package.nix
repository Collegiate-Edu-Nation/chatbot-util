# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

{
  default = pkgs.python313Packages.buildPythonApplication {
    pname = "chatbot-util";
    version = "1.2.0";
    pyproject = true;
    src = ../.;

    build-system = with pkgs.python313Packages; [ setuptools ];
    propagatedBuildInputs = deps.build;

    meta = {
      description = "Utility for generating similar FAQ's a la rag-fusion in a structured format ready for Google's Conversational Agents";
      maintainers = [ "camdenboren" ];
    };
  };
}
