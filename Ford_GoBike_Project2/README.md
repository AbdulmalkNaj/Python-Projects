# 🚲 Ford GoBike System Data Exploration & Explanatory Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458.svg)
![Seaborn](https://img.shields.io/badge/Seaborn-Data%20Visualization-ff69b4.svg)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen.svg)

## 📌 Project Overview
This two-part project analyzes individual ride data from the **Ford GoBike** bike-sharing system covering the greater San Francisco Bay area in February 2019. 

The project is divided into two main phases:
1. **Part I - Exploratory Data Analysis (EDA):** A deep dive into the dataset using univariate, bivariate, and multivariate visualizations to uncover underlying patterns and relationships between trip durations, temporal usage, and user demographics.
2. **Part II - Explanatory Data Analysis:** A polished presentation of the most significant insights discovered during exploration, crafted to communicate clear, actionable takeaways to stakeholders.

---

## 📊 The Dataset
The original dataset contained 183,412 trips with 16 features. After rigorous data wrangling, the final cleaned dataset consists of **174,760 observations** and 20 features.

**Key Data Cleaning & Engineering Steps:**
* **Null Handling:** Dropped rows with missing demographics (birth year, gender) and station names.
* **Outlier Removal:** Filtered out unrealistic age outliers (members > 80 years old).
* **Feature Engineering:** 
  * Calculated `duration_min` from `duration_sec`.
  * Extracted `member_age` from `member_birth_year`.
  * Extracted temporal features: `start_hour` and `start_day` (converted to ordered categorical variables).

---

## 🔍 Key Findings & Executive Summary

Through the exploratory and explanatory phases, three major behavioral insights were uncovered:

### 1. Trip Duration Profile
* The vast majority of bike trips are brief, single-purpose urban commutes.
* When plotted on a logarithmic scale, trip durations form a unimodal distribution that peaks sharply between **8 and 12 minutes**.

### 2. Weekly & Hourly Demand Spikes
* **Weekdays (Mon-Fri):** Usage follows a strict bimodal "rush-hour" pattern, with massive demand spikes at **8:00 AM** and **5:00 PM**, correlating heavily with traditional working hours.
* **Weekends (Sat-Sun):** The pattern shifts entirely. Commute spikes disappear, replaced by a smooth, continuous usage bell curve during midday hours (**11:00 AM to 4:00 PM**), reflecting leisure and recreational riding.

### 3. User Demographic Behaviors
* **Subscribers vs. Customers:** **Subscribers** account for ~90% of trips, taking highly regular, short-duration commutes. Casual **Customers**, while fewer in number, consistently log noticeably longer average trip durations (~13 mins vs ~8 mins).
* **Gender & Age Trends:** **Female** and **Other** gender riders consistently take slightly longer trips on average than Male riders across all days of the week. Furthermore, older riders limit their trips to shorter durations, whereas longer trips (>50 mins) are exclusively dominated by younger demographics (20-40 years old).

---

## 🛠️ Technologies Used
* **Python** - Core programming language.
* **Pandas & NumPy** - Data wrangling, cleaning, and feature engineering.
* **Matplotlib & Seaborn** - Creating high-quality exploratory and explanatory data visualizations.
* **Jupyter Notebook** - Interactive development and analysis environment.

---

## 📁 Repository Structure

```text
├── 201902-fordgobike-tripdata.csv       # Raw dataset (Not included in repo due to size limits)
├── Part_I_exploration_template.ipynb    # Exploratory Data Analysis (EDA) notebook
├── Part_II_slide_deck_template.ipynb    # Explanatory Data Analysis & Slides notebook
├── README.md                            # Project documentation
