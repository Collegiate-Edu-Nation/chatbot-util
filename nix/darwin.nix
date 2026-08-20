# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ self }:
{
  config,
  lib,
  pkgs,
  ...
}:

let
  defaultUser = "root";
  defaultGroup = "wheel";
  configDir = "/etc/chatbot-util";
  dataDir = "/Library/Application Support/chatbot-util";
  logFile = "/var/log/chatbot-util.log";
  cfg = config.services.chatbot-util;
in
{
  options.services.chatbot-util = {
    enable = lib.mkEnableOption "chatbot-util";

    package = lib.mkOption {
      type = lib.types.package;
      default = self.packages.${pkgs.stdenv.hostPlatform.system}.default;
      defaultText = lib.literalExpression "inputs.chatbot-util.packages.${pkgs.stdenv.hostPlatform.system}.default";
      description = "The chatbot-util package to run.";
    };

    user = lib.mkOption {
      type = lib.types.str;
      default = defaultUser;
      description = "User account under which chatbot-util runs.";
    };

    group = lib.mkOption {
      type = lib.types.str;
      default = defaultGroup;
      description = "Group under which chatbot-util runs.";
    };

    host = lib.mkOption {
      type = lib.types.str;
      default = "127.0.0.1";
      description = "Listening host for chatbot-util; overrides server.host in config.toml.";
    };

    port = lib.mkOption {
      type = lib.types.port;
      default = 8080;
      description = "Listening port for chatbot-util; overrides server.port in config.toml.";
    };

    proxyAuth = {
      enable = lib.mkEnableOption "authentication asserted by a trusted reverse proxy";

      userHeader = lib.mkOption {
        type = lib.types.str;
        default = "X-Authenticated-User";
        description = ''
          Request header in which the trusted reverse proxy supplies the
          authenticated user. The service must remain unreachable except through
          that proxy when this option is enabled.
        '';
      };
    };

    ollama = {
      host = lib.mkOption {
        type = lib.types.nullOr lib.types.str;
        default = null;
        example = "https://ollama.com";
        description = "Optional Ollama API host; overrides ollama.url in config.toml.";
      };

      model = lib.mkOption {
        type = lib.types.nullOr lib.types.str;
        default = null;
        example = "gpt-oss:120b";
        description = "Optional Ollama model; overrides ollama.model in config.toml.";
      };

      apiKeyFile = lib.mkOption {
        type = lib.types.nullOr lib.types.str;
        default = null;
        example = "/run/secrets/chatbot-util-ollama-api-key";
        description = ''
          Runtime path to the Ollama API key. The path is passed to the service
          without copying the secret into the Nix store.
        '';
      };
    };
  };

  config = lib.mkIf cfg.enable {
    system.activationScripts.launchd.text = lib.mkBefore ''
      ${pkgs.coreutils}/bin/install -d -m 0750 -o ${cfg.user} -g ${cfg.group} \
        ${lib.escapeShellArg configDir} \
        ${lib.escapeShellArg dataDir}
    '';

    launchd.daemons.chatbot-util = {
      command = "${cfg.package}/bin/chatbot-util";

      serviceConfig = {
        EnvironmentVariables = {
          HOST = cfg.host;
          PORT = toString cfg.port;
          CHATBOT_UTIL_PROXY_AUTH = lib.boolToString cfg.proxyAuth.enable;
          CHATBOT_UTIL_AUTH_HEADER = cfg.proxyAuth.userHeader;
        }
        // lib.optionalAttrs (cfg.ollama.host != null) {
          OLLAMA_HOST = cfg.ollama.host;
        }
        // lib.optionalAttrs (cfg.ollama.model != null) {
          OLLAMA_MODEL = cfg.ollama.model;
        }
        // lib.optionalAttrs (cfg.ollama.apiKeyFile != null) {
          OLLAMA_API_KEY_FILE = cfg.ollama.apiKeyFile;
        };
        UserName = cfg.user;
        GroupName = cfg.group;
        KeepAlive = true;
        ProcessType = "Background";
        RunAtLoad = true;
        StandardOutPath = logFile;
        WorkingDirectory = dataDir;
        Umask = 23;
      };
    };
  };
}
