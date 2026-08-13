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
  };

  config = lib.mkIf cfg.enable {
    users.groups.chatbot-util = { };
    users.users.chatbot-util = {
      description = "chatbot-util service user";
      group = "chatbot-util";
      home = "/etc/chatbot-util";
      isSystemUser = true;
    };

    systemd.tmpfiles.rules = [
      "d /etc/chatbot-util 0750 chatbot-util chatbot-util -"
    ];

    systemd.services.chatbot-util = {
      description = "chatbot-util web service";
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];

      serviceConfig = {
        ExecStart = lib.getExe cfg.package;
        Group = "chatbot-util";
        NoNewPrivileges = true;
        PrivateDevices = true;
        PrivateTmp = true;
        ProtectHome = true;
        ProtectSystem = "strict";
        ReadWritePaths = [ "/etc/chatbot-util" ];
        Restart = "on-failure";
        UMask = "0027";
        User = "chatbot-util";
        WorkingDirectory = "/etc/chatbot-util";
      };
    };
  };
}
