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
    {
      self,
      nixpkgs,
      flake-utils,
      vine,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        vineCli = vine.packages.${system}.vine;

        inherit (pkgs.lib) fileset;
      in
      {
        formatter = pkgs.nixfmt-tree;

        checks = {
          tests = pkgs.stdenvNoCC.mkDerivation {
            name = "liana-tests";
            src = fileset.toSource {
              root = ./.;
              fileset = fileset.unions [
                ./liana
                ./tests
              ];
            };
            nativeBuildInputs = [
              python
              vineCli
            ];
            buildPhase = "python3 tests/run_tests.py";
            installPhase = "touch $out";
          };

          example = pkgs.stdenvNoCC.mkDerivation {
            name = "liana-example";
            src = fileset.toSource {
              root = ./.;
              fileset = fileset.unions [
                ./liana
                ./example.vi
              ];
            };
            nativeBuildInputs = [
              vineCli
            ];
            buildPhase = "vine run --no-stats ./example.vi --lib liana/liana.vi";
            installPhase = "touch $out";
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
