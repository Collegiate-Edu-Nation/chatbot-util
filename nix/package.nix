# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

{
  default = pkgs.python312Packages.buildPythonApplication {
    pname = "chatbot-util";
    version = "1.2.0";
    pyproject = true;
    src = ../.;

    build-system = with pkgs.python312Packages; [ setuptools ];
    propagatedBuildInputs = deps.build;

    meta = {
      description = "Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format";
      maintainers = [ "camdenboren" ];
    };
  };
}
