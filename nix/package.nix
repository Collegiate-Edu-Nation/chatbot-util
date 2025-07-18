# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs, deps }:

let
  pname = "chatbot-util";
  version = "2.0.0";

  back = pkgs.python313Packages.buildPythonApplication {
    inherit pname version;
    pyproject = true;
    src = ../back/.;

    build-system = with pkgs.python313Packages; [ setuptools ];
    propagatedBuildInputs = deps.build;
  };

  front-build = pkgs.buildNpmPackage {
    inherit pname version;
    src = ../front/.;
    npmDepsHash = "sha256-UMyHZbT+pB5cmVX3wiQrug5zA+F2okHyK/vPwSl8kZI=";
  };

  front = pkgs.writeShellScriptBin "chatbot-util" ''
    ${pkgs.nodejs}/bin/npm run start --prefix ${front-build}/lib/node_modules/chatbot-util
  '';
in
{
  inherit back front;
  default = pkgs.writeShellScriptBin "chatbot-util" ''
    ${back}/bin/chatbot-util &
    ${front}/bin/chatbot-util
  '';
}
