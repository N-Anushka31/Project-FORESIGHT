import os
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FORESIGHT | Inventory Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background: #f5f7fb;
        }

        [data-testid="stSidebar"] {
            background: #111827;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        /* Upload button */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;  
        }

        /* Upload button hover */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
        background-color: #222222 !important;
        color: #ffffff !important;
        border-color: #222222 !important;
        }

        .brand {
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }

        .brand-subtitle {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 25px;
        }

        .page-title {
            font-size: 36px;
            font-weight: 800;
            color: #172554;
            margin-bottom: 5px;
        }

        .page-subtitle {
            color: #64748b;
            font-size: 16px;
            margin-bottom: 25px;
        }

        .metric-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px;
            min-height: 120px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }

        .metric-label {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 8px;
        }

        .metric-value {
            color: #172554;
            font-size: 30px;
            font-weight: 800;
        }

        .metric-note {
            color: #94a3b8;
            font-size: 12px;
            margin-top: 5px;
        }

        .section-title {
            color: #172554;
            font-size: 24px;
            font-weight: 750;
            margin-top: 25px;
            margin-bottom: 5px;
        }

        .section-subtitle {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 15px;
        }

        .source-box {
            background: #eef6ff;
            border: 1px solid #bfdbfe;
            border-radius: 10px;
            padding: 12px 15px;
            color: #1e3a8a;
            font-size: 13px;
            margin-bottom: 18px;
        }

        .hero {
            background: linear-gradient(135deg, #172554, #2563eb);
            color: white;
            border-radius: 22px;
            padding: 34px 40px;
            margin-bottom: 25px;
        }

        .hero-label {
            font-size: 15px;
            font-weight: 600;
            opacity: 0.85;
            margin-bottom: 10px;
        }

        .hero-title {
            font-size: 42px;
            font-weight: 850;
            line-height: 1.05;
            margin-bottom: 12px;
        }

        .hero-text {
            font-size: 16px;
            line-height: 1.6;
            max-width: 850px;
            opacity: 0.9;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIRS = [
    BASE_DIR / "data" / "processed",
    BASE_DIR / "data" / "raw",
    BASE_DIR / "data",
    BASE_DIR.parent / "data" / "processed",
    BASE_DIR.parent / "data" / "raw",
    BASE_DIR.parent / "data",
]

# Your generated planning dataset is checked first.
PLANNING_FILES = [
    "planning_dataset_final.csv",
    "planning_dataset.csv",
    "model_dataset.csv",
    "forecast_dataset.csv",
    "demand_forecast.csv",
]


# ============================================================
# COLUMN ALIASES
# ============================================================

ALIASES = {
    "sku": [
        "sku", "sku_id", "product_id", "item_id",
        "item", "product", "product_code"
    ],
    "category": [
        "category", "product_category", "department",
        "dept", "cat"
    ],
    "date": [
        "date", "ds", "month", "period", "timestamp",
        "order_date", "transaction_date"
    ],
    "forecast": [
        "forecast", "forecast_demand", "demand_forecast",
        "predicted_demand", "prediction", "forecast_qty"
    ],
    "actual": [
        "actual", "actual_demand", "actual_sales", "sales",
        "demand", "quantity_sold", "qty_sold", "units_sold"
    ],
    "stock": [
        "stock", "stock_qty", "inventory", "inventory_qty",
        "on_hand", "on_hand_qty", "current_stock",
        "stock_on_hand"
    ],
    "reorder_point": [
        "reorder_point", "reorder_level", "rop",
        "minimum_stock", "min_stock"
    ],
    "risk": [
        "risk", "risk_level", "stockout_risk"
    ],
    "action": [
        "action", "recommended_action", "recommendation"
    ],
    "priority": [
        "priority", "priority_score", "priority_level"
    ],
}


def normalise_name(name):
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )


def detect_column(columns, aliases):
    lookup = {normalise_name(c): c for c in columns}

    for alias in aliases:
        if alias in lookup:
            return lookup[alias]

    for column in columns:
        n = normalise_name(column)
        for alias in aliases:
            if alias in n or n in alias:
                return column

    return None


# ============================================================
# FILE HELPERS
# ============================================================

def find_data_file(names):
    for directory in DATA_DIRS:
        if not directory.exists():
            continue

        for name in names:
            path = directory / name
            if path.exists() and path.is_file():
                return path

    return None


def read_csv_safely(path):
    try:
        return pd.read_csv(path, low_memory=True)
    except Exception:
        try:
            return pd.read_csv(path, engine="python")
        except Exception:
            return None


# ============================================================
# SEEDED FALLBACK DATA
# ============================================================

@st.cache_data(show_spinner=False)
def create_seeded_dataset():
    rng = np.random.default_rng(42)

    skus = [f"SKU-{i:03d}" for i in range(1, 13)]
    categories = ["Apparel", "Home", "Electronics", "Beauty"]

    dates = pd.date_range(
        end=pd.Timestamp.today().replace(day=1),
        periods=12,
        freq="MS",
    )

    rows = []

    for sku_index, sku in enumerate(skus):
        category = categories[sku_index % len(categories)]
        base = 45 + (sku_index % 6) * 14

        if sku_index in [0, 5, 8]:
            stock_multiplier = 0.35
        elif sku_index in [2, 7, 10]:
            stock_multiplier = 2.4
        else:
            stock_multiplier = 1.1

        forecasts = []

        for month_index, date in enumerate(dates):
            seasonality = 1 + 0.10 * np.sin(month_index / 1.7)
            forecast = max(5, int(round(base * seasonality)))
            actual = max(
                0,
                int(round(forecast * rng.normal(1.0, 0.12))),
            )

            forecasts.append(forecast)

            rows.append(
                {
                    "date": date,
                    "sku": sku,
                    "category": category,
                    "forecast": forecast,
                    "actual": actual,
                }
            )

        avg_forecast = np.mean(forecasts)
        stock = max(5, int(round(avg_forecast * stock_multiplier)))
        reorder_point = max(10, int(round(avg_forecast * 0.85)))

        for row in rows[-len(dates):]:
            row["stock"] = stock
            row["reorder_point"] = reorder_point

    df = pd.DataFrame(rows)

    return add_derived_fields(df)


# ============================================================
# STANDARDISE PLANNING DATA
# ============================================================

def standardise_planning_dataframe(df):
    if df is None or df.empty:
        return None

    columns = list(df.columns)

    detected = {
        key: detect_column(columns, aliases)
        for key, aliases in ALIASES.items()
    }

    if detected["sku"] is None:
        return None

    result = pd.DataFrame()

    # Required identity fields
    result["sku"] = (
        df[detected["sku"]]
        .astype(str)
        .str.strip()
    )

    if detected["category"]:
        result["category"] = (
            df[detected["category"]]
            .fillna("Uncategorised")
            .astype(str)
            .str.strip()
        )
    else:
        result["category"] = "Uncategorised"

    if detected["date"]:
        result["date"] = pd.to_datetime(
            df[detected["date"]],
            errors="coerce",
        )
    else:
        result["date"] = pd.Timestamp.today().normalize()

    # Numeric planning fields
    for field in ["forecast", "actual", "stock", "reorder_point"]:
        source = detected[field]

        if source:
            result[field] = pd.to_numeric(
                df[source],
                errors="coerce",
            )
        else:
            result[field] = np.nan

    # Preserve the risk/action/priority already calculated
    # in your planning dataset whenever those columns exist.
    if detected["risk"]:
        result["risk"] = (
            df[detected["risk"]]
            .fillna("")
            .astype(str)
            .str.strip()
        )
    else:
        result["risk"] = ""

    if detected["action"]:
        result["action"] = (
            df[detected["action"]]
            .fillna("")
            .astype(str)
            .str.strip()
        )
    else:
        result["action"] = ""

    if detected["priority"]:
        result["priority"] = pd.to_numeric(
            df[detected["priority"]],
            errors="coerce",
        )
    else:
        result["priority"] = np.nan

    result = result.replace(
        {"": np.nan, "nan": np.nan, "None": np.nan}
    )

    result = result.dropna(subset=["sku"])

    return result


# ============================================================
# DERIVED RISK / ACTION FIELDS
# ============================================================

def add_derived_fields(df):
    df = df.copy()

    # Clean numeric fields
    for col in ["forecast", "actual", "stock", "reorder_point"]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce",
        )

    # If forecast is missing, use SKU average actual.
    if df["forecast"].notna().sum() == 0:
        df["forecast"] = (
            df.groupby("sku")["actual"]
            .transform("mean")
        )

    # If actual is missing, use forecast as a transparent fallback.
    if df["actual"].notna().sum() == 0:
        df["actual"] = df["forecast"] * 0.95

    sku_avg_forecast = (
        df.groupby("sku")["forecast"]
        .transform("mean")
    )

    if df["stock"].notna().sum() == 0:
        df["stock"] = sku_avg_forecast * 1.10
    else:
        df["stock"] = df["stock"].fillna(
            sku_avg_forecast * 1.10
        )

    if df["reorder_point"].notna().sum() == 0:
        df["reorder_point"] = sku_avg_forecast * 0.85
    else:
        df["reorder_point"] = df["reorder_point"].fillna(
            sku_avg_forecast * 0.85
        )

    # Numeric cleanup
    for col in ["forecast", "actual", "stock", "reorder_point"]:
        df[col] = (
            pd.to_numeric(df[col], errors="coerce")
            .fillna(0)
            .clip(lower=0)
        )

    # --------------------------------------------------------
    # Risk
    # Keep the risk from the user's dataset if it exists.
    # Calculate only missing risk values.
    # --------------------------------------------------------

    coverage = np.where(
        df["forecast"] > 0,
        df["stock"] / df["forecast"],
        999,
    )

    calculated_risk = np.select(
        [
            df["stock"] <= df["reorder_point"],
            coverage < 0.75,
            coverage > 2.0,
        ],
        [
            "High",
            "Medium",
            "Low",
        ],
        default="Low",
    )

    if "risk" not in df.columns:
        df["risk"] = "Low"

    if "action" not in df.columns:
        df["action"] = df["risk"].map({
            "High": "Reduce replenishment",
            "Medium": "Monitor inventory",
            "Low": "Maintain inventory"
        }).fillna("Monitor inventory")

    df["risk"] = (
        df["risk"]
        .fillna(pd.Series(calculated_risk, index=df.index))
        .replace("", np.nan)
        .fillna(pd.Series(calculated_risk, index=df.index))
    )

    # Normalise common risk labels.
    df["risk"] = (
        df["risk"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # --------------------------------------------------------
    # Action
    # Keep existing action if supplied.
    # --------------------------------------------------------

    reorder_qty = (
        df["forecast"] * 1.25 - df["stock"]
    ).clip(lower=0)

    calculated_action = np.select(
        [
            (reorder_qty > 0)
            & df["risk"].isin(["High", "Medium"]),
            (coverage > 2.0)
            & (df["actual"] < df["forecast"] * 0.90),
        ],
        [
            "REORDER URGENTLY",
            "MARKDOWN",
        ],
        default="MONITOR INVENTORY",
    )

    df["action"] = (
        df["action"]
        .replace("", np.nan)
        .fillna(pd.Series(calculated_action, index=df.index))
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Priority
    # Existing priority is preserved.
    # --------------------------------------------------------

    calculated_priority = (
        df["risk"].map(
            {
                "High": 3,
                "Medium": 2,
                "Low": 1,
            }
        )
        .fillna(1)
    )

    df["priority"] = (
        pd.to_numeric(df["priority"], errors="coerce")
        .fillna(calculated_priority)
    )

    df["reorder_qty"] = reorder_qty.round().astype(int)

    df["stock_cover_months"] = np.where(
        df["forecast"] > 0,
        df["stock"] / df["forecast"],
        0,
    )

    df["variance_pct"] = np.where(
        df["forecast"] > 0,
        ((df["actual"] - df["forecast"]) / df["forecast"]) * 100,
        0,
    )

    return df


# ============================================================
# LOAD REAL DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_project_data():
    messages = []

    planning_path = find_data_file(PLANNING_FILES)

    if planning_path is None:
        messages.append(
            "planning_dataset_final.csv was not found. "
            "Using seeded fallback data."
        )
        return (
            create_seeded_dataset(),
            messages,
            "Seeded fallback data",
        )

    raw = read_csv_safely(planning_path)

    if raw is None or raw.empty:
        messages.append(
            f"{planning_path.name} could not be read. "
            "Using seeded fallback data."
        )
        return (
            create_seeded_dataset(),
            messages,
            "Seeded fallback data",
        )

    data = standardise_planning_dataframe(raw)

    if data is None or data.empty:
        messages.append(
            f"{planning_path.name} does not contain a usable SKU column. "
            "Using seeded fallback data."
        )
        return (
            create_seeded_dataset(),
            messages,
            "Seeded fallback data",
        )

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce",
    )

    data = data.dropna(subset=["date"])

    # Monthly planning data is the expected grain for the dashboard.
    data["date"] = (
        data["date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    data = add_derived_fields(data)

    messages.append(
        f"Loaded {planning_path.name} successfully."
    )

    return (
        data,
        messages,
        f"Project dataset: {planning_path.name}",
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">📊 FORESIGHT</div>
        <div class="brand-subtitle">
            Demand Forecasting & Inventory Planning
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Dashboard")

    page = st.radio(
        "Navigation",
        [
            "Planning Dashboard",
            "SKU Detail",
            "Data Status",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Data")

    uploaded_file = st.file_uploader(
        "Optional planning CSV",
        type=["csv"],
        help=(
            "Upload a planning CSV to override the local project dataset. "
            "If it is invalid, the app falls back to the local dataset "
            "and then seeded data."
        ),
    )

    st.caption(
        "Local planning_dataset_final.csv is loaded automatically. "
        "Seeded data is used only when the project dataset is unavailable."
    )


# ============================================================
# LOAD DATA
# ============================================================

with st.spinner("Loading planning data..."):

    if uploaded_file is not None:
        try:
            uploaded_raw = pd.read_csv(
                uploaded_file,
                low_memory=True,
            )

            uploaded_data = standardise_planning_dataframe(
                uploaded_raw
            )

            if uploaded_data is not None and not uploaded_data.empty:
                data = uploaded_data

                data["date"] = pd.to_datetime(
                    data["date"],
                    errors="coerce",
                )

                data = data.dropna(subset=["date"])

                data["date"] = (
                    data["date"]
                    .dt.to_period("M")
                    .dt.to_timestamp()
                )

                data = add_derived_fields(data)

                data_source = "Uploaded planning CSV"
                load_messages = [
                    "Uploaded planning CSV loaded successfully."
                ]

            else:
                data, load_messages, data_source = (
                    load_project_data()
                )
                load_messages.insert(
                    0,
                    "Uploaded CSV was not recognised. "
                    "Using the project dataset/fallback.",
                )

        except Exception as exc:
            data, load_messages, data_source = (
                load_project_data()
            )
            load_messages.insert(
                0,
                f"Uploaded CSV could not be read ({exc}). "
                "Using the project dataset/fallback.",
            )

    else:
        data, load_messages, data_source = (
            load_project_data()
        )


# ============================================================
# EMPTY STATE
# ============================================================

if data is None or data.empty:
    st.title("FORESIGHT Planning Dashboard")
    st.error("No planning data is available.")
    st.info(
        "Place planning_dataset_final.csv in data/processed "
        "or upload a valid CSV from the sidebar."
    )
    st.stop()


# ============================================================
# FINAL CLEANUP
# ============================================================

data = data.copy()

data["sku"] = (
    data["sku"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

data["category"] = (
    data["category"]
    .fillna("Uncategorised")
    .astype(str)
    .str.strip()
)

data["date"] = pd.to_datetime(
    data["date"],
    errors="coerce",
)

data = data.dropna(subset=["date"])

for col in [
    "forecast",
    "actual",
    "stock",
    "reorder_point",
    "priority",
]:
    data[col] = pd.to_numeric(
        data[col],
        errors="coerce",
    ).fillna(0)

# Source information
st.markdown(
    f"""
    <div class="source-box">
        <strong>Data source:</strong> {data_source}
        &nbsp; • &nbsp;
        <strong>Records:</strong> {len(data):,}
        &nbsp; • &nbsp;
        <strong>SKUs:</strong> {data["sku"].nunique():,}
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PLANNING DASHBOARD
# ============================================================

if page == "Planning Dashboard":

    st.markdown(
        '<div class="page-title">Planning Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Monitor demand, compare actual performance with forecasts,
            identify inventory risk, and prioritise SKU-level actions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">Inventory Intelligence Platform</div>
            <div class="hero-title">Plan smarter. Act earlier.</div>
            <div class="hero-text">
                Monitor demand, compare actual performance with forecasts,
                identify inventory risk, and prioritise SKU-level planning
                actions using your project planning dataset.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.markdown("### Filters")

    f1, f2 = st.columns(2)

    categories = sorted(data["category"].unique().tolist())

    with f1:
        selected_categories = st.multiselect(
            "Category",
            categories,
            default=categories,
        )

    category_filtered = data[
        data["category"].isin(selected_categories)
    ]

    available_skus = sorted(
        category_filtered["sku"].unique().tolist()
    )

    with f2:
        selected_skus = st.multiselect(
            "SKU",
            available_skus,
            default=available_skus,
        )

    filtered = data[
        data["category"].isin(selected_categories)
        & data["sku"].isin(selected_skus)
    ].copy()

    if filtered.empty:
        st.warning(
            "No records match the selected filters."
        )
        st.stop()

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------

    sku_summary = (
        filtered.sort_values("date")
        .groupby("sku", as_index=False)
        .tail(1)
    )

    high_risk = int(
        (sku_summary["risk"] == "High").sum()
    )

    reorder_count = int(
        sku_summary["action"].astype(str).str.upper().eq("REORDER URGENTLY").sum()
    )

    # Also recognise the action wording from your generated dataset.
    reduce_replenishment_count = int(
        sku_summary["action"]
        .astype(str)
        .str.lower()
        .eq("reduce replenishment")
        .sum()
    )

    total_actions = reorder_count + reduce_replenishment_count

    forecast_total = float(
        filtered["forecast"].sum()
    )

    actual_total = float(
        filtered["actual"].sum()
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">SKUs</div>
                <div class="metric-value">
                    {filtered["sku"].nunique():,}
                </div>
                <div class="metric-note">Selected products</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Forecast Demand</div>
                <div class="metric-value">
                    {forecast_total:,.0f}
                </div>
                <div class="metric-note">Selected period</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Actual Demand</div>
                <div class="metric-value">
                    {actual_total:,.0f}
                </div>
                <div class="metric-note">Selected period</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">High Risk SKUs</div>
                <div class="metric-value">
                    {high_risk:,}
                </div>
                <div class="metric-note">Immediate attention</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c5:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Priority Actions</div>
                <div class="metric-value">
                    {total_actions:,}
                </div>
                <div class="metric-note">
                    Reorder / reduce replenishment
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # FORECAST VS ACTUAL GRAPH
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Forecast vs Actual</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Monthly comparison of forecast demand against actual demand.
        </div>
        """,
        unsafe_allow_html=True,
    )

    monthly = (
        filtered.groupby("date", as_index=True)
        .agg(
            Forecast=("forecast", "sum"),
            Actual=("actual", "sum"),
        )
        .sort_index()
    )

    fig = px.line(monthly)
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)

    if monthly["Forecast"].sum() > 0:
        variance = (
            (monthly["Actual"].sum() - monthly["Forecast"].sum())
            / monthly["Forecast"].sum()
        ) * 100

        st.caption(
            f"Overall actual vs forecast variance: {variance:+.1f}%"
        )

    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Risk Distribution</div>',
        unsafe_allow_html=True,
    )

    risk_counts = (
        sku_summary["risk"]
        .value_counts()
        .reindex(
            ["High", "Medium", "Low"],
            fill_value=0,
        )
    )

    st.bar_chart(
        risk_counts,
        height=300,
    )

    # --------------------------------------------------------
    # ACTION TABLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Prioritised SKU Actions</div>',
        unsafe_allow_html=True,
    )

    action_filter = st.radio(
        "Show actions",
        [
            "All",
            "REORDER URGENTLY",
            "REDUCE REPLENISHMENT",
            "MONITOR INVENTORY",
            "REVIEW REPLENISHMENT",
            "MAINTAIN NORMAL STOCK",
        ],
        horizontal=True,
    )

    action_table = sku_summary.copy()

    action_upper = (
        action_table["action"]
        .astype(str)
        .str.upper()
    )

    if action_filter == "REORDER URGENTLY":
        action_table = action_table[
            action_upper == "REORDER URGENTLY"
        ]
    elif action_filter == "REDUCE REPLENISHMENT":
        action_table = action_table[
            action_upper == "REDUCE REPLENISHMENT"
        ]
    elif action_filter == "MONITOR INVENTORY":
        action_table = action_table[
            action_upper == "MONITOR INVENTORY"
        ]
    elif action_filter == "REVIEW REPLENISHMENT":
            action_table = action_table[
                action_upper == "REVIEW REPLENISHMENT"
            ]
    elif action_filter == "MAINTAIN NORMAL STOCK":
        action_table = action_table[
            ~action_upper.isin(
                [
                    "REORDER URGENTLY",
                    "REDUCE REPLENISHMENT",
                    "REVIEW REPLENISHMENT",
                    "MONITOR INVENTORY",
                ]
            )
        ]

    action_table = action_table.sort_values(
        ["priority", "risk"],
        ascending=[False, True],
    )

    if action_table.empty:
        st.info("No SKUs match this action.")
    else:
        display = action_table[
            [
                "sku",
                "category",
                "risk",
                "action",
                "priority",
                "stock",
                "reorder_point",
                "forecast",
                "actual",
                "stock_cover_months",
                "variance_pct",
            ]
        ].copy()

        display.columns = [
            "SKU",
            "Category",
            "Risk",
            "Action",
            "Priority",
            "Stock",
            "Reorder Point",
            "Forecast",
            "Actual",
            "Stock Cover (Months)",
            "Variance %",
        ]

        display["Stock Cover (Months)"] = (
            display["Stock Cover (Months)"].round(1)
        )

        display["Variance %"] = (
            display["Variance %"]
            .round(1)
            .map(lambda x: f"{x:+.1f}%")
        )

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# SKU DETAIL
# ============================================================

elif page == "SKU Detail":

    st.markdown(
        '<div class="page-title">SKU Detail</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Select one SKU to inspect its demand history,
            forecast performance, inventory position, risk,
            and recommended action.
        </div>
        """,
        unsafe_allow_html=True,
    )

    sku_options = sorted(
        data["sku"].unique().tolist()
    )

    selected_sku = st.selectbox(
        "Select SKU",
        sku_options,
        key="sku_detail",
    )

    sku_data = data[
        data["sku"] == selected_sku
    ].copy()

    sku_data = sku_data.sort_values("date")

    if sku_data.empty:
        st.warning("No data available for this SKU.")
        st.stop()

    latest = sku_data.iloc[-1]

    # --------------------------------------------------------
    # SKU SUMMARY
    # --------------------------------------------------------

    d1, d2, d3, d4, d5 = st.columns(5)

    with d1:
        st.metric(
            "Risk",
            str(latest["risk"]),
        )

    with d2:
        st.metric(
            "Action",
            str(latest["action"]),
        )

    with d3:
        st.metric(
            "Current Stock",
            f"{latest['stock']:,.0f}",
        )

    with d4:
        st.metric(
            "Reorder Point",
            f"{latest['reorder_point']:,.0f}",
        )

    with d5:
        st.metric(
            "Priority",
            f"{latest['priority']:,.0f}",
        )

    st.info(
        f"Recommended action for {selected_sku}: "
        f"{latest['action']}"
    )

    # --------------------------------------------------------
    # GRAPH 1: ACTUAL VS FORECAST
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Demand: Actual vs Forecast</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-subtitle">
            This graph shows how the selected SKU's actual demand
            compares with the forecast over time.
        </div>
        """,
        unsafe_allow_html=True,
    )

    demand_chart = (
        sku_data.groupby("date")
        .agg(
            Actual=("actual", "sum"),
            Forecast=("forecast", "sum"),
        )
        .sort_index()
    )

    st.line_chart(
        demand_chart,
        height=420,
    )

    # --------------------------------------------------------
    # GRAPH 2: STOCK VS REORDER POINT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Inventory: Stock vs Reorder Point</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Stock below the reorder point indicates that the SKU
            needs closer replenishment attention.
        </div>
        """,
        unsafe_allow_html=True,
    )

    inventory_chart = (
        sku_data.groupby("date")
        .agg(
            Stock=("stock", "max"),
            Reorder_Point=("reorder_point", "max"),
        )
        .sort_index()
    )

    st.line_chart(
        inventory_chart,
        height=420,
    )

    # --------------------------------------------------------
    # GRAPH 3: ACTUAL / FORECAST VARIANCE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Forecast Variance</div>',
        unsafe_allow_html=True,
    )

    variance_chart = sku_data[
        ["date", "variance_pct"]
    ].copy()

    variance_chart = (
        variance_chart.groupby("date")["variance_pct"]
        .mean()
        .sort_index()
        .to_frame("Variance %")
    )

    st.bar_chart(
        variance_chart,
        height=300,
    )

    # --------------------------------------------------------
    # SKU DETAILS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">SKU Planning Information</div>',
        unsafe_allow_html=True,
    )

    avg_forecast = sku_data["forecast"].mean()
    avg_actual = sku_data["actual"].mean()

    detail = pd.DataFrame(
        {
            "Metric": [
                "SKU",
                "Category",
                "Average Forecast",
                "Average Actual",
                "Latest Forecast",
                "Latest Actual",
                "Current Stock",
                "Reorder Point",
                "Stock Cover",
                "Risk",
                "Recommended Action",
                "Priority",
            ],
            "Value": [
                selected_sku,
                latest["category"],
                f"{avg_forecast:,.1f}",
                f"{avg_actual:,.1f}",
                f"{latest['forecast']:,.1f}",
                f"{latest['actual']:,.1f}",
                f"{latest['stock']:,.0f}",
                f"{latest['reorder_point']:,.0f}",
                f"{latest['stock_cover_months']:.1f} months",
                latest["risk"],
                latest["action"],
                f"{latest['priority']:,.0f}",
            ],
        }
    )

    st.dataframe(
        detail,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # SKU HISTORY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">SKU History</div>',
        unsafe_allow_html=True,
    )

    history = sku_data[
        [
            "date",
            "actual",
            "forecast",
            "stock",
            "reorder_point",
            "risk",
            "action",
            "priority",
        ]
    ].copy()

    history.columns = [
        "Date",
        "Actual",
        "Forecast",
        "Stock",
        "Reorder Point",
        "Risk",
        "Action",
        "Priority",
    ]

    st.dataframe(
        history.sort_values(
            "Date",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# DATA STATUS
# ============================================================

elif page == "Data Status":

    st.markdown(
        '<div class="page-title">Data Status</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Verify that the real planning dataset is being used
            and inspect dashboard data coverage.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success(
        f"Current source: {data_source}"
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Records",
            f"{len(data):,}",
        )

    with s2:
        st.metric(
            "SKUs",
            f"{data['sku'].nunique():,}",
        )

    with s3:
        st.metric(
            "Categories",
            f"{data['category'].nunique():,}",
        )

    with s4:
        st.metric(
            "Months",
            f"{data['date'].dt.to_period('M').nunique():,}",
        )

    st.markdown(
        '<div class="section-title">Dataset Columns</div>',
        unsafe_allow_html=True,
    )

    st.write(
        list(data.columns)
    )

    st.markdown(
        '<div class="section-title">Data Coverage</div>',
        unsafe_allow_html=True,
    )

    coverage = pd.DataFrame(
        {
            "Check": [
                "SKU",
                "Category",
                "Date",
                "Actual",
                "Forecast",
                "Stock",
                "Reorder Point",
                "Risk",
                "Action",
                "Priority",
            ],
            "Available": [
                data["sku"].notna().any(),
                data["category"].notna().any(),
                data["date"].notna().any(),
                data["actual"].notna().any(),
                data["forecast"].notna().any(),
                data["stock"].notna().any(),
                data["reorder_point"].notna().any(),
                data["risk"].notna().any(),
                data["action"].notna().any(),
                data["priority"].notna().any(),
            ],
        }
    )

    coverage["Status"] = coverage["Available"].map(
        {
            True: "Ready",
            False: "Missing",
        }
    )

    st.dataframe(
        coverage[["Check", "Status"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        '<div class="section-title">Loading Messages</div>',
        unsafe_allow_html=True,
    )

    for message in load_messages:
        st.info(message)

    st.markdown(
        '<div class="section-title">Current Dataset Preview</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        data.head(20),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <div style="
        text-align:center;
        color:#94a3b8;
        font-size:12px;
        padding:20px;
    ">
        FORESIGHT • Inventory Planning & Demand Decision Support
    </div>
    """,
    unsafe_allow_html=True,
)