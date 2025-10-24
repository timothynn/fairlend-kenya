{
  description = "FairLend Kenya - Synthetic Data for Inclusive Credit Models";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Python environment with all required dependencies
        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          # Core data science
          pandas
          numpy
          scikit-learn
          scipy
          
          # Machine Learning
          torch
          torchvision
          
          # Synthetic Data Generation
          # Note: sdv and ctgan might not be in nixpkgs, will need pip install
          
          # Visualization
          matplotlib
          seaborn
          plotly
          
          # Jupyter
          jupyter
          notebook
          ipykernel
          ipython
          
          # Web framework for demo
          streamlit
          
          # Development tools
          black
          pylint
          pytest
          pytest-cov
          python-lsp-server
          
          # Additional utilities
          requests
          tqdm
          pyyaml
          pip  # For installing packages not in nixpkgs
        ]);

      in {
        # Default package
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "fairlend-kenya";
          version = "0.1.0";
          src = ./.;
          
          buildInputs = [ pythonEnv ];
          
          installPhase = ''
            mkdir -p $out/bin $out/lib
            cp -r . $out/lib/fairlend
            
            # Create startup script for the demo
            cat > $out/bin/fairlend-demo <<EOF
            #!${pkgs.bash}/bin/bash
            cd $out/lib/fairlend
            export PYTHONPATH=$out/lib/fairlend/src:\$PYTHONPATH
            ${pythonEnv}/bin/streamlit run demo/app.py "\$@"
            EOF
            chmod +x $out/bin/fairlend-demo
            
            # Create startup script for Jupyter
            cat > $out/bin/fairlend-notebook <<EOF
            #!${pkgs.bash}/bin/bash
            cd $out/lib/fairlend
            export PYTHONPATH=$out/lib/fairlend/src:\$PYTHONPATH
            ${pythonEnv}/bin/jupyter notebook "\$@"
            EOF
            chmod +x $out/bin/fairlend-notebook
            
            # Create test runner script
            cat > $out/bin/fairlend-test <<EOF
            #!${pkgs.bash}/bin/bash
            cd $out/lib/fairlend
            export PYTHONPATH=$out/lib/fairlend/src:\$PYTHONPATH
            ${pythonEnv}/bin/pytest tests/ -v "\$@"
            EOF
            chmod +x $out/bin/fairlend-test
          '';
          
          meta = with pkgs.lib; {
            description = "Synthetic Data Generation for Inclusive Credit Risk Assessment in Kenya";
            homepage = "https://github.com/timothynn/fairlend-kenya";
            license = licenses.mit;
            maintainers = [ ];
          };
        };

        # Development shell
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.git
            pkgs.which
            pkgs.figlet
            pkgs.pandoc
            pkgs.texlive.combined.scheme-small
          ];

          shellHook = ''
            # ASCII Art welcome message
            ${pkgs.figlet}/bin/figlet "FairLend Kenya"
            echo "🇰🇪 Synthetic Data for Inclusive Credit Models"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            
            # Set up Python path
            export PYTHONPATH=$PWD/src:$PYTHONPATH
            
            # Create necessary directories if they don't exist
            mkdir -p data/{raw,processed,synthetic}
            mkdir -p notebooks tests docs/presentation demo/assets/images
            
            # Install additional Python packages not in nixpkgs
            echo "📦 Installing additional Python packages..."
            pip install --quiet --user aif360 sdv ctgan shap 2>/dev/null || true
            
            echo ""
            echo "✨ FairLend development environment activated!"
            echo ""
            echo "📁 Directory structure created"
            echo "🐍 PYTHONPATH set to include ./src"
            echo ""
            echo "Available commands:"
            echo "  streamlit run demo/app.py    # Launch Streamlit demo"
            echo "  jupyter notebook              # Launch Jupyter notebooks"
            echo "  pytest tests/ -v              # Run test suite"
            echo "  python -m pytest --cov=src    # Run tests with coverage"
            echo "  black src/ tests/             # Format code with Black"
            echo "  pylint src/                   # Lint source code"
            echo ""
            echo "Quick start:"
            echo "  cd notebooks && python 01_sample_data_generation.py"
            echo "  streamlit run demo/app.py"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          '';
        };

        # Nix apps for easy running
        apps = {
          # Run the demo
          demo = {
            type = "app";
            program = "${self.packages.${system}.default}/bin/fairlend-demo";
          };
          
          # Run Jupyter notebook
          notebook = {
            type = "app";
            program = "${self.packages.${system}.default}/bin/fairlend-notebook";
          };
          
          # Run tests
          test = {
            type = "app";
            program = "${self.packages.${system}.default}/bin/fairlend-test";
          };
        };

        # Formatter for nix files
        formatter = pkgs.nixpkgs-fmt;
      }
    );
}
