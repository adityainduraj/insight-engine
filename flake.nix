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
            # System dependencies
            stdenv.cc.cc.lib  # This provides libstdc++
            zlib  # Add zlib explicitly
            gcc
          ];

          shellHook = ''
            if [ ! -d ".venv" ]; then
              python -m venv .venv
            fi
            source .venv/bin/activate

            # Ensure pip is up to date
            pip install --upgrade pip

            # Install requirements
            pip install -r requirements.txt

            # Set LD_LIBRARY_PATH to find the required libraries
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:$LD_LIBRARY_PATH

            echo "Python development environment activated!"
          '';
        };
      });
}
