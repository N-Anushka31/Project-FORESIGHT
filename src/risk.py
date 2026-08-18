import pandas as pd
import numpy as np


def prepare_risk_data(df):
    """
    Prepare inventory risk data for analysis.
    """

    df = df.copy()

    numeric_columns = [
        "stock_on_hand",
        "reorder_point",
        "safety_stock",
        "total_quantity",
        "average_weekly_demand",
        "total_sales",
        "average_unit_price",
        "cost_price",
        "inventory_coverage_weeks",
        "risk_score",
        "inventory_value",
        "stockout_quantity_exposure",
        "stockout_value_exposure",
        "excess_inventory_quantity",
        "excess_inventory_value",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    if "sku_id" in df.columns:
        df["sku_id"] = df["sku_id"].astype(str)

    if "store_id" in df.columns:
        df["store_id"] = df["store_id"].astype(str)

    return df


def calculate_risk_level(df):
    """
    Calculate a basic inventory risk level when
    a risk level is not already available.
    """

    df = df.copy()

    if "risk_level" in df.columns:
        return df

    if "risk_score" not in df.columns:
        return df

    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-np.inf, 0.33, 0.66, np.inf],
        labels=["Low", "Medium", "High"],
    )

    return df


def risk_summary(df):
    """
    Return a summary of inventory risk levels.
    """

    df = prepare_risk_data(df)

    if "risk_level" not in df.columns:
        df = calculate_risk_level(df)

    if "risk_level" not in df.columns:
        return {}

    return (
        df["risk_level"]
        .value_counts()
        .to_dict()
    )


def high_risk_items(df):
    """
    Return high-risk inventory items.
    """

    df = prepare_risk_data(df)

    if "risk_level" not in df.columns:
        df = calculate_risk_level(df)

    if "risk_level" not in df.columns:
        return pd.DataFrame()

    return df[
        df["risk_level"]
        .astype(str)
        .str.lower()
        == "high"
    ].copy()


def calculate_stockout_exposure(df):
    """
    Calculate stockout exposure when required fields exist.
    """

    df = df.copy()

    if {
        "stock_on_hand",
        "average_weekly_demand",
    }.issubset(df.columns):

        df["stockout_quantity_exposure"] = np.maximum(
            df["average_weekly_demand"]
            - df["stock_on_hand"],
            0,
        )

    if {
        "stockout_quantity_exposure",
        "average_unit_price",
    }.issubset(df.columns):

        df["stockout_value_exposure"] = (
            df["stockout_quantity_exposure"]
            * df["average_unit_price"]
        )

    return df


def calculate_overstock_exposure(df):
    """
    Calculate excess inventory exposure.
    """

    df = df.copy()

    if {
        "stock_on_hand",
        "reorder_point",
    }.issubset(df.columns):

        df["excess_inventory_quantity"] = np.maximum(
            df["stock_on_hand"]
            - df["reorder_point"],
            0,
        )

    if {
        "excess_inventory_quantity",
        "cost_price",
    }.issubset(df.columns):

        df["excess_inventory_value"] = (
            df["excess_inventory_quantity"]
            * df["cost_price"]
        )

    return df