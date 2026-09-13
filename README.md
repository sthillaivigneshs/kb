# 🧹 Data Cleaning & Reporting Automation

Automate data cleaning and reporting workflows using Python.

## 🎯 Project Overview

This project automates the entire data cleaning pipeline — from raw messy data to cleaned dataset with automated Excel reports and visual summaries.

## 🔍 Key Features

- ✅ **Automated Cleaning**: Missing values, duplicates, inconsistent data
- ✅ **Data Profiling**: Detect issues before cleaning
- ✅ **Standardization**: Country names, emails, formats
- ✅ **Validation**: Invalid ages, negative values, zero quantities
- ✅ **Automated Reports**: Excel report with 5 sheets
- ✅ **Visual Summaries**: 9-panel dashboard

## 🛠️ Technologies Used

- Python 3.x
- pandas, numpy
- matplotlib, seaborn
- openpyxl (Excel reports)

## 📁 Project Structure
data_cleaning_automation/
├── data/
│ ├── raw/messy_data.csv
│ └── cleaned/cleaned_data.csv
├── scripts/cleaning_pipeline.py
├── reports/
│ ├── cleaning_report.xlsx
│ └── summary_charts.png
├── requirements.txt
├── .gitignore
└── README.md

## 🚀 How to Run

```bash
git clone https://github.com/sthillaivigneshs/data-cleaning-automation.git
cd data_cleaning_automation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd scripts
python cleaning_pipeline.py
📊 Cleaning Pipeline Steps
Create/Load messy data

Profile data (find issues)

Remove duplicates

Handle missing values (median/mode)

Standardize text (Country, Email)

Fix invalid values

Add derived columns

Generate visualizations

Export Excel report

📈 Results
Metric	Before	After
Rows	205	200
Missing Values	73	0
Duplicates	5	0
Columns	9	13
11 cleaning actions performed automatically

📊 Excel Report Sheets
Cleaning_Log: All actions taken

Before_vs_After: Comparison metrics

Cleaned_Data: First 100 rows

Summary_Stats: Descriptive statistics

Country_Analysis: Grouped metrics