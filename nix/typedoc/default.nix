# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{
  stdenv,
  fetchFromGitHub,
  nodejs,
  pnpm,
  typescript,
}:

stdenv.mkDerivation rec {
  pname = "typedoc";
  version = "0.28.14";
  src = fetchFromGitHub {
    owner = "TypeStrong";
    repo = pname;
    rev = "v${version}";
    hash = "sha256-30HOFaQgbOyyKrPbRfpjrSL+YHJsEKlT1gb/GdAIa+o=";
  };

  nativeBuildInputs = [
    nodejs
    pnpm.configHook
    typescript
  ];

  pnpmDeps = pnpm.fetchDeps {
    inherit pname version src;
    fetcherVersion = 2;
    hash = "sha256-tjCgYO3Biws2lcmuP5SGorkoQ44MO81OLrgheu+WfQY=";
  };
  
  installPhase = ''
    mkdir -p $out/bin
    cp bin/typedoc $out/bin
  '';
}
