# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{
  nixosModule,
  pkgs,
}:

let
  testPackage = import ./package.nix { inherit pkgs; };
in
pkgs.testers.runNixOSTest {
  name = "chatbot-util-module";

  nodes.machine = {
    imports = [ nixosModule ];

    services.chatbot-util = {
      enable = true;
      package = testPackage;
      host = "0.0.0.0";
      port = 9090;
    };
  };

  testScript = ''
    machine.start()
    machine.wait_for_unit("chatbot-util.service")
    machine.wait_until_succeeds(
        "test -f /var/lib/chatbot-util/module-test"
    )

    service_user = machine.succeed(
        "systemctl show chatbot-util.service --property User --value"
    ).strip()
    assert service_user == "chatbot-util", service_user

    endpoint = machine.succeed(
        "cat /var/lib/chatbot-util/module-test"
    ).strip()
    assert endpoint == "0.0.0.0:9090", endpoint

    config_owner_mode = machine.succeed(
        "stat -c '%U:%G:%a' /etc/chatbot-util"
    ).strip()
    assert config_owner_mode == "chatbot-util:chatbot-util:750", config_owner_mode
  '';
}
