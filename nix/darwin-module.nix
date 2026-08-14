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
      defaultText = lib.literalExpression "inputs.chatbot-util.packages.${pkgs.stdenv.hostPlatform.system}.default";
      description = "The chatbot-util package to run.";
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
    launchd.daemons.chatbot-util = {
      script = ''
        ${pkgs.coreutils}/bin/install -d -m 0750 -o root -g wheel /etc/chatbot-util
        cd /etc/chatbot-util
        exec ${cfg.package}/bin/chatbot-util
      '';

      serviceConfig = {
        EnvironmentVariables = {
          HOST = cfg.host;
          PORT = toString cfg.port;
        };
        UserName = "root";
        GroupName = "wheel";
        KeepAlive = true;
        ProcessType = "Background";
        RunAtLoad = true;
        StandardOutPath = "/var/log/chatbot-util.log";
        Umask = 23;
      };
    };
  };
}
