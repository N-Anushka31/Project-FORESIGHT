import pandas as pd
import numpy as np


def prepare_forecast_data(df):
    """
    Prepare actual and forecast demand data.
    """

    df = df.copy()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

    for column in ["actual", "forecast"]:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    if "sku" in df.columns:
        df["sku"] = df["sku"].astype(str)

    return df


def calculate_forecast_error(df):
    """
    Calculate forecast error metrics.
    """

    df = prepare_forecast_data(df)

    if "actual" not in df.columns or "forecast" not in df.columns:
        return df

    df["error"] = df["actual"] - df["forecast"]

    df["absolute_error"] = (
        df["actual"] - df["forecast"]
    ).abs()

    df["percentage_error"] = np.where(
        df["actual"] != 0,
        (
            df["absolute_error"]
            / df["actual"].abs()
        ) * 100,
        np.nan,
    )

    return df


def forecast_summary(df):
    """
    Return overall forecast performance summary.
    """

    df = calculate_forecast_error(df)

    if df.empty:
        return {
            "actual_total": 0,
            "forecast_total": 0,
            "mae": 0,
            "mape": 0,
        }

    actual_total = df["actual"].sum()
    forecast_total = df["forecast"].sum()

    mae = df["absolute_error"].mean()

    valid_mape = df["percentage_error"].dropna()

    mape = (
        valid_mape.mean()
        if not valid_mape.empty
        else 0
    )

    return {
        "actual_total": float(actual_total),
        "forecast_total": float(forecast_total),
        "mae": float(mae),
        "mape": float(mape),
    }


def sku_forecast(df, sku):
    """
    Return forecast history for a selected SKU.
    """

    df = prepare_forecast_data(df)

    if "sku" not in df.columns:
        return pd.DataFrame()

    result = df[
        df["sku"].astype(str) == str(sku)
    ].copy()

    if "date" in result.columns:
        result = result.sort_values("date")

    return result


def aggregate_forecast(df):
    """
    Aggregate actual and forecast demand by date.
    """

    df = prepare_forecast_data(df)

    required = {"date", "actual", "forecast"}

    if not required.issubset(df.columns):
        return pd.DataFrame()

    result = (
        df.groupby("date", as_index=False)
        .agg(
            actual=("actual", "sum"),
            forecast=("forecast", "sum"),
        )
        .sort_values("date")
    )

    return result