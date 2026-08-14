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
  };

  config = lib.mkIf cfg.enable {
    users = lib.mkIf (cfg.user == defaultUser) {
      ${defaultUser} = {
        description = "chatbot-util service user";
        inherit (cfg) group;
        home = "/etc/chatbot-util";
        isSystemUser = true;
      };
    };
    groups = lib.mkIf (cfg.group == defaultGroup) { ${defaultGroup} = { }; };

    systemd.tmpfiles.rules = [
      "d /etc/chatbot-util 0750 chatbot-util chatbot-util -"
    ];

    systemd.services.chatbot-util = {
      description = "chatbot-util web service";
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];

      serviceConfig = {
        ExecStart = "${cfg.package}/bin/chatbot-util";
        User = "chatbot-util";
        Group = "chatbot-util";
        NoNewPrivileges = true;
        PrivateDevices = true;
        PrivateTmp = true;
        ProtectHome = true;
        ProtectSystem = "strict";
        ReadWritePaths = [ "/etc/chatbot-util" ];
        Restart = "on-failure";
        UMask = "0027";
        WorkingDirectory = "/etc/chatbot-util";
      };
    };
  };
}
