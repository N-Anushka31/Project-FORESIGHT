# Risk Scoring Report

## 1. Objective

The objective of the risk-scoring analysis is to identify SKU-store combinations that may require inventory intervention. The analysis combines inventory levels, historical demand, inventory coverage, reorder points, and safety stock levels to classify stockout and overstock risks.

The resulting risk scores and recommended actions provide a transparent decision-support framework for inventory planning.

---

## 2. Data Used

The analysis uses the following processed datasets:

- Inventory snapshot data
- Historical sales and demand data
- Forecasting/model dataset

The inventory dataset contains SKU-store inventory information including:

- `store_id`
- `sku_id`
- `stock_on_hand`
- `reorder_point`
- `safety_stock`
- `last_restock_date`

Historical demand was aggregated at the `store_id` and `sku_id` level before being combined with the inventory data.

---

## 3. Demand and Inventory Integration

Historical transaction data was aggregated at the store-SKU level to calculate:

- Total quantity sold
- Average weekly demand
- Total sales
- Average unit price
- Cost price

The resulting demand summary was merged with the inventory snapshot using:

- `store_id`
- `sku_id`

This produced a final risk dataset containing 26,408 SKU-store combinations with no missing values in the analytical fields.

---

## 4. Inventory Coverage

Inventory coverage was calculated as:

**Inventory Coverage (weeks) = Stock on Hand / Average Weekly Demand**

The resulting coverage distribution was:

| Metric | Value |
|---|---:|
| Number of SKU-store combinations | 26,408 |
| Mean coverage | 90.04 weeks |
| Median coverage | 74.61 weeks |
| 25th percentile | 21.36 weeks |
| 75th percentile | 141.91 weeks |
| Minimum | 0 weeks |
| Maximum | 535 weeks |

The high coverage values indicate that a substantial number of SKU-store combinations hold inventory well above recent average demand.

---

## 5. Stockout Risk Classification

Stockout risk was classified using stock on hand relative to safety stock and reorder point.

### Classification rules

- **High:** Stock on hand <= Safety stock
- **Medium:** Stock on hand > Safety stock and <= Reorder point
- **Low:** Stock on hand > Reorder point

### Results

| Stockout Risk | Count |
|---|---:|
| High | 5,270 |
| Medium | 1,892 |
| Low | 19,246 |
| **Total** | **26,408** |

A total of 7,162 SKU-store combinations were classified as Medium or High stockout risk and therefore require further replenishment review.

---

## 6. Overstock Risk Classification

Overstock risk was assessed using inventory coverage.

### Classification rules

- **High:** Inventory coverage >= 26 weeks
- **Medium:** Inventory coverage >= 13 and < 26 weeks
- **Low:** Inventory coverage < 13 weeks

### Results

| Overstock Risk | Count |
|---|---:|
| High | 19,274 |
| Medium | 1,452 |
| Low | 5,682 |
| **Total** | **26,408** |

The results indicate that a large number of SKU-store combinations have high inventory coverage relative to historical demand.

These results should be interpreted as potential overstock exposure rather than automatically treating all high-coverage items as dead stock.

---

## 7. Combined Risk Framework

Stockout and overstock indicators were combined into a single risk framework.

Risk scores were assigned as follows:

| Condition | Risk Score |
|---|---:|
| High stockout risk | 3 |
| High overstock risk | 3 |
| Medium stockout risk | 2 |
| Medium overstock risk | 2 |
| No elevated risk | 1 |

The resulting score was converted into:

- **High Risk:** Score 3
- **Medium Risk:** Score 2
- **Low Risk:** Score 1

### Overall Risk Distribution

| Risk Level | Count |
|---|---:|
| High | 24,543 |
| Medium | 1,841 |
| Low | 24 |
| **Total** | **26,408** |

The high number of High Risk combinations reflects the fact that either a high stockout condition or high overstock condition results in a High Risk classification.

---

## 8. Recommended Actions

Recommended actions were assigned based on the identified inventory conditions.

The decision framework includes:

| Condition | Recommended Action |
|---|---|
| High stockout risk | Reorder urgently |
| Medium stockout risk | Review replenishment |
| High overstock risk | Reduce replenishment |
| Medium overstock risk | Monitor inventory |
| No elevated risk | Maintain normal stock |

The recommended actions are intended to support prioritised inventory decisions rather than replace operational judgement.

---

## 9. Business Impact

The risk dataset was enriched with:

- Inventory value
- Estimated stockout quantity exposure
- Estimated stockout value exposure
- Estimated excess inventory quantity
- Estimated excess inventory value

Inventory value was estimated using:

**Inventory Value = Stock on Hand × Cost Price**

Potential stockout exposure was estimated using the difference between average weekly demand and stock on hand when demand exceeded available inventory.

Potential excess inventory was estimated using the amount of stock above the 26-week inventory coverage threshold.

These measures provide an approximate financial view of the inventory risks identified by the analysis.

---

## 10. Final Output

The completed risk-scoring dataset has been saved as:

`data/processed/risk_scoring_output.csv`

The dataset contains the original inventory information together with:

- Historical demand metrics
- Inventory coverage
- Stockout risk
- Overstock risk
- Risk score
- Risk level
- Recommended action
- Inventory value
- Stockout exposure
- Excess inventory exposure

This dataset will be used as an input for the planning dashboard.

---

## 11. Limitations

The risk-scoring framework has several limitations:

1. Inventory coverage is based on historical average demand and may not fully represent future demand changes.
2. The overstock thresholds are planning thresholds and should be reviewed with business stakeholders.
3. Stockout exposure is an estimate and does not account for lost sales behaviour, substitution, or service-level effects.
4. The analysis uses the available inventory snapshot and therefore represents inventory conditions at the time of the snapshot.
5. Recommended actions should be reviewed against operational constraints such as supplier lead times, minimum order quantities, and upcoming promotions.

---

## 12. Conclusion

The risk-scoring analysis provides a transparent SKU-store level framework for identifying potential inventory problems.

The analysis highlights both potential stockout exposure and substantial inventory coverage. By combining these indicators into risk levels and recommended actions, the resulting dataset provides a practical foundation for inventory planning and decision support.

The final risk dataset will be carried forward into the planning dashboard developed in the next phase.