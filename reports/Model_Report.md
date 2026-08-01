# Model Report

## Phase 5 – Demand Forecasting

---

# Objective

The objective of this phase was to develop a weekly SKU-level demand forecasting model to support inventory planning. The forecasting model was evaluated against a Seasonal Naive Baseline to determine whether machine learning could improve forecasting accuracy.

---

# Dataset

The forecasting model was developed using the processed weekly demand dataset created during the feature engineering phase.

**Target Variable**

- weekly_quantity

**Features Used**

- SKU Code
- Year
- Month
- Quarter
- Week
- Lag 1
- Lag 2
- Lag 4
- Rolling Mean (4 Weeks)

These features capture both calendar effects and historical demand patterns.

---

# Baseline Model

A Seasonal Naive Forecast was implemented as the benchmark model.

### Baseline Performance

| Metric | Value |
|---------|------:|
| WAPE | 36.09% |
| MAE | 6.49 |
| RMSE | 11.49 |

The baseline assumes that future demand follows historical seasonal demand patterns and serves as the reference for model evaluation.

---

# Machine Learning Model

A Random Forest Regressor was trained using engineered time-series features.

### Model Configuration

- Algorithm: Random Forest Regressor
- Trees: 200
- Maximum Depth: 20
- Random State: 42

### Additional Features

- Lag 1
- Lag 2
- Lag 4
- Rolling Mean (4 Weeks)

These features allow the model to learn demand behaviour from previous weeks while avoiding data leakage.

---

# Model Performance

| Metric | Value |
|---------|------:|
| WAPE | 33.52% |
| MAE | 7.11 |
| RMSE | 31.32 |

---

# Baseline vs Random Forest

| Metric | Baseline | Random Forest |
|---------|----------:|--------------:|
| WAPE | 36.09% | 33.52% |
| MAE | 6.49 | 7.11 |
| RMSE | 11.49 | 31.32 |

### Interpretation

- The Random Forest model reduced WAPE from **36.09%** to **33.52%**, indicating improved overall forecasting accuracy.
- MAE and RMSE are higher than the baseline, suggesting that while the model improved the overall percentage error, it produced larger errors for some individual observations.
- The inclusion of lag features and rolling averages helped the model capture historical demand patterns more effectively.

---

# Rolling-Origin Cross-Validation

Rolling-Origin Cross-Validation was performed using five chronological folds to evaluate the forecasting model while preserving the time order of the data.

This approach prevents data leakage and provides a more reliable estimate of forecasting performance compared with random cross-validation.

---

# Model Strengths

- Uses historical demand information through lag features.
- Captures seasonal and temporal demand patterns.
- Prevents data leakage using chronological validation.
- Produces weekly SKU-level demand forecasts.
- Can support inventory planning and replenishment decisions.

---

# Model Limitations

- Random Forest does not explicitly model sequential time-series dependencies.
- Additional external variables such as holidays, weather, supplier lead times, and marketing campaigns were not included.
- Hyperparameter tuning was limited and may further improve forecasting accuracy.
- Higher RMSE indicates sensitivity to large demand fluctuations.

---

# Future Improvements

Future versions of the forecasting model may include:

- XGBoost Regressor
- LightGBM
- CatBoost
- Prophet
- LSTM-based deep learning models
- Hyperparameter optimization
- Additional business and seasonal features

---

# Conclusion

A Random Forest forecasting model was developed to predict weekly SKU demand using engineered time-series features. The model achieved a **WAPE of 33.52%**, improving upon the Seasonal Naive Baseline (**36.09%**). Rolling-Origin Cross-Validation was used to validate the model while preventing data leakage. The forecasting model provides a practical foundation for inventory planning and serves as the input for the subsequent Risk Scoring phase.