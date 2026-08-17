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
      description = "Fallback host for chatbot-util when server.host is not set in config.toml.";
    };

    port = lib.mkOption {
      type = lib.types.port;
      default = 8080;
      description = "Fallback port for chatbot-util when server.port is not set in config.toml.";
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
