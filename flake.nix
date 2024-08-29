{
  description = "chatbot-util Development Environment and Package via Nix Flake";

  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
  };

  outputs = { self, nixpkgs }: 
  let
    supportedSystems = [ "x86_64-linux" "aarch64-darwin" ];
    forEachSupportedSystem = function: nixpkgs.lib.genAttrs supportedSystems (system: function rec {
      pkgs = nixpkgs.legacyPackages.${system}.extend (final: prev: {
        python311 = prev.python311.override {
          packageOverrides = python311-final: python311-prev: {
            # Adding disabled test fixes build on darwin due to test_openai_schema failing with: Unclosed <MemoryObjectSendStream>
            fastapi = python311-prev.fastapi.overrideAttrs (old: {
              disabledTests = (old.disabledTests or []) ++ [
                "test_schema_extra_examples"
              ];
            });
          };
        };
      });
      deps = with pkgs.python311Packages; [
        langchain
        langchain-core
        langchain-community
      ];
    });
  in {
    devShells = forEachSupportedSystem ({ pkgs, deps }: {
      default = pkgs.mkShell {
        packages = with pkgs; [ 
          bashInteractive 
          python311 
        ] ++ deps;

        shellHook = ''
          echo -e "\nchatbot-util Development Environment via Nix Flake\n"
          python --version
        '';
      };
    });
    packages = forEachSupportedSystem ({ pkgs, deps }: {
      default = pkgs.python311Packages.buildPythonApplication {
        pname = "chatbot-util";
        version = "0.1";
        src = ./.;

        propagatedBuildInputs = deps;

        meta = {
          description = "Utility for generating similar FAQ's a la rag-fusion in a Dialogflow-ready, structured format.";
          maintainers = [ "camdenboren" ];
        };
      };
    });
  };
}