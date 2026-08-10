# 📊 World Happiness & Economic Indicators - Data Wrangling Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458.svg)
![Status](https://img.shields.io/badge/Udacity-Approved-brightgreen.svg)

## 📌 Project Overview
This project presents an end-to-end data wrangling, cleaning, and exploratory data analysis (EDA) pipeline designed to investigate the relationship between **objective macroeconomic output** (Gross Domestic Product per capita) and **subjective national happiness** (Life Evaluation Scores) across global nations. 

By merging two disparate, real-world datasets gathered using distinct extraction protocols, the pipeline structures, cleans, and standardizes over **1,600 cross-country temporal observations** to evaluate the key socio-economic drivers of global well-being.

---

## 🛠️ Data Sources & Gathering Methods

The project ingests two distinct datasets using different data acquisition methods:

1. **Dataset 1: World Happiness Report (WHR)**
   * **Acquisition Method:** Downloaded Manually (`Excel/CSV`).
   * **Source File:** `data/raw/raw_happiness_data.csv`
   * **Metrics:** Subjective Life Evaluation (3-year average happiness score), Social Support, Healthy Life Expectancy, Freedom, Generosity, and Corruption Perceptions.
2. **Dataset 2: World Bank Global Economic Indicators**
   * **Acquisition Method:** Fetched Programmatically via Python `requests` & HTTP APIs (`CSV`).
   * **Source File:** `data/raw/raw_worldbank_gdp.csv`
   * **Metrics:** National Gross Domestic Product (`GDP Value` in USD), ISO Country Codes, and Temporal Indicators (`Year`).

---

## 🧹 Data Assessment & Cleaning Highlights

Following strict **Tidy Data** principles (Hadley Wickham) and Data Quality pillars, 4 core data issues were systematically identified, documented, and cleaned:

### 1. Data Quality Issues
* **Completeness (Missing Values):** Imputed missing values in numerical indicator columns using median imputation to preserve sample size without introducing outlier skewness.
* **Validity & Consistency (Column Naming & Types):** Standardized column headers to pythonic `snake_case`, eliminated spaces/prefixes, and aligned variable types across both data structures.

### 2. Data Tidiness Issues
* **Structural Key Alignment:** Resolved mismatched geographic keys (`Country name` vs `Country Name`) and eliminated redundant ISO country code identifiers.
* **Observational Unit Consolidation:** Merged fragmented tables on composite keys (`['country', 'year']`) to consolidate subjective well-being and objective economic metrics into a single unified observational unit.

*All cleaning steps were strictly validated using programmatic assertions (`assert`).*

---

## 📁 Repository Directory Structure

```text
├── data/
│   ├── raw/                               # Raw immutable checkpoints
│   │   ├── raw_happiness_data.csv
│   │   └── raw_worldbank_gdp.csv
│   └── cleaned/                           # Cleaned & merged dataset
│       └── cleaned_world_happiness_gdp_combined.csv
├── Real_World_Data_Wrangling.ipynb        # Main Jupyter Notebook
├── README.md                              # Project Documentation
└── requirements.txt                       # Dependencies
