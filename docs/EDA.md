# Exploratory Data Analysis (EDA) Documentation
## Notebook: `03_eda.ipynb`
**Project:** Factors Affecting Crime — Optimizing Law Enforcement Resource Allocation
**Team:** Section A - Group 15 | Newton School of Technology

---

## Overview

EDA (Exploratory Data Analysis) is the process of visually and statistically exploring the cleaned dataset to discover patterns, trends, and relationships before applying formal statistical tests.

| Attribute | Detail |
|---|---|
| **Input File** | `data/processed/crime_dataset_clean.csv` |
| **Rows Analyzed** | 271,673 |
| **Columns** | 24 (+ 4 derived) |
| **Libraries Used** | `pandas`, `numpy`, `seaborn`, `matplotlib` |

---

## Why EDA is Necessary

> **"Look before you leap"** — Before applying statistical tests or ML models, we must understand the data visually.

EDA helps us:
- Discover patterns (when/where does crime peak?)
- Identify outliers and anomalies
- Understand distributions of key variables
- Form hypotheses for statistical testing
- Decide which features to use in ML models

---

## Derived Columns Added

Before analysis, 4 new columns were extracted from existing fields:

```python
df['hour']  = pd.to_datetime(df['TIME OCC'], format='%H:%M:%S').dt.hour
df['day']   = df['DATE OCC'].dt.day_name()
df['month'] = df['DATE OCC'].dt.month
df['year']  = df['DATE OCC'].dt.year
```

| New Column | Source | Values | Purpose |
|---|---|---|---|
| `hour` | `TIME OCC` | 0–23 | Peak hour analysis |
| `day` | `DATE OCC` | Monday–Sunday | Day-of-week analysis |
| `month` | `DATE OCC` | 1–12 | Monthly trend analysis |
| `year` | `DATE OCC` | 2020–2024 | Yearly trend analysis |

---

## Data Overview

### Dataset Shape
```
(271,673 rows × 28 columns including derived)
```

### Case Status Distribution
```python
df['Status Desc'].value_counts()
```

| Status | Count | Meaning |
|---|---|---|
| **Invest Cont** | 66,291 | Case still under investigation (Pending) |
| **Adult Other** | 29,824 | Adult involved — other outcome |
| **Adult Arrest** | 20,918 | Adult arrested |
| **Juv Arrest** | 865 | Juvenile arrested |
| **Juv Other** | 410 | Juvenile — other outcome |

> **Key Finding:** 56% of cases are still pending — a major resolution crisis.

---

## Part 1 — Univariate Analysis

*Analyzing one variable at a time to understand its distribution.*

---

### Analysis 1 — Crime Frequency by Hour

```python
sns.countplot(x='hour', data=df)
plt.title("Crime Frequency by Hour")
```

**Chart Type:** Bar chart (X = Hour 0–23, Y = Crime Count)

**Finding:**
- Crime gradually increases from morning
- **Sharp peak at Hour 20 (8 PM) — 18,765 incidents**
- Drops sharply after 8 PM
- Lowest crime at 5–6 AM

| Hour | Crime Count | Note |
|---|---|---|
| 20 (8 PM) | 18,765 | **PEAK — 5.75% of all crime** |
| 12 (Noon) | ~14,000 | Secondary peak |
| 5 AM | ~3,000 | Lowest |

> **Business Insight:** Deploy extra patrol units at 8 PM in high-risk areas.

---

### Analysis 2 — Crime by Day of Week

```python
order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
sns.countplot(x='day', data=df, order=order)
plt.title("Crime by Day of Week")
```

**Chart Type:** Bar chart (X = Day, Y = Crime Count)

**Finding:**
- Crime is relatively consistent across weekdays
- **Friday has the highest crime count**
- **Saturday and Sunday together = 31.29% of all crime**
- Expected baseline = 28.6% (2 out of 7 days)
- Weekend crime is **disproportionately higher** than expected

> **Business Insight:** Weekend patrol strength should exceed weekday levels in hotspot divisions.

---

### Analysis 3 — Crime by Month

```python
sns.countplot(x='month', data=df)
plt.title("Crime by Month")
```

**Chart Type:** Bar chart (X = Month 1–12, Y = Crime Count)

**Finding:**
- Crime shows a **Q3 seasonal peak (July–September)**
- July and August consistently highest months
- December lowest (partly due to partial 2024 data)
- Stable band of 4,500–6,000 incidents per month

> **Business Insight:** Pre-position additional units every summer (July–September).

---

### Analysis 4 — Crime by Year

```python
sns.countplot(x='year', data=df)
plt.title("Crime by Year")
```

**Chart Type:** Bar chart (X = Year, Y = Crime Count)

**Finding:**
- Crime relatively stable 2020–2023
- **2022–2023 shows highest annual volume**
- 2024 appears lower (partial year data — December 2024 incomplete)

---

## Part 2 — Bivariate Analysis

*Analyzing two variables together to find relationships.*

---

### Analysis 5 — Crime Type Distribution (Top Crimes)

```python
df['Crm Cd Desc'].value_counts().head(10)
```

**Top 10 Crime Types:**

| Rank | Crime Type | Count |
|---|---|---|
| 1 | **Battery - Simple Assault** | 74,704 |
| 2 | **Assault with Deadly Weapon** | 53,451 |
| 3 | **Intimate Partner - Simple Assault** | 46,583 |
| 4 | Theft of Identity | ~30,000 |
| 5 | Robbery | ~25,000 |
| 6 | Burglary | ~20,000 |
| 7 | Vehicle Theft | ~18,000 |
| 8 | Vandalism | ~15,000 |
| 9 | Attempted Robbery | ~12,000 |
| 10 | Criminal Threats | ~10,000 |

> **Key Finding:** Top 3 crime types are all assault-linked = **46.1% Violent Crime Ratio**
> Top 3 alone account for **55%+ of all incidents**

---

### Analysis 6 — Area-wise Crime (LAPD Divisions)

```python
df['AREA NAME'].value_counts()
```

**Top 5 High-Risk Areas:**

| Rank | Area | Crime Count | % of Total |
|---|---|---|---|
| 1 | **77th Street** | 24,124 | 8.87% |
| 2 | **Central** | 20,291 | 7.47% |
| 3 | Southeast | 19,378 | 7.13% |
| 4 | Southwest | 17,275 | 6.36% |
| 5 | Hollywood | 16,033 | 5.90% |

**Top 5 Low-Risk Areas:**

| Rank | Area | Crime Count | % of Total |
|---|---|---|---|
| 17 | Topanga | ~10,916 | 3.35% |
| 18 | Northeast | ~10,553 | 3.23% |
| 19 | Foothill | ~10,505 | 3.22% |
| 20 | Devonshire | ~10,460 | 3.21% |
| 21 | **West LA** | ~10,203 | 3.13% |

> **Key Finding:** 77th Street + Central together = nearly **1/5 of all citywide crime**
> These 2 divisions alone outpace the combined total of the bottom 10 divisions.

---

### Analysis 7 — Victim Age Distribution

```python
df['Vict Age'].hist(bins=30)
plt.title("Victim Age Distribution")
```

**Chart Type:** Histogram (X = Age, Y = Count)

**Finding:**
- Sharp spike at ages **25–35**
- Sustained high-risk plateau from **35–49** (111,000+ incidents)
- Mean victim age = **38.12 years**
- Median victim age = **35 years**
- Elderly victims (65+) = relatively low count

> **Business Insight:** Community safety programs should target working-age adults (35–49) in high-risk divisions.

---

### Analysis 8 — Victim Sex Distribution

```python
df['Vict Sex'].value_counts()
```

| Sex | Count |
|---|---|
| **Male (M)** | 137,741 |
| Female (F) | ~110,000 |
| Unknown (X) | ~20,000 |

> **Key Finding:** Male victims slightly outnumber female victims.

---

### Analysis 9 — Victim Descent Distribution

```python
df['Vict Descent'].value_counts()
```

| Code | Descent | Count |
|---|---|---|
| H | **Hispanic** | Largest group |
| B | **Black** | Second largest |
| W | White | Third |
| O | Other | Fourth |
| X | Unknown | Fifth |

> **Key Finding:** Hispanic and Black descent categories represent the largest victim demographic groups.

---

### Analysis 10 — Crime Premises (Where Crime Happens)

```python
df['Premis Desc'].value_counts().head(10)
```

**Top Crime Locations:**

| Rank | Premise | Note |
|---|---|---|
| 1 | **Street** | Highest volume outdoor location |
| 2 | **Single Family Dwelling** | Highest indoor location |
| 3 | Multi-Unit Dwelling | Apartments/flats |
| 4 | **Sidewalk** | Public outdoor |
| 5 | **Parking Lot** | Vehicle-related crimes |
| 6 | Other Business | Commercial |
| 7 | Restaurant/Fast Food | Public indoor |
| 8 | Alley | Outdoor |

> **Business Insight:** Visible vehicle patrols on streets and parking lots = highest-leverage deterrence tool.

---

## Key EDA Findings Summary

| Finding | Value | Business Implication |
|---|---|---|
| **Peak Crime Hour** | 8 PM (20:00) | Surge deployment at 8 PM |
| **Peak Crime Day** | Friday/Weekend | Weekend patrol increase |
| **Peak Crime Season** | July–September (Q3) | Summer surge planning |
| **#1 High-Risk Area** | 77th Street (24,124) | Priority patrol zone |
| **#2 High-Risk Area** | Central (20,291) | Priority patrol zone |
| **Most Common Crime** | Battery - Simple Assault | Physical response units needed |
| **Violent Crime Ratio** | 46.1% | Assault-focused response |
| **Most Affected Age** | 35–49 years | Community programs |
| **Most Affected Gender** | Male (137,741) | — |
| **Primary Crime Location** | Street/Sidewalk | Vehicle patrols |
| **Cases Pending** | 57.11% | Case triage urgently needed |
| **Resolution Rate** | 17.47% | Investigative crisis |

---

## EDA → Statistical Analysis Connection

EDA findings form the **hypotheses** that are tested in `04_statistical_analysis.ipynb`:

| EDA Observation | Statistical Test Used | Result |
|---|---|---|
| Crime type varies by area | Chi-Square Test | p = 0.0000 ✅ Confirmed |
| Crime type varies by hour | Chi-Square Test | p = 0.0000 ✅ Confirmed |
| Victim age differs by crime type | ANOVA | p = 0.0000 ✅ Confirmed |
| Violent victims are younger | T-Test | p = 0.0000 ✅ Confirmed |
| Jan 1 looks like an outlier | Z-Score Analysis | Z = 4.57 ✅ Confirmed |

---

## Charts Produced in This Notebook

| Chart | Type | Key Finding |
|---|---|---|
| Crime Frequency by Hour | Bar Chart | 8 PM peak |
| Crime by Day of Week | Bar Chart | Friday highest |
| Crime by Month | Bar Chart | July–August peak |
| Crime by Year | Bar Chart | 2022–2023 highest |
| Victim Age Distribution | Histogram | 35–49 most affected |
| Top Crime Types | Bar Chart | Battery #1 |
| Area-wise Crime | Bar Chart | 77th Street #1 |
| Crime Premises | Bar Chart | Street #1 |

---

*Section A - Group 15 | Newton School of Technology | April 2026*
