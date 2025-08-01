# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

let
  pname = "chatbot-util";
  version = "2.0.0";

  front = pkgs.buildNpmPackage {
    inherit pname version;
    src = ../front/.;

    npmDepsHash = "sha256-/c24orY5gem1m585CacXvZT9npzMw0Mf3iYjYLVSN3s=";
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
    build-system = with pkgs.python313Packages; [ setuptools ];
    propagatedBuildInputs = deps.build;
    postInstall = ''
      wrapProgram "$out/bin/chatbot-util" --set \
        FRONT_DIR "${front}/lib/node_modules/chatbot-util/dist"
    '';
  };
}
