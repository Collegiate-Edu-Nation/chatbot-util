# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

let
  pname = "chatbot-util";
  version = "2.0.0";

  front = pkgs.buildNpmPackage {
    inherit pname version;
    src = ../front/.;

    npmDepsHash = "sha256-fiQ1MEeXzANs+m9wPzoXUB6vcRP4kuzIRZh9zmu0Mdw=";
    postInstall = ''
      cp -r dist/ $out/lib/node_modules/chatbot-util/
    '';
  };
in
{
  inherit front;
  default = pkgs.python313Packages.buildPythonApplication {
    inherit pname version;
    pyproject = true;
    src = ../back/.;

    build-system = with pkgs.python313Packages; [ setuptools ];
    propagatedBuildInputs = deps.build;
    postInstall = ''
      wrapProgram "$out/bin/chatbot-util" --set \
        FRONT_DIR "${front}/lib/node_modules/chatbot-util/dist"
    '';
  };
}
