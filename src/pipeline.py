from pathlib import Path
import pandas as pd


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def load_csv(filename, folder=PROCESSED_DIR):
    """
    Load a CSV file from the specified project data folder.
    """
    path = folder / filename

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)


def load_planning_data(filename="planning_dataset_final.csv"):
    """
    Load the planning dataset used by the Streamlit dashboard.
    """
    return load_csv(filename, PROCESSED_DIR)


def load_inventory_data(filename="inventory.csv"):
    """
    Load inventory data.
    """
    return load_csv(filename, PROCESSED_DIR)


def load_risk_data(filename="risk.csv"):
    """
    Load inventory risk data.
    """
    return load_csv(filename, PROCESSED_DIR)


def prepare_planning_data(df):
    """
    Basic preparation for the planning dataset.
    """

    df = df.copy()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_columns = [
        "actual",
        "forecast",
        "stock",
        "reorder_point",
        "priority",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    if "sku" in df.columns:
        df["sku"] = df["sku"].astype(str)

    if "risk" in df.columns:
        df["risk"] = df["risk"].astype(str)

    if "action" in df.columns:
        df["action"] = df["action"].astype(str)

    return df


def prepare_inventory_data(df):
    """
    Basic preparation for inventory data.
    """

    df = df.copy()

    numeric_columns = [
        "stock_on_hand",
        "reorder_point",
        "safety_stock",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    if "last_restock_date" in df.columns:
        df["last_restock_date"] = pd.to_datetime(
            df["last_restock_date"],
            errors="coerce"
        )

    if "sku_id" in df.columns:
        df["sku_id"] = df["sku_id"].astype(str)

    return df


def prepare_risk_data(df):
    """
    Basic preparation for the inventory risk dataset.
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

    if "last_restock_date" in df.columns:
        df["last_restock_date"] = pd.to_datetime(
            df["last_restock_date"],
            errors="coerce"
        )

    if "sku_id" in df.columns:
        df["sku_id"] = df["sku_id"].astype(str)

    return df


def get_data_summary(df):
    """
    Return basic information about a dataset.
    """

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }