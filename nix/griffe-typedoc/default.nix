{ pkgs }:

pkgs.python313Packages.buildPythonPackage rec {
  pname = "griffe-typedoc";
  version = "0.1.0";
  pyproject = true;

  src = pkgs.fetchFromGitHub {
    owner = "mkdocstrings";
    repo = "griffe-typedoc";
    tag = version;
    hash = "sha256-ln9GL2NI/SmA3INgVuMjjd4/enK+0NS0nfT497mch7o=";
  };

  build-system = with pkgs.python313Packages; [ pdm-backend ];

  dependencies = with pkgs.python313Packages; [
    pydantic
  ];
}
