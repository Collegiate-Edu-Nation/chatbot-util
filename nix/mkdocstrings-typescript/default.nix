{ pkgs }:

let
  griffe-typedoc = pkgs.callPackage ../griffe-typedoc {};
in
pkgs.python313Packages.buildPythonPackage rec {
  pname = "mkdocstrings-typescript";
  version = "0.1.0";
  pyproject = true;

  src = pkgs.fetchFromGitHub {
    owner = "mkdocstrings";
    repo = "typescript";
    tag = version;
    hash = "sha256-1wpRINBV5dvfCmtquDDzKsSC4b06jPVTElMr1uFLf0E=";
  };

  build-system = with pkgs.python313Packages; [ pdm-backend ];

  dependencies = with pkgs.python313Packages; [
    griffe-typedoc
    mkdocstrings
  ];
}
