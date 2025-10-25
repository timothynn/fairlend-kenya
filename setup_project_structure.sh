#!/bin/bash

# FairLend Kenya - Project Structure Setup Script
# This script creates all missing directories and placeholder files

set -e  # Exit on error

echo "🚀 Setting up FairLend Kenya project structure..."
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create data directories
echo -e "${BLUE}📁 Creating data directories...${NC}"
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/synthetic
echo -e "${GREEN}✓ Data directories created${NC}"

# Create notebook directory (if not exists)
echo -e "${BLUE}📁 Creating notebooks directory...${NC}"
mkdir -p notebooks
echo -e "${GREEN}✓ Notebooks directory ready${NC}"

# Create docs/presentation directory
echo -e "${BLUE}📁 Creating documentation directories...${NC}"
mkdir -p docs/presentation
echo -e "${GREEN}✓ Documentation directories created${NC}"

# Create demo/assets directories
echo -e "${BLUE}📁 Creating demo asset directories...${NC}"
mkdir -p demo/assets/images
echo -e "${GREEN}✓ Demo directories created${NC}"

# Create placeholder README files
echo -e "${BLUE}📄 Creating placeholder README files...${NC}"

# Data directory READMEs
cat > data/README.md << 'EOF'
# Data Directory

This directory contains all data files for FairLend Kenya.

## Structure

- `raw/` - Original/raw credit data files
- `processed/` - Cleaned and preprocessed data
- `synthetic/` - Generated synthetic fair datasets
- `sample_data.csv` - Sample Kenyan credit data for demonstration

## Usage

1. Generate sample data: `python notebooks/01_sample_data_generation.py`
2. Place your own credit data in the `raw/` folder
3. Use the notebooks to process and analyze data

## Data Privacy

⚠️ Never commit real customer data to version control!
All data files are ignored by `.gitignore`.
EOF

cat > data/raw/README.md << 'EOF'
# Raw Data

Place original credit data files here.

**Note:** This directory is empty by default and files here are gitignored.
EOF

cat > data/processed/README.md << 'EOF'
# Processed Data

Cleaned and preprocessed data files are stored here.

**Note:** Files in this directory are gitignored.
EOF

cat > data/synthetic/README.md << 'EOF'
# Synthetic Data

Generated synthetic fair credit datasets are stored here.

These datasets are created by FairLend's AI models and can be used
for training fair credit risk models.

**Note:** Files in this directory are gitignored.
EOF

# Demo assets README
cat > demo/assets/README.md << 'EOF'
# Demo Assets

This directory contains images, logos, and other assets for the Streamlit demo.

## Directory Structure

- `images/` - Images, charts, and visualizations

## Adding Assets

Place any demo-related media files here for use in the Streamlit app.
EOF

echo -e "${GREEN}✓ README files created${NC}"

# Create .gitkeep files to preserve empty directories in git
echo -e "${BLUE}📄 Creating .gitkeep files...${NC}"
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/synthetic/.gitkeep
touch demo/assets/images/.gitkeep
echo -e "${GREEN}✓ .gitkeep files created${NC}"

# Summary
echo ""
echo "=========================================="
echo "✨ Project structure setup complete!"
echo "=========================================="
echo ""
echo "Created directories:"
echo "  ├── data/"
echo "  │   ├── raw/"
echo "  │   ├── processed/"
echo "  │   └── synthetic/"
echo "  ├── notebooks/"
echo "  ├── docs/"
echo "  │   └── presentation/"
echo "  └── demo/"
echo "      └── assets/"
echo "          └── images/"
echo ""
echo "Next steps:"
echo "  1. Run: python generate_sample_data.py"
echo "  2. Open notebooks with: jupyter notebook"
echo "  3. Run demo: streamlit run demo/app.py"
echo ""
echo "Happy coding! 🇰🇪"
