"""ETL pipeline for LA Crime Incidents - NST DVA Capstone 2, Section A Group 15.

Reads the raw crime CSV, applies all cleaning and feature-engineering steps
described in the data dictionary, and writes a processed file ready for
Tableau and notebook analysis.

Usage:
    python scripts/etl_pipeline.py \
        --input  data/raw/crime_dataset.csv \
        --output data/processed/crime_dataset_clean.csv

Output columns (24 canonical + derived):
    Canonical  : DR_NO, Date Rptd, DATE OCC, TIME OCC, AREA, AREA NAME,
                 Rpt Dist No, LOCATION, LAT, LON, Part 1-2, Crm Cd,
                 Crm Cd Desc, Crm Cd 1, Mocodes, Vict Age, Vict Sex,
                 Vict Descent, Premis Cd, Premis Desc, Weapon Used Cd,
                 Weapon Desc, Status, Status Desc
    Derived    : hour, day, month, year, time_of_day, Age Group, is_violent
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Columns to drop (sparse / high-missingness per data dictionary)
COLS_TO_DROP = ["Crm Cd 2", "Crm Cd 3", "Crm Cd 4", "Cross Street"]

# Valid LA bounding box (generous margins around LA County)
LA_LAT_MIN, LA_LAT_MAX = 33.70, 34.82
LA_LON_MIN, LA_LON_MAX = -118.95, -117.65

# Victim sex codes considered valid
VALID_VICT_SEX = {"F", "M", "X", "H"}

# Crime descriptions treated as violent (used for is_violent flag)
VIOLENT_CRIME_KEYWORDS = [
    "ASSAULT", "ROBBERY", "RAPE", "HOMICIDE", "MURDER",
    "KIDNAPPING", "MANSLAUGHTER", "SHOOTING", "STABBING",
    "BATTERY", "SEX", "HUMAN TRAFFICKING",
]

# Time-of-day buckets
TIME_OF_DAY_BINS  = [0,  6, 12, 17, 21, 24]
TIME_OF_DAY_LABELS = ["Night", "Morning", "Afternoon", "Evening", "Night"]

# Age group bins matching notebook derivation
AGE_BINS   = [0, 17, 25, 34, 44, 54, 64, 120]
AGE_LABELS = ["Under 18", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"]


# ---------------------------------------------------------------------------
# Step 1 – Load
# ---------------------------------------------------------------------------

def load_raw(input_path: Path) -> pd.DataFrame:
    """Read raw CSV and return a DataFrame."""
    print(f"[1/7] Loading raw data from: {input_path}")
    df = pd.read_csv(input_path, low_memory=False)
    print(f"      Raw shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


# ---------------------------------------------------------------------------
# Step 2 – Column cleanup
# ---------------------------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from column names (keep original names
    so they match the data dictionary exactly)."""
    df.columns = df.columns.str.strip()
    return df


def drop_sparse_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove columns flagged as high-missingness in the data dictionary."""
    cols_present = [c for c in COLS_TO_DROP if c in df.columns]
    df = df.drop(columns=cols_present)
    if cols_present:
        print(f"      Dropped sparse columns: {cols_present}")
    return df


# ---------------------------------------------------------------------------
# Step 3 – Date / time parsing
# ---------------------------------------------------------------------------

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Date Rptd and DATE OCC to datetime; normalise TIME OCC."""
    for col in ["Date Rptd", "DATE OCC"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # TIME OCC can arrive as an int (e.g. 1845 = 18:45) or as HH:MM:SS string
    if "TIME OCC" in df.columns:
        raw = df["TIME OCC"].astype(str).str.strip()
        # If purely numeric (up to 4 digits), treat as HHMM
        numeric_mask = raw.str.match(r"^\d{1,4}$")
        df.loc[numeric_mask, "TIME OCC"] = (
            raw[numeric_mask]
            .str.zfill(4)
            .apply(lambda t: f"{t[:2]}:{t[2:]}:00")
        )
        df["TIME OCC"] = pd.to_datetime(df["TIME OCC"], format="%H:%M:%S", errors="coerce").dt.time

    return df


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive hour, day, month, year and time_of_day from DATE OCC / TIME OCC."""
    if "DATE OCC" in df.columns:
        df["year"]  = df["DATE OCC"].dt.year
        df["month"] = df["DATE OCC"].dt.month
        df["day"]   = df["DATE OCC"].dt.day

    if "TIME OCC" in df.columns:
        # Extract hour from time object
        df["hour"] = df["TIME OCC"].apply(
            lambda t: t.hour if pd.notna(t) and hasattr(t, "hour") else pd.NA
        ).astype("Int64")

        # Time-of-day bucket (handles the duplicate "Night" label for wrap-around)
        def _bucket(h):
            if pd.isna(h):
                return pd.NA
            h = int(h)
            if 0 <= h < 6 or h >= 21:
                return "Night"
            elif 6 <= h < 12:
                return "Morning"
            elif 12 <= h < 17:
                return "Afternoon"
            else:
                return "Evening"

        df["time_of_day"] = df["hour"].apply(_bucket).astype("category")

    return df


# ---------------------------------------------------------------------------
# Step 4 – Deduplication
# ---------------------------------------------------------------------------

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate incidents keyed on DR_NO (primary identifier)."""
    before = len(df)
    if "DR_NO" in df.columns:
        df = df.drop_duplicates(subset=["DR_NO"]).reset_index(drop=True)
    else:
        df = df.drop_duplicates().reset_index(drop=True)
    dropped = before - len(df)
    if dropped:
        print(f"      Removed {dropped:,} duplicate rows (DR_NO key)")
    return df


# ---------------------------------------------------------------------------
# Step 5 – Field-level cleaning
# ---------------------------------------------------------------------------

def clean_victim_age(df: pd.DataFrame) -> pd.DataFrame:
    """Replace invalid (<=0) victim ages with the median age."""
    if "Vict Age" not in df.columns:
        return df
    df["Vict Age"] = pd.to_numeric(df["Vict Age"], errors="coerce")
    invalid_mask = df["Vict Age"] <= 0
    median_age = df.loc[~invalid_mask, "Vict Age"].median()
    count = invalid_mask.sum()
    df.loc[invalid_mask, "Vict Age"] = median_age
    if count:
        print(f"      Replaced {count:,} invalid Vict Age values with median ({median_age:.0f})")
    return df


def clean_victim_sex(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise Vict Sex; mark unexpected codes as 'X' (unknown)."""
    if "Vict Sex" not in df.columns:
        return df
    df["Vict Sex"] = df["Vict Sex"].astype(str).str.strip().str.upper()
    df.loc[~df["Vict Sex"].isin(VALID_VICT_SEX), "Vict Sex"] = "X"
    df["Vict Sex"] = df["Vict Sex"].astype("category")
    return df


def clean_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Flag and remove rows with 0.0 or out-of-bounds coordinates.

    Per the data dictionary, LAT/LON == 0.0 indicates an invalid/unknown
    location.  Rows outside the LA County bounding box are also flagged.
    Both LAT and LON are kept in the output; rows are NOT dropped so that
    non-spatial Tableau sheets still have full coverage — but a boolean
    column `valid_geo` is added so dashboards can filter easily.
    """
    if "LAT" not in df.columns or "LON" not in df.columns:
        return df

    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")

    zero_coords  = (df["LAT"] == 0.0) | (df["LON"] == 0.0)
    out_of_bounds = (
        (df["LAT"] < LA_LAT_MIN) | (df["LAT"] > LA_LAT_MAX) |
        (df["LON"] < LA_LON_MIN) | (df["LON"] > LA_LON_MAX)
    )
    df["valid_geo"] = (~zero_coords & ~out_of_bounds)
    invalid_count = (~df["valid_geo"]).sum()
    print(f"      Flagged {invalid_count:,} rows with invalid/out-of-bounds coordinates (valid_geo=False)")
    return df


def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from all object/string columns."""
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string").str.strip()
    return df


# ---------------------------------------------------------------------------
# Step 6 – Derived analytical features
# ---------------------------------------------------------------------------

def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    """Bucket Vict Age into labelled age groups matching notebook logic."""
    if "Vict Age" not in df.columns:
        return df
    df["Age Group"] = pd.cut(
        df["Vict Age"],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        right=True,
    )
    return df


def add_is_violent(df: pd.DataFrame) -> pd.DataFrame:
    """Binary flag: 1 if Crm Cd Desc contains a violent-crime keyword."""
    if "Crm Cd Desc" not in df.columns:
        return df
    pattern = "|".join(VIOLENT_CRIME_KEYWORDS)
    df["is_violent"] = (
        df["Crm Cd Desc"]
        .astype(str)
        .str.upper()
        .str.contains(pattern, regex=True, na=False)
        .astype(int)
    )
    violent_pct = df["is_violent"].mean() * 100
    print(f"      is_violent flag: {violent_pct:.1f}% of incidents marked violent")
    return df


# ---------------------------------------------------------------------------
# Step 7 – Data quality report
# ---------------------------------------------------------------------------

def print_quality_report(df: pd.DataFrame, output_path: Path) -> None:
    """Print a concise data quality summary to stdout."""
    print("\n" + "=" * 60)
    print("  DATA QUALITY REPORT")
    print("=" * 60)
    print(f"  Output file     : {output_path}")
    print(f"  Final shape     : {len(df):,} rows × {len(df.columns)} columns")

    if "DATE OCC" in df.columns:
        valid_dates = df["DATE OCC"].dropna()
        print(f"  Date range      : {valid_dates.min().date()} → {valid_dates.max().date()}")

    if "year" in df.columns:
        years = sorted(df["year"].dropna().unique().astype(int))
        print(f"  Years covered   : {years}")

    if "Crm Cd Desc" in df.columns:
        n_types = df["Crm Cd Desc"].nunique()
        top5 = df["Crm Cd Desc"].value_counts().head(5)
        print(f"  Unique crime types : {n_types}")
        print("  Top 5 crime types  :")
        for desc, cnt in top5.items():
            print(f"      {cnt:>7,}  {desc}")

    if "AREA NAME" in df.columns:
        print(f"  LAPD areas      : {df['AREA NAME'].nunique()} unique")

    if "valid_geo" in df.columns:
        valid_pct = df["valid_geo"].mean() * 100
        print(f"  Valid coordinates : {valid_pct:.1f}% of rows")

    null_summary = df.isnull().sum()
    null_summary = null_summary[null_summary > 0].sort_values(ascending=False)
    if not null_summary.empty:
        print("  Columns with nulls :")
        for col, n in null_summary.items():
            print(f"      {col:<25} {n:>8,} nulls")
    else:
        print("  Null values     : none")

    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def build_clean_dataset(input_path: Path) -> pd.DataFrame:
    """Run all ETL steps and return the cleaned, enriched DataFrame."""
    df = load_raw(input_path)

    print("[2/7] Cleaning columns and dropping sparse fields...")
    df = normalize_columns(df)
    df = drop_sparse_columns(df)

    print("[3/7] Parsing dates and adding temporal features...")
    df = parse_dates(df)
    df = add_temporal_features(df)

    print("[4/7] Deduplicating on DR_NO...")
    df = deduplicate(df)

    print("[5/7] Cleaning field values...")
    df = clean_victim_age(df)
    df = clean_victim_sex(df)
    df = clean_coordinates(df)
    df = clean_string_columns(df)

    print("[6/7] Adding derived features (Age Group, is_violent)...")
    df = add_age_group(df)
    df = add_is_violent(df)

    return df


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    """Write the cleaned DataFrame to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[7/7] Saved processed dataset → {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ETL pipeline for LA Crime dataset (DVA Capstone 2, Group 15)."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to raw CSV, e.g. data/raw/crime_dataset.csv",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path for cleaned output, e.g. data/processed/crime_dataset_clean.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    cleaned_df = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)
    print_quality_report(cleaned_df, args.output)


if __name__ == "__main__":
    main()