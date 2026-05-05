# Data Cleaning Documentation
## Notebook: `02_cleaning.ipynb`
**Project:** Factors Affecting Crime — Optimizing Law Enforcement Resource Allocation
**Team:** Section A - Group 15 | Newton School of Technology

---

## Overview

The cleaning stage transforms the raw LAPD Crime Incidents dataset into a high-fidelity, analysis-ready file.

| Attribute | Before Cleaning | After Cleaning |
|---|---|---|
| **Rows** | 1,004,894 | 271,673 |
| **Columns** | 28 | 24 |
| **File** | `data/raw/crime_dataset.csv` | `data/processed/crime_dataset_clean.csv` |

---

## Why Cleaning is Necessary

Raw data is never perfect. Issues found in this dataset:
- Date and time fields stored as strings — not usable for analysis
- Duplicate incident records present
- Victim Sex and Descent had `NaN`, `Unknown`, `UNKNOWN` values
- 4 columns had >80% missing values — useless for analysis
- Some victim ages were `0` or negative — impossible values
- Rows with missing critical fields needed to be removed

> **"Garbage in, Garbage out"** — dirty data produces wrong results.

---

## Cleaning Steps (7 Steps)

---

### Step 1 — Date/Time Standardization

**Problem:** `DATE OCC` and `Date Rptd` were stored as strings like `"10/21/2020 12:00:00 AM"`. `TIME OCC` was stored as an integer like `1845`.

**Action:**
```python
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], format='%m/%d/%Y %I:%M:%S %p').dt.date
df['DATE OCC']  = pd.to_datetime(df['DATE OCC'],  format='%m/%d/%Y %I:%M:%S %p').dt.date

df['TIME OCC'] = (
    df['TIME OCC'].astype(str).str.zfill(4)
    .str.slice(0, 2) + ':' +
    df['TIME OCC'].astype(str).str.zfill(4).str.slice(2, 4)
)
df['TIME OCC'] = pd.to_datetime(df['TIME OCC'], format='%H:%M').dt.time
```

**Result:** `1845` → `18:45:00` | Consistent datetime types across all records.

---

### Step 2 — Deduplication

**Problem:** Same crime incident could appear multiple times in the raw data.

**Action:**
```python
df = df.drop_duplicates(subset=['DR_NO'])
print(f"Duplicates removed. Current row count: {len(df)}")
```

**Key:** `DR_NO` (Division of Records Number) is the unique identifier for each crime incident.

**Result:** No duplicate incident records in the final dataset.

---

### Step 3 — Victim Sex & Descent Normalization

**Problem:** `Vict Sex` and `Vict Descent` columns had `NaN`, `"Unknown"`, `"UNKNOWN"` values — inconsistent categories.

**Action:**
```python
target_cols = ['Vict Sex', 'Vict Descent']
for col in target_cols:
    df[col] = df[col].fillna('X')
    df[col] = df[col].replace(['Unknown', 'UNKNOWN', 'unknown'], 'X')
```

**Result:** All null/unknown values replaced with `'X'` (standard unknown code). Clean, consistent categorical fields.

**Valid Vict Sex codes after cleaning:**
| Code | Meaning |
|---|---|
| F | Female |
| M | Male |
| X | Unknown |
| H | Other |

---

### Step 4 — Sparse Column Removal

**Problem:** 4 columns had >80% missing values — they add no analytical value.

**Columns Dropped:**
| Column | Reason |
|---|---|
| `Crm Cd 2` | >80% missing — secondary crime code rarely recorded |
| `Crm Cd 3` | >80% missing — tertiary crime code rarely recorded |
| `Crm Cd 4` | >80% missing — quaternary crime code rarely recorded |
| `Cross Street` | >80% missing — cross street rarely recorded |

**Action:**
```python
df = df.drop(columns=['Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Cross Street'])
```

**Result:** Column count reduced from **28 → 24**.

---

### Step 5 — Victim Age Imputation

**Problem:** Some records had `Vict Age <= 0` — impossible values (0 or negative age).

**Action:**
```python
median_age = df.loc[df['Vict Age'] > 0, 'Vict Age'].median()  # = 35
df.loc[df['Vict Age'] <= 0, 'Vict Age'] = median_age
```

**Records corrected:** 26,084

**Why median and not mean?**
Median is more robust to outliers. If we used mean, extreme ages (e.g., 120 years) would skew the replacement value.

**Result:** Valid age range maintained throughout dataset. No more impossible age values.

---

### Step 6 — Missing Value Removal

**Problem:** After column pruning and targeted fixes, some rows still had missing values in critical fields.

**Action:**
```python
df = df.dropna()
```

**Result:** Row count reduced from **1,004,894 → 271,673** (high-fidelity records only).

> Note: The large reduction is primarily due to rows missing LAT/LON coordinates and other critical fields.

---

### Step 7 — Export Clean Dataset

**Action:**
```python
df.to_csv('crime_dataset_clean.csv', index=False)
```

**Output file:** `data/processed/crime_dataset_clean.csv`

---

## Final Dataset Summary

| Attribute | Value |
|---|---|
| **Total Rows** | 271,673 |
| **Total Columns** | 24 |
| **Date Range** | January 1, 2020 – December 30, 2024 |
| **Duplicate Records** | 0 |
| **Invalid Ages** | 0 |
| **Null Values** | 0 (in retained columns) |

---

## Final 24 Columns

| Column | Type | Description |
|---|---|---|
| `DR_NO` | int64 | Unique crime report number |
| `Date Rptd` | date | Date crime was reported |
| `DATE OCC` | date | Date crime occurred |
| `TIME OCC` | time | Time of occurrence (HH:MM:SS) |
| `AREA` | int64 | LAPD area/division code |
| `AREA NAME` | str | LAPD division name |
| `Rpt Dist No` | int64 | Reporting district number |
| `Part 1-2` | int64 | Crime severity (1=serious, 2=less serious) |
| `Crm Cd` | int64 | Crime code |
| `Crm Cd Desc` | str | Crime type description |
| `Mocodes` | str | Modus Operandi codes |
| `Vict Age` | int64 | Victim age (invalid values replaced with 35) |
| `Vict Sex` | str | Victim sex (F/M/X/H) |
| `Vict Descent` | str | Victim ethnicity code |
| `Premis Cd` | float64 | Premise type code |
| `Premis Desc` | str | Premise description |
| `Weapon Used Cd` | float64 | Weapon code |
| `Weapon Desc` | str | Weapon description |
| `Status` | str | Case status code |
| `Status Desc` | str | Case status description |
| `Crm Cd 1` | float64 | Primary crime code |
| `LOCATION` | str | Street address of incident |
| `LAT` | float64 | Latitude coordinate |
| `LON` | float64 | Longitude coordinate |

---

## Cleaning Summary Table

| Step | Action | Before | After |
|---|---|---|---|
| Date/Time | Convert to proper formats | String | datetime/time |
| Deduplication | Drop duplicates on DR_NO | Possible duplicates | 0 duplicates |
| Normalization | Unknown → 'X' | NaN/Unknown | X |
| Column Pruning | Drop 4 sparse columns | 28 columns | 24 columns |
| Age Imputation | Invalid ages → median (35) | 26,084 invalid | 0 invalid |
| Missing Values | dropna() | 1,004,894 rows | 271,673 rows |
| **Final Export** | **Save clean CSV** | **Raw data** | **Clean data** |

---

*Section A - Group 15 | Newton School of Technology | April 2026*
