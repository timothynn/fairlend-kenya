{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# FairLend Kenya - Bias Analysis\n",
    "## Quantitative Bias Detection Using Disparate Impact\n",
    "\n",
    "This notebook performs comprehensive bias analysis using fairness metrics."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import sys\n",
    "sys.path.append('../src')\n",
    "\n",
    "from data_processing.bias_detector import BiasDetector\n",
    "\n",
    "plt.style.use('seaborn-v0_8-darkgrid')\n",
    "sns.set_palette('husl')\n",
    "\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Load Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('../data/sample_data.csv')\n",
    "print(f\"Loaded {len(df)} records\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Initialize Bias Detector"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "detector = BiasDetector()\n",
    "print(f\"Protected attributes: {detector.protected_attributes}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Run Comprehensive Bias Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save data temporarily for analysis\n",
    "temp_path = '../data/temp_analysis.csv'\n",
    "df.to_csv(temp_path, index=False)\n",
    "\n",
    "# Run bias analysis\n",
    "bias_report = detector.analyze_dataset(temp_path)\n",
    "\n",
    "print(\"\\n\" + \"=\"*60)\n",
    "print(\"BIAS ANALYSIS REPORT\")\n",
    "print(\"=\"*60)\n",
    "print(f\"\\nDataset shape: {bias_report['dataset_shape']}\")\n",
    "print(f\"Overall approval rate: {bias_report['approval_rate']:.2%}\")"
