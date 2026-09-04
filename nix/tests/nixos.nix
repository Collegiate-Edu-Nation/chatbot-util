# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{
  nixosModule,
  pkgs,
}:

let
  support = import ./support.nix { inherit pkgs; };
in
pkgs.testers.runNixOSTest {
  name = "chatbot-util-module";

  nodes.machine = { pkgs, ... }: {
    imports = [ nixosModule ];

    virtualisation = {
      cores = 2;
      diskSize = 4096;
      memorySize = 4096;
    };

    users.users.cypress = {
      isNormalUser = true;
      group = "users";
    };

    services.ollama = {
      enable = true;
      package = support.ollama;
      environmentVariables.OLLAMA_NO_CLOUD = "1";
    };

    services.chatbot-util = {
      enable = true;
      host = "0.0.0.0";
      port = 9090;
    };

    systemd.services.chatbot-util.preStart = ''
      ${pkgs.coreutils}/bin/install -m 0640 ${support.faq} \
        "/var/lib/chatbot-util/FAQ - Enter Here.csv"
      ${pkgs.coreutils}/bin/install -m 0640 ${support.other} \
        "/var/lib/chatbot-util/Other.txt"
    '';
  };

  testScript = ''
    machine.start()
    machine.wait_for_unit("ollama.service")
    machine.wait_for_open_port(11434)

    machine.succeed(
        "OLLAMA_HOST=127.0.0.1:11434 "
        "${support.ollama}/bin/ollama create mistral "
        "--file ${support.modelFile}"
    )

    machine.wait_for_unit("chatbot-util.service")
    machine.wait_until_succeeds(
        "${pkgs.curl}/bin/curl --fail --silent "
        "http://127.0.0.1:9090/api/health"
    )

    service_user = machine.succeed(
        "systemctl show chatbot-util.service --property User --value"
    ).strip()
    assert service_user == "chatbot-util", service_user

    config_owner_mode = machine.succeed(
        "stat -c '%U:%G:%a' /etc/chatbot-util"
    ).strip()
    assert config_owner_mode == "chatbot-util:chatbot-util:750", config_owner_mode

    machine.succeed(
        "runuser -u cypress -- ${support.cypress}/bin/chatbot-util-cypress"
    )
    machine.wait_until_succeeds(
        "journalctl -u chatbot-util.service --no-pager "
        "| grep -Fq Interrupted"
    )
  '';
}
