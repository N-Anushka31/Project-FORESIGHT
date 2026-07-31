# Exploratory Data Analysis (EDA) Report

## Project: Project-FORESIGHT
### End-to-End Demand Forecasting and Inventory Intelligence System

---

# 1. Introduction

The objective of this Exploratory Data Analysis (EDA) is to understand historical sales, customer behavior, inventory levels, promotional activities, and store performance before developing demand forecasting and inventory intelligence models.

EDA helps identify trends, seasonality, anomalies, business opportunities, and potential data issues that influence future forecasting performance.

---

# 2. Dataset Overview

The project uses the following cleaned datasets:

| Dataset | Records | Description |
|---------|---------|-------------|
| Customer Master | 10,000 | Customer demographic information |
| Inventory Snapshot | 26,408 | Current inventory levels across stores |
| Promotions | 100 | Promotional campaign information |
| Sales Transactions | 9,945,511 | Historical sales transactions |
| SKU Inventory Flags | 600 | Inventory risk indicators |
| SKU Master | 5,000 | Product master information |
| Store Master | 30 | Store information |

---

# 3. Data Quality Summary

Data quality was assessed before performing analysis.

### Findings

- Duplicate records were removed during Phase 2.
- Missing values were handled appropriately.
- Date columns were converted into datetime format.
- Numeric columns were validated.
- Data types were standardized across datasets.

The cleaned datasets were used for all analyses presented in this report.

---

# 4. Daily Sales Trend Analysis

Daily sales were aggregated to observe changes in revenue over time.

### Observation

- Daily sales remained relatively stable throughout the available period.
- Minor fluctuations indicate regular customer purchasing behavior.
- No unexpected spikes or abnormal drops were observed.

---

# 5. Monthly Sales Trend Analysis

Monthly sales aggregation was performed to identify long-term business trends.

### Observation

- Monthly revenue shows gradual variation over time.
- Seasonal fluctuations are visible.
- Monthly aggregation provides a clearer understanding of business growth than daily sales.

---

# 6. Top 10 Selling Products

Products were ranked based on total sales value.

### Observation

- A small number of SKUs contribute a significant portion of total revenue.
- High-performing products should receive higher inventory priority.
- These products are potential candidates for demand forecasting optimization.

---

# 7. Top 10 Stores by Sales

Store performance was analyzed using total sales.

### Observation

- Some stores consistently outperform others.
- Store demand varies by location.
- Inventory allocation should consider store-level demand.

---

# 8. Sales by Channel

Sales were analyzed across different sales channels.

### Observation

- Customer purchasing behavior differs across channels.
- Some channels generate significantly higher revenue.
- Channel performance can influence inventory planning.

---

# 9. Sales by Product Category

Revenue contribution was analyzed for each product category.

### Observation

- Product categories contribute unevenly to total sales.
- High-performing categories represent major revenue drivers.
- Low-performing categories may require promotional strategies.

---

# 10. Customer Loyalty Segment Analysis

Sales were analyzed based on customer loyalty segments.

### Observation

- Premium loyalty customers contribute significantly to sales.
- Customer segmentation provides opportunities for personalized marketing.
- Loyalty programs appear to positively influence purchasing behavior.

---

# 11. Inventory Analysis

Inventory levels across products were examined.

### Observation

- Inventory quantities vary considerably across SKUs.
- Some products maintain higher safety stock levels.
- Inventory policies should align with product demand.

---

# 12. Promotion Analysis

Promotional campaigns were analyzed using discount percentages.

### Observation

- Promotions use varying discount levels.
- Different promotion types target different customer segments.
- Promotional strategies influence sales performance.

---

# 13. SKU Inventory Flag Analysis

Inventory flag records were analyzed.

### Observation

- Several SKUs were flagged for stockout risk.
- These products require closer monitoring.
- Inventory intelligence can improve replenishment planning.

---

# 14. Dead Stock Analysis

Products with zero recorded sales during the analysis period were identified as potential dead stock.

### Observation

- No dead stock products were identified in the available dataset.
- All products recorded at least one sale during the observed period.
- This indicates healthy inventory movement across the product catalog.

---

# 15. Business Insights

The exploratory analysis produced the following key business insights:

1. Sales remain relatively stable over time with normal business fluctuations.

2. A limited number of products generate a significant proportion of total revenue.

3. Store performance differs considerably, suggesting location-specific demand patterns.

4. Customer loyalty segments contribute differently to revenue, indicating opportunities for targeted marketing.

5. Promotional campaigns play an important role in influencing purchasing behavior.

6. Several SKUs have been flagged for stockout risk and should receive priority during inventory planning.

7. No dead stock products were identified, indicating effective inventory turnover.

---

# 16. Conclusion

The exploratory data analysis successfully identified important sales trends, customer behavior patterns, inventory characteristics, promotional insights, and business opportunities.

These findings provide a strong foundation for the next stage of the project: Feature Engineering, where additional predictive features will be created to improve demand forecasting model performance.

---

**Next Phase:** Feature Engineering