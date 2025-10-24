{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# FairLend Kenya - Data Exploration\n",
    "## Exploring Kenyan Credit Data for Bias Detection\n",
    "\n",
    "This notebook explores the sample Kenyan credit dataset and identifies potential biases."
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
    "# Set plotting style\n",
    "plt.style.use('seaborn-v0_8-darkgrid')\n",
    "sns.set_palette('husl')\n",
    "\n",
    "%matplotlib inline\n",
    "%load_ext autoreload\n",
    "%autoreload 2"
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
    "# Load sample data\n",
    "df = pd.read_csv('../data/sample_data.csv')\n",
    "\n",
    "print(f\"Dataset shape: {df.shape}\")\n",
    "print(f\"\\nColumns: {list(df.columns)}\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Data Overview"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Basic statistics\n",
    "print(\"Dataset Info:\")\n",
    "print(df.info())\n",
    "print(\"\\nNumerical Statistics:\")\n",
    "df.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Check for missing values\n",
    "missing_values = df.isnull().sum()\n",
    "print(\"Missing values per column:\")\n",
    "print(missing_values[missing_values > 0])\n",
    "\n",
    "if missing_values.sum() == 0:\n",
    "    print(\"✅ No missing values found!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Target Variable Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Overall approval rate\n",
    "approval_rate = df['loan_approved'].mean()\n",
    "print(f\"Overall Loan Approval Rate: {approval_rate:.2%}\")\n",
    "\n",
    "# Visualize\n",
    "fig, ax = plt.subplots(1, 2, figsize=(12, 4))\n",
    "\n",
    "# Count plot\n",
    "df['loan_approved'].value_counts().plot(kind='bar', ax=ax[0], color=['red', 'green'])\n",
    "ax[0].set_title('Loan Approval Distribution')\n",
    "ax[0].set_xlabel('Approved (1=Yes, 0=No)')\n",
    "ax[0].set_ylabel('Count')\n",
    "ax[0].set_xticklabels(['Rejected', 'Approved'], rotation=0)\n",
    "\n",
    "# Pie chart\n",
    "df['loan_approved'].value_counts().plot(kind='pie', ax=ax[1], autopct='%1.1f%%', \n",
    "                                         labels=['Rejected', 'Approved'],\n",
    "                                         colors=['red', 'green'])\n",
    "ax[1].set_title('Loan Approval Rate')\n",
    "ax[1].set_ylabel('')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Demographic Distribution"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gender distribution\n",
    "fig, axes = plt.subplots(2, 2, figsize=(15, 10))\n",
    "\n",
    "# Gender\n",
    "df['gender'].value_counts().plot(kind='bar', ax=axes[0,0], color=['skyblue', 'pink'])\n",
    "axes[0,0].set_title('Gender Distribution')\n",
    "axes[0,0].set_ylabel('Count')\n",
    "axes[0,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=0)\n",
    "\n",
    "# Location\n",
    "df['location'].value_counts().plot(kind='bar', ax=axes[0,1])\n",
    "axes[0,1].set_title('Location Distribution')\n",
    "axes[0,1].set_ylabel('Count')\n",
    "axes[0,1].tick_params(axis='x', rotation=45)\n",
    "\n",
    "# Business Type\n",
    "df['business_type'].value_counts().plot(kind='bar', ax=axes[1,0])\n",
    "axes[1,0].set_title('Business Type Distribution')\n",
    "axes[1,0].set_ylabel('Count')\n",
    "axes[1,0].tick_params(axis='x', rotation=45)\n",
    "\n",
    "# Education Level\n",
    "df['education_level'].value_counts().plot(kind='bar', ax=axes[1,1])\n",
    "axes[1,1].set_title('Education Level Distribution')\n",
    "axes[1,1].set_ylabel('Count')\n",
    "axes[1,1].tick_params(axis='x', rotation=45)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Kenyan-Specific Features"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# M-Pesa and SACCO analysis\n",
    "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
    "\n",
    "# M-Pesa transaction count\n",
    "axes[0].hist(df['mpesa_transaction_count'], bins=30, edgecolor='black')\n",
    "axes[0].set_title('M-Pesa Transaction Count Distribution')\n",
    "axes[0].set_xlabel('Monthly Transactions')\n",
    "axes[0].set_ylabel('Frequency')\n",
    "\n",
    "# M-Pesa average transaction\n",
    "axes[1].hist(df['mpesa_avg_transaction'], bins=30, edgecolor='black', color='orange')\n",
    "axes[1].set_title('M-Pesa Average Transaction Amount')\n",
    "axes[1].set_xlabel('Amount (KES)')\n",
    "axes[1].set_ylabel('Frequency')\n",
    "\n",
    "# SACCO membership\n",
    "sacco_counts = df['sacco_member'].value_counts()\n",
    "axes[2].bar(['Non-Member', 'Member'], sacco_counts.values, color=['coral', 'lightgreen'])\n",
    "axes[2].set_title('SACCO Membership')\n",
    "axes[2].set_ylabel('Count')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "print(f\"SACCO Membership Rate: {df['sacco_member'].mean():.2%}\")\n",
    "print(f\"Average M-Pesa transactions/month: {df['mpesa_transaction_count'].mean():.1f}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Approval Rate Analysis by Protected Attributes\n",
    "### This is where we start seeing potential biases!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Approval rates by protected attributes\n",
    "fig, axes = plt.subplots(2, 2, figsize=(15, 10))\n",
    "\n",
    "# By Gender\n",
    "gender_approval = df.groupby('gender')['loan_approved'].agg(['mean', 'count'])\n",
    "gender_approval['mean'].plot(kind='bar', ax=axes[0,0], color=['skyblue', 'pink'])\n",
    "axes[0,0].set_title('Loan Approval Rate by Gender')\n",
    "axes[0,0].set_ylabel('Approval Rate')\n",
    "axes[0,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=0)\n",
    "axes[0,0].axhline(y=approval_rate, color='red', linestyle='--', label='Overall Rate')\n",
    "axes[0,0].legend()\n",
    "for i, (idx, row) in enumerate(gender_approval.iterrows()):\n",
    "    axes[0,0].text(i, row['mean'] + 0.01, f\"{row['mean']:.2%}\\n(n={int(row['count'])})\", \n",
    "                   ha='center', va='bottom')\n",
    "\n",
    "# By Location\n",
    "location_approval = df.groupby('location')['loan_approved'].agg(['mean', 'count']).sort_values('mean', ascending=False)\n",
    "location_approval['mean'].plot(kind='bar', ax=axes[0,1])\n",
    "axes[0,1].set_title('Loan Approval Rate by Location')\n",
    "axes[0,1].set_ylabel('Approval Rate')\n",
    "axes[0,1].tick_params(axis='x', rotation=45)\n",
    "axes[0,1].axhline(y=approval_rate, color='red', linestyle='--', label='Overall Rate')\n",
    "axes[0,1].legend()\n",
    "\n",
    "# By Business Type\n",
    "business_approval = df.groupby('business_type')['loan_approved'].agg(['mean', 'count']).sort_values('mean', ascending=False)\n",
    "business_approval['mean'].plot(kind='bar', ax=axes[1,0])\n",
    "axes[1,0].set_title('Loan Approval Rate by Business Type')\n",
    "axes[1,0].set_ylabel('Approval Rate')\n",
    "axes[1,0].tick_params(axis='x', rotation=45)\n",
    "axes[1,0].axhline(y=approval_rate, color='red', linestyle='--', label='Overall Rate')\n",
    "axes[1,0].legend()\n",
    "\n",
    "# By Education\n",
    "education_approval = df.groupby('education_level')['loan_approved'].agg(['mean', 'count']).sort_values('mean', ascending=False)\n",
    "education_approval['mean'].plot(kind='bar', ax=axes[1,1])\n",
    "axes[1,1].set_title('Loan Approval Rate by Education')\n",
    "axes[1,1].set_ylabel('Approval Rate')\n",
    "axes[1,1].tick_params(axis='x', rotation=45)\n",
    "axes[1,1].axhline(y=approval_rate, color='red', linestyle='--', label='Overall Rate')\n",
    "axes[1,1].legend()\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Key Findings Summary"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"=\"*60)\n",
    "print(\"KEY FINDINGS: Potential Biases Detected\")\n",
    "print(\"=\"*60)\n",
    "\n",
    "print(\"\\n1. GENDER BIAS:\")\n",
    "for gender, rate in gender_approval['mean'].items():\n",
    "    print(f\"   {gender}: {rate:.2%}\")\n",
    "print(f\"   Gap: {abs(gender_approval['mean'].iloc[0] - gender_approval['mean'].iloc[1]):.2%}\")\n",
    "\n",
    "print(\"\\n2. LOCATION BIAS:\")\n",
    "urban_locs = ['Nairobi', 'Mombasa', 'Thika']\n",
    "urban_rate = df[df['location'].isin(urban_locs)]['loan_approved'].mean()\n",
    "rural_rate = df[df['location'] == 'Rural']['loan_approved'].mean()\n",
    "print(f\"   Urban areas: {urban_rate:.2%}\")\n",
    "print(f\"   Rural areas: {rural_rate:.2%}\")\n",
    "print(f\"   Gap: {abs(urban_rate - rural_rate):.2%}\")\n",
    "\n",
    "print(\"\\n3. BUSINESS TYPE BIAS:\")\n",
    "formal_rate = df[df['business_type'] != 'Informal']['loan_approved'].mean()\n",
    "informal_rate = df[df['business_type'] == 'Informal']['loan_approved'].mean()\n",
    "print(f\"   Formal sector: {formal_rate:.2%}\")\n",
    "print(f\"   Informal sector: {informal_rate:.2%}\")\n",
    "print(f\"   Gap: {abs(formal_rate - informal_rate):.2%}\")\n",
    "\n",
    "print(\"\\n4. M-PESA ACTIVITY:\")\n",
    "high_mpesa = df[df['mpesa_transaction_count'] > 30]['loan_approved'].mean()\n",
    "low_mpesa = df[df['mpesa_transaction_count'] <= 30]['loan_approved'].mean()\n",
    "print(f\"   High M-Pesa activity (>30 trans/month): {high_mpesa:.2%}\")\n",
    "print(f\"   Low M-Pesa activity (≤30 trans/month): {low_mpesa:.2%}\")\n",
    "print(f\"   Gap: {abs(high_mpesa - low_mpesa):.2%}\")\n",
    "\n",
    "print(\"\\n\" + \"=\"*60)\n",
    "print(\"🎯 These biases demonstrate the need for FairLend Kenya!\")\n",
    "print(\"=\"*60)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Next Steps\n",
    "\n",
    "1. Proceed to `02_bias_analysis.ipynb` for detailed disparate impact analysis\n",
    "2. Use these insights to configure synthetic data generation\n",
    "3. Validate that synthetic data reduces these biases"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
