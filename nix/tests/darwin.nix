# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

# Building `.#checks.aarch64-darwin.darwinModule` evaluates and builds this
# configuration. CI additionally activates it on an ephemeral macOS runner and
# exercises the launchd job via `testScript`.
{
  nix-darwin,
  module,
  system,
  activate ? false,
}:

nix-darwin.lib.darwinSystem {
  inherit system;
  modules = [
    module
    (
      { pkgs, ... }:
      {
        system.stateVersion = 5;
        system.primaryUser = "runner";
        nix.enable = !activate;

        services.chatbot-util = {
          enable = true;
          package = import ./package.nix { inherit pkgs; };
          host = "0.0.0.0";
          port = 9090;
        };

        environment.systemPackages = [
          (pkgs.writeShellScriptBin "testScript" ''
            set -euo pipefail

            marker="/Library/Application Support/chatbot-util/module-test"
            trap 'sudo launchctl print system/org.nixos.chatbot-util || true; sudo cat "$marker" || true' ERR

            sudo launchctl print system/org.nixos.chatbot-util
            sudo launchctl kickstart -k system/org.nixos.chatbot-util

            for _ in {1..30}; do
              if sudo test -f "$marker"; then
                break
              fi
              sleep 1
            done

            test "$(sudo cat "$marker")" = "0.0.0.0:9090"
          '')
        ];
      }
    )
  ];
}
