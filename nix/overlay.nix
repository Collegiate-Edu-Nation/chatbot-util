# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

{ pkgs }:

(final: prev: {
  build = pkgs.callPackage ./build.nix { };
  format = pkgs.callPackage ./format.nix { };
  launch = pkgs.callPackage ./launch.nix { };
  verify = pkgs.callPackage ./verify.nix { };
})
