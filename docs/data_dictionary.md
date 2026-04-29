# Data Dictionary - Los Angeles Crime Analysis Dataset

> **Version:** 1.0 | **Prepared by:** Section A, Group 15 | **Last Updated:** 28 April 2026 

---

## Dataset Summary

| Item | Details |
| --- | --- |
| **Project** | Factors Affecting Crime |
| **Primary Dataset Name** | LA Crime Incidents (Cleaned) |
| **Canonical File** | `data/processed/crime_dataset_clean.csv` |
| **Raw Source (Referenced in notebooks)** | `crime_dataset.csv` (`/content/crime_dataset.csv` in notebook runtime) |
| **Granularity** | One row per crime incident report |
| **Processed Shape** | 326,327 rows x 24 columns |
| **Primary Identifier** | `DR_NO` |
| **Core Time Fields** | `Date Rptd`, `DATE OCC`, `TIME OCC` |
| **Core Geography Fields** | `AREA`, `AREA NAME`, `Rpt Dist No`, `LOCATION`, `LAT`, `LON` |
| **Core Labeling Fields** | `Crm Cd`, `Crm Cd Desc`, `Part 1-2`, `Status`, `Status Desc` |
| **Pipeline Notebooks** | `notebooks/01_extraction.ipynb` -> `notebooks/02_cleaning.ipynb` -> `notebooks/eda.ipynb` -> `notebooks/Statistical_analysis.ipynb` -> `notebooks/final_load_prep.ipynb` |

---

## Data Flow and Lineage

1. **Extraction (`01_extraction.ipynb`)**  
   Loads raw incident file (`crime_dataset.csv`) and inspects initial shape/schema.

2. **Cleaning (`02_cleaning.ipynb`)**  
   Converts date/time fields, removes duplicates, standardizes unknown categories, handles invalid ages, drops high-missingness columns, and exports a cleaned CSV in notebook runtime.

3. **EDA and Statistical Analysis (`eda.ipynb`, `Statistical_analysis.ipynb`)**  
   Uses cleaned data to create derived temporal and victim-segmentation features (`hour`, `day`, `month`, `year`, `Age Group`), aggregate trend tables, and train/evaluate statistical/ML models.

4. **Final Prepared Analysis (`final_load_prep.ipynb`)**  
   Produces aggregated tables (monthly and YoY trends) for downstream reporting/dashboard use.

---

## Column Definitions (Canonical Processed Dataset)

### Incident Identity and Time

| Column Name | Data Type | Description | Example Value | Notes |
| --- | --- | --- | --- | --- |
| `DR_NO` | int64 (identifier) | Unique crime report number for an incident record. | `201516622` | Treated as record identifier; expected unique in cleaned data. |
| `Date Rptd` | date | Date when the incident was officially reported. | `2020-10-21` | Not always equal to occurrence date. |
| `DATE OCC` | date | Date when the crime occurred. | `2020-10-18` | Used for daily/monthly trend analysis. |
| `TIME OCC` | time | Time of occurrence in `HH:MM:SS` format. | `18:45:00` | Often transformed to numeric `hour` in notebooks. |

### Location and Jurisdiction

| Column Name | Data Type | Description | Example Value | Notes |
| --- | --- | --- | --- | --- |
| `AREA` | int64 | Numeric LAPD area/division code. | `15` | Observed range corresponds to LAPD area partitions. |
| `AREA NAME` | category/string | Human-readable LAPD area name. | `N Hollywood` | Used in area-wise frequency comparisons and maps. |
| `Rpt Dist No` | int64 | Reporting district number within area. | `1521` | Finer-grain jurisdiction than `AREA`. |
| `LOCATION` | string | Street/location text associated with the incident. | `ATOLL AV` | Free-text formatted field; spacing may vary. |
| `LAT` | float64 | Latitude coordinate of incident location. | `34.1993` | Contains `0.0` values in dataset; may indicate invalid/unknown coordinates. |
| `LON` | float64 | Longitude coordinate of incident location. | `-118.4203` | Contains `0.0` values in dataset; check before spatial modeling. |

### Crime Classification

| Column Name | Data Type | Description | Example Value | Notes |
| --- | --- | --- | --- | --- |
| `Part 1-2` | int64 (categorical numeric) | Broad legal severity grouping (Part I / Part II). | `1` | Observed values: `1`, `2`. |
| `Crm Cd` | int64 | LAPD crime code for incident offense type. | `230` | Linked to text label in `Crm Cd Desc`. |
| `Crm Cd Desc` | category/string | Crime description associated with `Crm Cd`. | `ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT` | Used as target class in multiclass modeling (top categories subset). |
| `Crm Cd 1` | float64/int-like | Primary crime code field retained after cleaning. | `230.0` | Auxiliary coding field; semantically close to `Crm Cd`. |
| `Mocodes` | string | Modus Operandi code sequence for incident behavior pattern. | `0416 0334 2004 ...` | High-cardinality coded text; often requires parsing for advanced analysis. |

### Victim Attributes

| Column Name | Data Type | Description | Example Value | Notes |
| --- | --- | --- | --- | --- |
| `Vict Age` | int64 | Victim age in years. | `32` | Cleaning notebook replaces invalid non-positive ages with median value. |
| `Vict Sex` | category/string | Victim sex code. | `M` | Observed values include `F`, `M`, `X`, `H`. |
| `Vict Descent` | category/string | Victim descent/ethnicity code. | `H` | Observed codes include `A,B,C,D,F,G,H,I,J,K,L,O,P,S,U,V,W,X,Z`. |

### Premise, Weapon, and Case Status

| Column Name | Data Type | Description | Example Value | Notes |
| --- | --- | --- | --- | --- |
| `Premis Cd` | float64/int-like | Premise type code where incident occurred. | `102.0` | Mapped to text via `Premis Desc`. |
| `Premis Desc` | category/string | Premise description. | `SIDEWALK` | High-cardinality location category. |
| `Weapon Used Cd` | float64/int-like | Weapon code associated with incident. | `200.0` | Includes generic/unknown weapon categories. |
| `Weapon Desc` | category/string | Weapon description label. | `KNIFE WITH BLADE 6INCHES OR LESS` | Retained as descriptive categorical feature. |
| `Status` | category/string | Short status code for case disposition. | `IC` | Observed values include `AA`, `AO`, `CC`, `IC`, `JA`, `JO`. |
| `Status Desc` | category/string | Full text for status code. | `Invest Cont` | Includes categories such as `Adult Arrest`, `Juv Arrest`, `UNK`. |

---

## Referenced but Dropped Columns (Cleaning Stage)

The raw notebook schema includes additional sparse columns that are not present in the final canonical processed file:

| Raw Column | Typical Role | Cleaning Treatment (as indicated in notebooks) |
| --- | --- | --- |
| `Crm Cd 2` | Secondary crime code | Dropped due to high missingness/sparsity |
| `Crm Cd 3` | Tertiary crime code | Dropped due to high missingness/sparsity |
| `Crm Cd 4` | Quaternary crime code | Dropped due to high missingness/sparsity |
| `Cross Street` | Cross-street descriptor | Dropped due to high missingness/sparsity |

---

## Derived Fields Used in Analysis Notebooks

These are created transiently in notebooks for analysis/modeling and are not stored as columns in `crime_dataset_clean.csv`:

| Derived Field | Source Field(s) | Transformation Logic | Primary Use |
| --- | --- | --- | --- |
| `hour` | `TIME OCC` | Extract hour from occurrence time | Temporal trend analysis; model features |
| `day` | `DATE OCC` | Extract day-of-month | Exploratory temporal breakdown |
| `month` | `DATE OCC` | Extract month number | Monthly trend tables and seasonality |
| `year` | `DATE OCC` | Extract year | Year-over-year trend analysis |
| `Age Group` | `Vict Age` | Bucket age into ranges | Demographic segmentation and charts |
| `is_violent` | `Crm Cd Desc` | Binary flag using predefined violent-crime list | Logistic regression target |
| `Crm_Type_Encoded` | `Crm Cd Desc` | Label encoding on filtered top crime types | Multiclass classification target |
| `Ordinal_Date` | `Date` (daily aggregate) | Date converted to ordinal integer | Linear regression on crime trend |
| `Crime_Count` | aggregated `DATE OCC` | Group-by incident count per period | Time-series and anomaly analysis |
| `MoM_growth` | monthly aggregates | Month-over-month rate change | Trend KPI |
| `YoY_growth` | monthly + previous-year aggregates | Year-over-year rate change | Trend KPI |
| `Z_Score` | daily `Crime_Count` | Standard-score normalization | Daily anomaly detection |

---

## Data Quality and Cleaning Notes

### Missingness and Null Handling

- The canonical processed dataset appears fully populated at the CSV level for its 24 retained columns.
- Notebook cleaning indicates explicit `dropna()` after major cleanup steps; this reduces row count and removes records with unresolved missing values.
- Sparse auxiliary fields (`Crm Cd 2/3/4`, `Cross Street`) are removed rather than imputed.

### Duplicates

- Cleaning workflow removes duplicate incidents using `DR_NO` as de-duplication key.
- This supports one-record-per-incident consistency in the final dataset.

### Category Standardization

- Unknown or inconsistent category markers in victim attributes are normalized (especially in `Vict Sex` and `Vict Descent`).
- Final observed categories include compact code-based representations.

### Outlier and Validity Handling

- Invalid victim ages (`<= 0`) are replaced with median age during cleaning.
- Coordinate fields retain `0.0` values in canonical CSV; these should be treated cautiously in spatial analysis as potential invalid placeholders.

---

## Modeling and Analytical Usage Notes

### Features Frequently Used for Modeling

- `Vict Age`, `hour`, `LAT`, `LON` are repeatedly used as baseline predictive features in notebook experiments.
- `Crm Cd Desc` is used both as descriptive label and transformed modeling target.

### Targets Used in Notebook Models

- **Binary classification target:** `is_violent`
- **Multiclass target:** `Crm_Type_Encoded` (top crime categories subset)
- **Regression target:** aggregated `Crime_Count` over time
