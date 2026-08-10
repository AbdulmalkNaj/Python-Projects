# 🎬 TMDb Movie Data Analysis - Industry Success Factors

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange.svg)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen.svg)

## 📌 Project Overview
This data analysis project investigates the **The Movie Database (TMDb)** dataset, containing information on thousands of movies spanning several decades. The objective is to analyze key financial and reception metrics—such as adjusted budget, adjusted revenue, user ratings, and genres—to uncover the key drivers behind financial success and popularity in the film industry.

---

## ❓ Research Questions

1. **Budget vs. Revenue:** Does a higher adjusted budget (`budget_adj`) correlate with higher adjusted revenue (`revenue_adj`)?
2. **Ratings vs. Financial Success:** How does the user rating (`vote_average`) relate to a movie's financial success (profitability)?
3. **Genre Trends:** Which movie genres (`genres`) are the most profitable on average over the decades?

---

## 🧹 Data Wrangling & Cleaning Summary

To ensure data integrity and avoid analytical skewness, the following cleaning steps were executed:
* **Feature Dropping:** Removed non-essential features with high missing values (`homepage`, `tagline`, `keywords`, `production_companies`).
* **Deduplication:** Identified and removed duplicate rows across the dataset.
* **Financial Filtering:** Filtered out records where `budget_adj` or `revenue_adj` equaled `$0` (retaining 3,854 valid financial entries).
* **Missing Value Handling:** Dropped records with missing values in critical categorical attributes such as `genres`.

---

## 📊 Key Insights & Findings

* **💰 Budget vs. Revenue:** A clear positive correlation exists between adjusted budget and adjusted revenue. While higher budgets generally yield higher revenues, exceptions exist—moderate-budget films occasionally become massive blockbusters, whereas certain high-budget films fail to recoup costs.
* **⭐ Ratings vs. Profitability:** Highly profitable movies overwhelmingly cluster within user ratings between **6.0 and 8.0**. Films rated below 5.0 rarely achieve financial success, proving that acceptable audience reception (≥ 6.0) is a crucial baseline for high profitability.
* **🎭 Genre Performance:** **Animation** and **Adventure** emerge as the most profitable genres on average, followed by **Family** and **Fantasy**. Conversely, **Documentaries** and **Foreign** films sit at the bottom of average profit metrics.

---

## ⚠️ Project Limitations

* **Data Selection Bias:** Dropping rows with missing or `$0` financial metrics reduced the dataset size, which may introduce selection bias toward commercially documented releases.
* **Macroeconomic Factors:** While inflation-adjusted metrics (`_adj`) were utilized, standard inflation algorithms do not capture changing global market dynamics, streaming shifts, or international distribution nuances over time.
* **Rating Ecosystem Bias:** User ratings are derived from the TMDB community ecosystem, which may not fully reflect global general audience opinions.

---

## 📁 Project Structure

```text
├── tmdb-movies.csv             # Raw TMDb Dataset
├── My_Movie_Analysis.ipynb      # Main Jupyter Notebook Analysis
├── My_Movie_Analysis.html       # Exported HTML Report
└── README.md                    # Project Documentation
