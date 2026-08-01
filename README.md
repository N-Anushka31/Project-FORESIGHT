# Project-FORESIGHT

## End-to-End Demand Forecasting and Inventory Intelligence System

---

## Project Overview

Project-FORESIGHT is an end-to-end data analytics and machine learning solution developed to forecast product demand, monitor inventory performance, identify stock-related risks, and support inventory planning through interactive business dashboards.

The project integrates data preprocessing, exploratory data analysis, feature engineering, demand forecasting, inventory risk scoring, dashboard development, and deployment into a single reproducible workflow.

The objective is to transform historical sales and inventory data into actionable business insights that support efficient inventory management and strategic decision-making.

---

## Business Problem

Retail organizations often struggle to maintain optimal inventory levels because customer demand changes over time. Inaccurate demand estimation can lead to:

- Stockouts and lost sales
- Excess inventory and higher storage costs
- Poor inventory utilization
- Reduced customer satisfaction
- Inefficient business planning

This project addresses these challenges by building a data-driven forecasting and inventory intelligence system that enables proactive inventory management.

---

## Project Objectives

The primary objectives of this project are to:

- Forecast future product demand using historical sales data.
- Analyze sales trends and seasonality.
- Evaluate inventory performance.
- Identify stockout and overstock risks.
- Generate inventory intelligence through business rules.
- Develop interactive dashboards for business users.
- Support executive decision-making with actionable insights.

---

## Dataset

The datasets are **not included** in this repository because GitHub has a file size limit of 100 MB, and the retail transaction dataset exceeds this limit.

Download the dataset from Kaggle:

**Synthetic Retail Dataset – 10 Million Transactions**

https://www.kaggle.com/datasets/mrayyanshehzad/synthetic-retail-dataset-10-million-transactions

After downloading and extracting the ZIP file, place the following CSV files inside the `data/raw/` folder:

```text
customer_master.csv
inventory_snapshot.csv
promotions.csv
sales_transactions.csv
sku_inventory_flags.csv
sku_master.csv
store_master.csv
```

The cleaned datasets will be generated automatically and saved in the `data/processed/` folder after running the data cleaning notebook.

## Project Workflow

Business Understanding

↓

Data Collection

↓

Data Cleaning

↓

Exploratory Data Analysis

↓

Feature Engineering

↓

Demand Forecasting

↓

Inventory Risk Scoring

↓

Dashboard Development

↓

Deployment

↓

Executive Summary

---

## Expected Deliverables

The final project will include:

- Data preprocessing pipeline
- Data quality assessment
- Exploratory Data Analysis (EDA)
- Feature engineering pipeline
- Demand forecasting model
- Inventory risk scoring engine
- Interactive Streamlit dashboard
- Business reports
- Executive presentation
- Deployable solution

---

## Technology Stack

### Programming Language

- Python

### Data Processing

- Pandas
- NumPy

### Data Visualization

- Matplotlib
- Seaborn
- Plotly

### Machine Learning

- Scikit-learn
- XGBoost
- LightGBM
- Prophet

### Dashboard

- Streamlit
- Power BI

### Deployment

- FastAPI

### Version Control

- Git
- GitHub

---

```text
Project-FORESIGHT/
│
├── app/
├── data/
│   ├── raw/                  # Downloaded Kaggle datasets
│   └── processed/            # Cleaned datasets generated locally
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_forecasting.ipynb
│   └── 05_risk_scoring.ipynb
├── reports/
│   └── Data_Quality_Report.md
├── src/
├── presentation/
├── README.md
├── requirements.txt
└── .gitignore
```

**Current Phase:** Phase 6– Inventory risk scoring

### Completed

- Repository initialization
- Project structure
- Business understanding
- Project documentation
- Data collection
- Data cleaning
- Data quality assessment
-Exploratory Data Analysis
- Feature engineering
- Demand forecasting

### Upcoming

- Inventory risk scoring
- Dashboard development
- Deployment
- Executive presentation

## Expected Outcomes

The completed solution will:

- Improve demand forecasting accuracy.
- Support efficient inventory planning.
- Reduce stockout and overstock risks.
- Enable data-driven inventory decisions.
- Provide interactive dashboards for business users.
- Deliver executive-level business insights.

---

## Future Enhancements

Future improvements may include:

- Real-time demand forecasting
- Automated data pipelines
- Cloud deployment
- API integration
- Advanced forecasting models
- Continuous model monitoring

---
## How to Run

1. Clone the repository.

```bash
git clone <repository-url>
```

2. Open the project in Visual Studio Code.

3. Create and activate a Python virtual environment.

4. Install the required packages.

```bash
pip install -r requirements.txt
```

5. Download the dataset from Kaggle.

6. Extract the ZIP file and copy all CSV files into the `data/raw/` folder.

7. Run the notebooks in the following order:

- 01_data_cleaning.ipynb
- 02_eda.ipynb
- 03_feature_engineering.ipynb
- 04_forecasting.ipynb
- 05_risk_scoring.ipynb

8. Run the Streamlit dashboard after development is complete.

```bash
streamlit run app/app.py
```

## License

This project is licensed under the MIT License.
