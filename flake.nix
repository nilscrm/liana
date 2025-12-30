{
  description = "Liana: Vine linear program solver";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    vine = {
      url = "github:VineLang/vine";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    { self, nixpkgs, flake-utils, vine, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        vineCli = vine.packages.${system}.vine;

        inherit (pkgs.lib) fileset;

        lianaSrc = ./liana;

        liana = pkgs.runCommand "liana" { } ''
          cp -r ${fileset.toSource { root = ./.; fileset = lianaSrc; }} $out
        '';
      in
      {
        formatter = pkgs.nixfmt-tree;
        packages = {
          inherit liana;
          default = liana;
        };

        checks = {
          tests = pkgs.stdenvNoCC.mkDerivation {
            name = "liana-tests";
            src = fileset.toSource { root = ./.; fileset = fileset.unions [ lianaSrc ./tests ]; };
            nativeBuildInputs = [
              python
              vineCli
            ];
            buildPhase = ''
              python3 tests/run_tests.py
              touch $out
            '';
          };

          example = pkgs.stdenvNoCC.mkDerivation {
            name = "liana-example";
            src = fileset.toSource { root = ./.; fileset = fileset.unions [ lianaSrc ./example.vi ]; };
            nativeBuildInputs = [
              vineCli
            ];
            buildPhase = ''
              vine run --no-stats ./example.vi --lib liana/liana.vi
              touch $out
            '';
          };
        };

        devShells.default = pkgs.mkShell {
          packages = [
            python
            vineCli
          ];
        };
      }
    );
}
