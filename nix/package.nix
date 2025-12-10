# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

let
  pname = "chatbot-util";
  version = "2.0.0";

  front = pkgs.buildNpmPackage {
    inherit pname version;
    src = ../front/.;

    env.CYPRESS_INSTALL_BINARY = 0;
    npmDepsHash = "sha256-kGSg6vTcoO0gp/pjfNTHRGqgmySZ7LxcdENOv79lPts=";
    postInstall = ''
      cp -r dist/ $out/lib/node_modules/chatbot-util/
    '';
  };
in
{
  inherit front;
  default = pkgs.python313Packages.buildPythonApplication {
    inherit pname version;
    src = ../back/.;

    pyproject = true;
    dontCheckRuntimeDeps = true;
    propagatedBuildInputs = deps.build;
    build-system = with pkgs.python313Packages; [ setuptools ];
    postInstall = ''
      wrapProgram "$out/bin/chatbot-util" --set \
        FRONT_DIR "${front}/lib/node_modules/chatbot-util/dist"
    '';
  };
}
