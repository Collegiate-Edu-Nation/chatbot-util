# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

let
  ollama = pkgs.ollama-cpu;

  tinyModel = pkgs.fetchurl {
    name = "smollm2-135m.gguf";
    url = "https://registry.ollama.ai/v2/library/smollm2/blobs/sha256:f535f83ec568d040f88ddc04a199fa6da90923bbb41d4dcaed02caa924d6ef57";
    hash = "sha256-9TX4PsVo0ED4jdwEoZn6bakJI7u0HU3K7QLKqSTW71c=";
  };

  modelFile = pkgs.writeText "chatbot-util-test.Modelfile" ''
    FROM ${tinyModel}
    PARAMETER temperature 0
    PARAMETER seed 39
    PARAMETER num_ctx 512
    PARAMETER num_predict 64
  '';

  # might work w/ this file empty as well
  faq = pkgs.writeText "FAQ - Enter Here.csv" ''
    Person/Entity,Questions
    CEN,What is CEN?
  '';

  other = pkgs.writeText "Other.txt" "";

  cypressCli = pkgs.buildNpmPackage {
    pname = "chatbot-util-cypress-runner";
    version = "1.0.0";
    src = ./cypress;

    env.CYPRESS_INSTALL_BINARY = 0;
    npmDepsHash = "sha256-Vx97aHZRJH4mquy3BJDTZHz8wipzZtrinrMMxEskNqo=";
    dontNpmBuild = true;

    installPhase = ''
      runHook preInstall

      runner="$out/lib/node_modules/chatbot-util-cypress-runner"
      mkdir -p "$runner/cypress"
      cp -r node_modules "$runner/"
      cp ${./cypress/package.json} "$runner/package.json"
      cp ${./cypress/package-lock.json} "$runner/package-lock.json"
      cp -r ${../../front/cypress/e2e} "$runner/cypress/e2e"
      cp -r ${../../front/cypress/fixtures} "$runner/cypress/fixtures"
      cp -r ${../../front/cypress/support} "$runner/cypress/support"
      cp ${../../front/cypress.config.js} "$runner/cypress.config.mjs"
      cp ${../../front/tsconfig.json} "$runner/tsconfig.json"
      cp ${../../front/tsconfig.app.json} "$runner/tsconfig.app.json"
      cp ${../../front/tsconfig.node.json} "$runner/tsconfig.node.json"

      runHook postInstall
    '';
  };

  cypressBinary =
    if pkgs.stdenv.hostPlatform.isDarwin then
      "${pkgs.cypress}/opt/cypress/Cypress.app/Contents/MacOS/Cypress"
    else
      "${pkgs.cypress}/bin/Cypress";

  cypress = pkgs.writeShellApplication {
    name = "chatbot-util-cypress";
    runtimeInputs = [
      pkgs.coreutils
      pkgs.nodejs
    ]
    ++ pkgs.lib.optionals pkgs.stdenv.hostPlatform.isLinux [ pkgs.xvfb-run ];
    text = ''
      test_home=$(mktemp -d)
      trap 'rm -rf "$test_home"' EXIT

      export CI=1
      export CYPRESS_INSTALL_BINARY=0
      export CYPRESS_RUN_BINARY=${cypressBinary}
      export HOME="$test_home"
      mkdir -p /tmp/chatbot-util-cypress

      runner=${cypressCli}/lib/node_modules/chatbot-util-cypress-runner
      test_project="$test_home/project"
      mkdir -p "$test_project"
      cp -r "$runner/cypress" "$test_project/cypress"
      cp "$runner/cypress.config.mjs" "$test_project/cypress.config.mjs"
      cp "$runner"/tsconfig*.json "$test_project/"
      chmod -R u+w "$test_project"
      ln -s "$runner/node_modules" "$test_project/node_modules"

      ${pkgs.lib.optionalString pkgs.stdenv.hostPlatform.isLinux "xvfb-run --auto-servernum "}node \
        "$runner/node_modules/cypress/bin/cypress" \
        run \
        --browser electron \
        --config baseUrl=http://127.0.0.1:9090 \
        --project "$test_project"
    '';
  };
in
{
  inherit
    cypress
    faq
    modelFile
    ollama
    other
    ;
}
