# FairLend Kenya - Complete Setup Guide

This guide will help you set up the complete FairLend Kenya project structure with all missing files and directories.

## 📋 Table of Contents
1. [Missing Files Checklist](#missing-files-checklist)
2. [Quick Setup](#quick-setup)
3. [Manual Setup](#manual-setup)
4. [Verification](#verification)
5. [Next Steps](#next-steps)

---

## Missing Files Checklist

Based on the README.md structure, here are the files/directories you need to create:

### ✅ Already Have
- [x] `.gitignore`
- [x] `LICENSE`
- [x] `README.md`
- [x] `requirements.txt`
- [x] `setup.py`
- [x] `flake.nix`
- [x] All source files in `src/`
- [x] Test files in `tests/`
- [x] `demo/app.py`
- [x] `docs/problem_statement.md`
- [x] `docs/technical_approach.md`

### 📁 Need to Create

#### Data Directories
- [ ] `data/` (main directory)
- [ ] `data/raw/` (for original data)
- [ ] `data/processed/` (for cleaned data)
- [ ] `data/synthetic/` (for generated data)
- [ ] `data/sample_data.csv` (sample dataset)

#### Notebooks
- [ ] `notebooks/01_data_exploration.ipynb`
- [ ] `notebooks/02_bias_analysis.ipynb`
- [ ] `notebooks/03_model_training.ipynb`
- [ ] `notebooks/04_synthetic_generation.ipynb`

#### Documentation
- [ ] `docs/presentation/` (directory)
- [ ] `docs/presentation/hackathon_pitch.md`

#### Demo Assets
- [ ] `demo/assets/` (directory)
- [ ] `demo/assets/images/` (directory)

#### Additional
- [ ] `generate_sample_data.py` (helper script)
- [ ] `setup_project_structure.sh` (setup script)

---

## 🚀 Quick Setup

### Option 1: Using the Setup Script

1. **Create the setup script:**
   ```bash
   # Copy the setup_project_structure.sh content to your project root
   chmod +x setup_project_structure.sh
   ```

2. **Run the setup script:**
   ```bash
   ./setup_project_structure.sh
   ```

3. **Generate sample data:**
   ```bash
   python generate_sample_data.py
   ```

### Option 2: Using Nix Flake

If you have Nix with flakes enabled:

```bash
# Enter development environment
nix develop

# The shellHook will automatically create directories
# Then generate sample data
python generate_sample_data.py
```

---

## 🔧 Manual Setup

If you prefer to set up manually:

### 1. Create Directory Structure

```bash
# Data directories
mkdir -p data/{raw,processed,synthetic}

# Documentation
mkdir -p docs/presentation

# Demo assets
mkdir -p demo/assets/images

# Models (for storing trained models)
mkdir -p models

# Add .gitkeep files to preserve empty directories
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/synthetic/.gitkeep
touch demo/assets/images/.gitkeep
```

### 2. Create Data Generation Script

Save the `generate_sample_data.py` file to your project root.

### 3. Create Notebooks

Save each notebook file to the `notebooks/` directory:
- `01_data_exploration.ipynb`
- `02_bias_analysis.ipynb`
- `03_model_training.ipynb`
- `04_synthetic_generation.ipynb`

### 4. Create Documentation

Save `hackathon_pitch.md` to `docs/presentation/`.

### 5. Generate Sample Data

```bash
python generate_sample_data.py
```

---

## ✓ Verification

After setup, verify your structure:

```bash
tree -L 3 -I '__pycache__|*.pyc|.git'
```

Expected output:
```
.
├── data/
│   ├── raw/
│   ├── processed/
│   ├── synthetic/
│   └── sample_data.csv
├── demo/
│   ├── app.py
│   ├── assets/
│   │   └── images/
│   └── requirements_demo.txt
├── docs/
│   ├── problem_statement.md
│   ├── technical_approach.md
│   └── presentation/
│       └── hackathon_pitch.md
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 01_sample_data_generation.py
│   ├── 02_bias_analysis.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_synthetic_generation.ipynb
├── src/
│   ├── __init__.py
│   ├── data_processing/
│   ├── synthetic_generator/
│   └── visualization/
├── tests/
│   ├── __init__.py
│   ├── test_bias_detection.py
│   └── test_synthetic_data.py
├── flake.nix
├── generate_sample_data.py
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

### Quick Verification Commands

```bash
# Check data directory exists
ls -la data/

# Check sample data was generated
ls -lh data/sample_data.csv

# Check notebooks exist
ls -la notebooks/*.ipynb

# Check documentation
ls -la docs/presentation/
```

---

## 🎯 Next Steps

Once setup is complete:

### 1. Install Dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using Nix:**
```bash
nix develop
# Dependencies are automatically available
```

### 2. Generate Sample Data

```bash
python generate_sample_data.py
```

This will create `data/sample_data.csv` with 1,000 sample Kenyan credit records.

### 3. Explore the Data

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

Or run all notebooks in sequence:
1. Data Exploration
2. Bias Analysis
3. Model Training
4. Synthetic Generation

### 4. Run the Demo

```bash
streamlit run demo/app.py
```

Or with Nix:
```bash
nix run .#demo
```

### 5. Run Tests

```bash
pytest tests/ -v
```

Or with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 🐛 Troubleshooting

### Issue: Missing Python packages

**Solution:**
```bash
pip install --upgrade -r requirements.txt

# For packages not in nixpkgs (when using Nix)
pip install --user aif360 sdv ctgan shap
```

### Issue: Jupyter kernel not found

**Solution:**
```bash
python -m ipykernel install --user --name fairlend --display-name "FairLend Kenya"
```

### Issue: Sample data generation fails

**Solution:**
```bash
# Ensure data directories exist
mkdir -p data/{raw,processed,synthetic}

# Run with verbose output
python generate_sample_data.py
```

### Issue: Import errors in notebooks

**Solution:**
```bash
# Set PYTHONPATH
export PYTHONPATH=$PWD/src:$PYTHONPATH

# Or add to notebook cell:
import sys
sys.path.append('../src')
```

### Issue: Streamlit demo won't start

**Solution:**
```bash
# Install demo dependencies
pip install -r demo/requirements_demo.txt

# Check if port 8501 is available
lsof -i :8501

# Run on different port
streamlit run demo/app.py --server.port 8502
```

---

## 📚 Additional Resources

### File Descriptions

| File/Directory | Purpose |
|----------------|---------|
| `data/sample_data.csv` | Sample Kenyan credit dataset with intentional biases |
| `01_data_exploration.ipynb` | Exploratory data analysis and visualization |
| `02_bias_analysis.ipynb` | Disparate impact and bias detection |
| `03_model_training.ipynb` | Train credit risk models |
| `04_synthetic_generation.ipynb` | Generate fair synthetic data |
| `hackathon_pitch.md` | Complete pitch deck for CBK hackathon |
| `generate_sample_data.py` | Script to create sample data |

### Important Notes

1. **Data Privacy**: Never commit real customer data. All data files are gitignored.

2. **Sample Data**: The generated sample data contains intentional biases for demonstration purposes.

3. **Production Use**: Increase epochs and batch size for production synthetic data generation.

4. **Model Artifacts**: Trained models are saved in `models/` directory (gitignored).

5. **Fairness Threshold**: The 0.8 disparate impact threshold is industry standard (80% rule).

---

## 🤝 Contributing

To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/`
5. Submit a pull request

---

## 📞 Support

For issues or questions:
- GitHub Issues: [Report a bug](https://github.com/timothynn/fairlend-kenya/issues)
- Email: timothynn08@gmail.com

---

## ✨ Quick Start Summary

```bash
# 1. Setup structure
./setup_project_structure.sh

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate data
python generate_sample_data.py

# 4. Run notebooks
jupyter notebook

# 5. Launch demo
streamlit run demo/app.py

# 6. Run tests
pytest tests/ -v
```

---

**Happy coding! 🇰🇪 Building a fairer financial future, one synthetic dataset at a time.**
