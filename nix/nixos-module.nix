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
      description = "Fallback host for chatbot-util when server.host is not set in config.toml.";
    };

    port = lib.mkOption {
      type = lib.types.port;
      default = 8080;
      description = "Fallback port for chatbot-util when server.port is not set in config.toml.";
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
      };

      serviceConfig = {
        ExecStart = "${cfg.package}/bin/chatbot-util";
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
