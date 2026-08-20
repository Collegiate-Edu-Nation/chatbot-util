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
  defaultUser = "chatbot-util";
  defaultGroup = "chatbot-util";
  configDir = "/etc/chatbot-util";
  dataDir = "/var/lib/chatbot-util";
  cfg = config.services.chatbot-util;
in
{
  options.services.chatbot-util = {
    enable = lib.mkEnableOption "chatbot-util";

    package = lib.mkOption {
      type = lib.types.package;
      default = self.packages.${pkgs.stdenv.hostPlatform.system}.default;
      defaultText = lib.literalExpression "inputs.chatbot-util.packages.\${pkgs.stdenv.hostPlatform.system}.default";
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
          Runtime path to the Ollama API key. The file is loaded through a
          systemd credential and must not be placed in the Nix store.
        '';
      };
    };
  };

  config = lib.mkIf cfg.enable {
    users = {
      users = lib.mkIf (cfg.user == defaultUser) {
        ${defaultUser} = {
          description = "chatbot-util service user";
          inherit (cfg) group;
          home = configDir;
          isSystemUser = true;
        };
      };
      groups = lib.mkIf (cfg.group == defaultGroup) { ${defaultGroup} = { }; };
    };

    systemd.tmpfiles.rules = [
      "d ${configDir} 0750 ${cfg.user} ${cfg.group} -"
    ];

    systemd.services.chatbot-util = {
      description = "chatbot-util web service";
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];
      environment = {
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
      };

      serviceConfig = {
        ExecStart = "${cfg.package}/bin/chatbot-util";
        LoadCredential = lib.optional (
          cfg.ollama.apiKeyFile != null
        ) "ollama-api-key:${cfg.ollama.apiKeyFile}";
        User = cfg.user;
        Group = cfg.group;
        NoNewPrivileges = true;
        PrivateDevices = true;
        PrivateTmp = true;
        ProtectHome = true;
        ProtectSystem = "strict";
        StateDirectory = "chatbot-util";
        StateDirectoryMode = "0750";
        ReadWritePaths = [ configDir ];
        WorkingDirectory = dataDir;
        Restart = "on-failure";
        UMask = "0027";
      };
    };
  };
}
