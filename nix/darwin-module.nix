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
    launchd.daemons.chatbot-util = {
      script = ''
        ${pkgs.coreutils}/bin/install -d -m 0750 -o root -g wheel /etc/chatbot-util
        cd /etc/chatbot-util
        exec ${lib.getExe cfg.package}
      '';

      serviceConfig = {
        GroupName = "wheel";
        KeepAlive = true;
        ProcessType = "Background";
        RunAtLoad = true;
        Umask = 23;
        UserName = "root";
      };
    };
  };
}
