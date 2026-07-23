{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python3
    git
    ruff
    python3Packages.pytest
  ];

  shellHook = ''
    echo
    echo "Entering Nix-Lock development environment"
    echo
  '';
}
