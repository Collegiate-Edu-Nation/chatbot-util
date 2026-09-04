# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

# Building `.#checks.aarch64-darwin.darwinModule` evaluates and builds this
# configuration. CI additionally activates it on an ephemeral macOS runner and
# exercises Ollama, the launchd jobs, and Cypress via `testScript`.
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
      { lib, pkgs, ... }:
      let
        support = import ./support.nix { inherit pkgs; };
        dataDir = "/Library/Application Support/chatbot-util";
        ollamaDir = "/Library/Application Support/chatbot-util-test-ollama";
        ollamaLog = "/var/log/chatbot-util-test-ollama.log";
      in
      {
        system.stateVersion = 5;
        system.primaryUser = "runner";
        nix.enable = !activate;
        nixpkgs.overlays = [ (import ../overlay.nix) ];

        services.chatbot-util = {
          enable = true;
          host = "0.0.0.0";
          port = 9090;
        };

        system.activationScripts.launchd.text = lib.mkBefore ''
          ${pkgs.coreutils}/bin/install -d -m 0750 -o root -g wheel \
            ${lib.escapeShellArg dataDir} \
            ${lib.escapeShellArg ollamaDir} \
            ${lib.escapeShellArg "${ollamaDir}/models"}
          ${pkgs.coreutils}/bin/install -m 0640 -o root -g wheel \
            ${support.faq} \
            ${lib.escapeShellArg "${dataDir}/FAQ - Enter Here.csv"}
          ${pkgs.coreutils}/bin/install -m 0640 -o root -g wheel \
            ${support.other} \
            ${lib.escapeShellArg "${dataDir}/Other.txt"}
        '';

        launchd.daemons.ollama = {
          command = "${support.ollama}/bin/ollama serve";
          serviceConfig = {
            EnvironmentVariables = {
              HOME = ollamaDir;
              OLLAMA_HOST = "127.0.0.1:11434";
              OLLAMA_MODELS = "${ollamaDir}/models";
              OLLAMA_NO_CLOUD = "1";
            };
            GroupName = "wheel";
            KeepAlive = true;
            ProcessType = "Background";
            RunAtLoad = true;
            StandardErrorPath = ollamaLog;
            StandardOutPath = ollamaLog;
            UserName = "root";
            WorkingDirectory = ollamaDir;
          };
        };

        environment.systemPackages = [
          (pkgs.writeShellScriptBin "testScript" ''
            set -euo pipefail

            trap 'sudo launchctl print system/org.nixos.chatbot-util || true; sudo launchctl print system/org.nixos.ollama || true; sudo tail -n 100 /var/log/chatbot-util.log ${ollamaLog} || true' ERR

            sudo launchctl print system/org.nixos.ollama
            sudo launchctl print system/org.nixos.chatbot-util

            for _ in {1..60}; do
              if /usr/bin/curl --fail --silent http://127.0.0.1:11434/api/version >/dev/null; then
                break
              fi
              sleep 1
            done

            sudo env \
              HOME=${lib.escapeShellArg ollamaDir} \
              OLLAMA_HOST=127.0.0.1:11434 \
              OLLAMA_MODELS=${lib.escapeShellArg "${ollamaDir}/models"} \
              ${support.ollama}/bin/ollama create mistral --file ${support.modelFile}

            for _ in {1..60}; do
              if /usr/bin/curl --fail --silent http://127.0.0.1:9090/api/health >/dev/null; then
                break
              fi
              sleep 1
            done

            ${support.cypress}/bin/chatbot-util-cypress
            for _ in {1..60}; do
              if sudo grep -Fq Interrupted /var/log/chatbot-util.log; then
                break
              fi
              sleep 1
            done
            sudo grep -Fq Interrupted /var/log/chatbot-util.log
          '')
        ];
      }
    )
  ];
}
