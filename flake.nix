{
  description = "Project Insight Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python310
            python310Packages.pip
            python310Packages.virtualenv
          ];

          shellHook = ''
            if [ ! -d ".venv" ]; then
              python -m venv .venv
            fi
            source .venv/bin/activate
            pip install -r requirements.txt
            echo "Python development environment activated!"
          '';
        };
      });
}
