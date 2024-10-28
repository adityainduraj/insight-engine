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

        pythonPackages = pkgs.python310Packages;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            (python310.withPackages (ps: with ps; [
              pandas
              plotly
              numpy
              scikit-learn
              scipy
              streamlit
              pip
            ]))
            python310Packages.pip
          ];

          shellHook = ''
            # Create and activate a virtual environment if it doesn't exist
            if [ ! -d ".venv" ]; then
              python -m venv .venv
            fi
            source .venv/bin/activate
            
            # Install requirements from requirements.txt if needed
            pip install -r requirements.txt
            
            echo "Python development environment activated!"
          '';
        };
      });
}
