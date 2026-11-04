# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

final: prev:
let
  # read script by name and patch bash shebang for nix users
  # see https://ertt.ca/nix/shell-scripts/
  writePatchedScript =
    name:
    (prev.writeScriptBin name (builtins.readFile ../script/${name})).overrideAttrs (old: {
      buildCommand = "${old.buildCommand}\n patchShebangs $out";
    });
  availableBinaries = {
    x86_64-linux = {
      platform = "linux-x64";
      hash = "sha256-mS6tiWbkbp5IiQ6zYbMzhZGmefMsnVC2maGaakgxys4=";
    };
    aarch64-linux = {
      platform = "linux-arm64";
      hash = "sha256-m6kgLcQE8drGGv+2ZgkytnEPyVfBbEJShGOz4cDGZPw=";
    };
    aarch64-darwin = {
      platform = "darwin-arm64";
      hash = "sha256-r8akzSxrjRrwE/Y5Y3rHgG4yr4FPRSX9eM5J7mriR6k=";
    };
  };
  inherit (prev.stdenv.hostPlatform) system;
  binary =
    availableBinaries.${system} or (throw "cypress: No binaries available for system ${system}");
  inherit (binary) platform hash;
in
{
  build = writePatchedScript "build";
  docs = writePatchedScript "docs";
  format = writePatchedScript "format";
  launch = writePatchedScript "launch";
  cypress = prev.cypress.overrideAttrs (o: rec {
    version = "16.2.1";
    meta = o.meta // {
      # The inherited warning concerns Electron 37.6.0;
      # Cypress 16.2.1 bundles Electron 41.7.0.
      knownVulnerabilities = [ ];
    };
    src = prev.fetchzip {
      url = "https://cdn.cypress.io/desktop/${version}/${platform}/cypress.zip";
      inherit hash;
      stripRoot = !prev.stdenv.hostPlatform.isDarwin;
    };
    installPhase =
      o.installPhase or ""
      +
        # cli usage via npx works on macOS once binary_state.json is writable
        # CYPRESS_SKIP_VERIFY=true didnt' work for me
        prev.lib.optionalString prev.stdenv.hostPlatform.isDarwin ''
          cp $out/binary_state.json $out/opt/cypress/binary_state.json
          chmod +w $out/opt/cypress/binary_state.json
        '';
  });
}
