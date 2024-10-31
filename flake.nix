{
  description = "chatbot-util Development Environment and Package via Nix Flake";

  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
  };

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
      forEachSupportedSystem =
        function:
        nixpkgs.lib.genAttrs supportedSystems (
          system:
          function rec {
            pkgs = nixpkgs.legacyPackages.${system};
            deps = with pkgs.python312Packages; [
              ollama
            ];
          }
        );
    in
    {
      devShells = forEachSupportedSystem (
        { pkgs, deps }:
        {
          default = pkgs.mkShell {
            packages =
              with pkgs;
              [
                bashInteractive
                python312
              ]
              ++ deps;

            shellHook = ''
              echo -e "\nchatbot-util Development Environment via Nix Flake\n"
              python --version
            '';
          };
        }
      );
      packages = forEachSupportedSystem (
        { pkgs, deps }:
        {
          default = pkgs.python312Packages.buildPythonApplication {
            pname = "chatbot-util";
            version = "0.2";
            src = ./.;

            propagatedBuildInputs = deps;

            meta = {
              description = "Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format.";
              maintainers = [ "camdenboren" ];
            };
          };
        }
      );
    };
}
