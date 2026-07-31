# Data Quality Report

## Project: FORESIGHT – Retail Inventory & Demand Forecasting

### Datasets Assessed

1. customer_master.csv
2. inventory_snapshot.csv
3. promotions.csv
4. sales_transactions.csv
5. sku_inventory_flags.csv
6. sku_master.csv
7. store_master.csv

---

## Data Quality Findings

| Dataset             | Missing Values                                     | Duplicates |
| ------------------- | -------------------------------------------------- | ---------- |
| Customer            | 0                                                  | 0          |
| Inventory           | 0                                                  | 0          |
| Promotions          | 0                                                  | 0          |
| Sales               | promo_id missing values identified                 | 12,897     |
| SKU Inventory Flags | window_start, window_end missing values identified | 0          |
| SKU Master          | 0                                                  | 0          |
| Store               | 0                                                  | 0          |

---

## Cleaning Actions Performed

* Converted all date columns to datetime format.
* Replaced missing `promo_id` values with `No Promotion`.
* Replaced missing `window_start` and `window_end` values with `Not Available`.
* Verified dataset structures and data types.
* Verified duplicate records.

---

## Cleaned Files Generated

* customer_master_clean.csv
* inventory_snapshot_clean.csv
* promotions_clean.csv
* sales_transactions_clean.csv
* sku_inventory_flags_clean.csv
* sku_master_clean.csv
* store_master_clean.csv

---

## Conclusion

All datasets were successfully inspected, cleaned, and saved in the `data/processed/` directory. The cleaned datasets are now ready for exploratory data analysis and subsequent forecasting and risk-scoring phases.
