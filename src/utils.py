from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


def find_file(filename):
    """
    Search for a file in the project's common data folders.
    """

    locations = [
        BASE_DIR / "data" / "processed",
        BASE_DIR / "data" / "raw",
    ]

    for folder in locations:
        path = folder / filename

        if path.exists():
            return path

    return None


def safe_read_csv(filename):
    """
    Safely load a CSV file.
    Returns None if the file does not exist.
    """

    path = find_file(filename)

    if path is None:
        return None

    try:
        return pd.read_csv(path)
    except Exception:
        return None


def clean_column_names(df):
    """
    Standardize dataframe column names.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def format_number(value):
    """
    Format numbers for dashboard display.
    """

    if pd.isna(value):
        return "0"

    if isinstance(value, float):
        return f"{value:,.2f}"

    return f"{value:,}"


def format_percentage(value):
    """
    Format a numeric value as a percentage.
    """

    if pd.isna(value):
        return "0.00%"

    return f"{value:.2f}%"


def get_unique_values(df, column):
    """
    Return sorted unique values from a dataframe column.
    """

    if column not in df.columns:
        return []

    values = (
        df[column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    return sorted(values)


def filter_dataframe(df, column, value):
    """
    Filter dataframe by a selected value.
    """

    if column not in df.columns:
        return df.copy()

    if value is None or value == "All":
        return df.copy()

    return df[
        df[column].astype(str) == str(value)
    ].copy()