# Factors Affecting Crime: Optimizing Law Enforcement Resource Allocation 

> **Newton School of Technology | Data Visualization & Analytics**  
> A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw LAPD crime data into actionable law enforcement intelligence.

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | Factors Affecting Crime: Optimizing Law Enforcement Resource Allocation |
| **Sector** | Public Safety & Law Enforcement |
| **Team ID** | Section A – Group 15 |
| **Section** | Section A |
| **Faculty Mentor** | Aayushi Mam & Satyaki Sir |
| **Institute** | Newton School of Technology |
| **Submission Date** | April 29, 2026 |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | Apoorva | codee-wizard |
| Data Lead | Arun Kumar | ArPriCode |
| ETL Lead | Ishan | ishan-goyal-12 |
| Analysis Lead | Divyansh | 111-DEBUG-111 |
| Visualization Lead | Nakul | Nakul-Jaglan |
| PPT & Quality Lead | Archit | ArchitCodes1204 |

---

## Business Problem

Urban law enforcement agencies face finite budgets and severe personnel constraints. Police chiefs, resource planners, and city councils cannot afford uniform, city-wide patrol distributions — deploying officers equally across unequal risk zones leads to over-patrolling safe areas while high-crime hotspots remain understaffed.

**Core Business Question**

> What factors influence crime occurrence patterns across time and location, and how can law enforcement optimize resource allocation?

**Decision Supported**

> This analysis enables shift lieutenants and resource planners to shift from reactive policing to proactive, data-driven deployment — concentrating patrol units in the right areas, at the right hours, with the right response type.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | LAPD Crime Incidents Dataset |
| **Direct Access Link** | [data/raw/crime_dataset.csv](data/raw/crime_dataset.csv) |
| **Row Count** | 271,673 (cleaned) from 1,004,894 raw |
| **Column Count** | 24 canonical columns + 7 derived features |
| **Time Period Covered** | January 1, 2020 – December 30, 2024 |
| **Format** | CSV |

### Key Columns Used

| Column Name | Description | Role in Analysis |
|---|---|---|
| `DATE OCC` | Date crime occurred | Monthly/yearly trend analysis, KPI computation |
| `TIME OCC` | Time of occurrence | Peak-hour index, time-of-day bucketing |
| `AREA NAME` | LAPD division name | Spatial concentration, hotspot identification |
| `Crm Cd Desc` | Crime type description | Category analysis, violent crime flag |
| `Vict Age` | Victim age in years | Age group segmentation, demographic KPIs |
| `Vict Sex` | Victim sex code (F/M/X/H) | Gender split dashboard filter |
| `Vict Descent` | Victim ethnicity code | Demographic breakdown |
| `LAT` / `LON` | Incident coordinates | Crime hotspot map in Tableau |
| `Status Desc` | Case disposition | Resolution rate KPI |
| `Part 1-2` | Crime severity grouping | Severity split analysis |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Value | Formula / Computation |
|---|---|---|---|
| **Total Crimes** | Total high-fidelity incident volume (2020–2024) | 271,673 | `COUNT(DR_NO)` on cleaned dataset |
| **Night Crime Ratio** | % of crimes occurring between 21:00–05:00 | 30.57% | `crimes_in_night_hours / total_crimes × 100` |
| **Peak Hour Index** | % of all crimes concentrated in the single busiest hour (20:00) | 5.75% | `crimes_at_peak_hour / total_crimes × 100` |
| **Violent Crime Ratio** | Share of assault/battery incidents vs. total | 46.1% | `is_violent==1 count / total_crimes × 100` |
| **Top 5 Area Concentration** | % of citywide crime in the 5 highest-volume divisions | 35.7% | `sum(top5_area_counts) / total_crimes × 100` |
| **Average Victim Age** | Mean age of crime victims | 38.12 years | `MEAN(Vict Age)` after median imputation |
| **Resolution Rate** | % of cases with a conclusive status (Adult/Juv Arrest or Closed) | 17.47% | `resolved_cases / total_cases × 100` |
| **Investigation Pending Rate** | % of cases still under investigation (`Invest Cont`) | 57.11% | `IC_status_count / total_cases × 100` |
| **Weekend Crime Ratio** | % of incidents occurring on Saturday or Sunday | 31.29% | `weekend_crimes / total_crimes × 100` |
| **Crime Diversity Index** | Count of unique crime types in cleaned dataset | 10 | `COUNT(DISTINCT Crm Cd Desc)` (top categories shown) |

KPI computation logic is documented in [`notebooks/04_statistical_analysis.ipynb`](notebooks/04_statistical_analysis.ipynb) and [`notebooks/05_final_load_prep.ipynb`](notebooks/05_final_load_prep.ipynb).

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | [View on Tableau Public](https://public.tableau.com/app/profile/apoorva.choudhary3398/viz/Factors_Affecting_Crime/CrimeOverviewandTrends?publish=yes) |
| **Dashboard 1 – Crime Overview & Trends** | Monthly crime trend line, peak hour heatmap (day × hour), quarterly seasonality bar, yearly volume — with KPI tiles for Total Crimes, Night Ratio, Avg Crimes per Day, Weekend Ratio |
| **Dashboard 2 – Spatial & Crime Nature** | Crime type Pareto analysis, Top 5 LAPD area bar chart, geographic hotspot map, violent ratio and crime diversity KPIs |
| **Dashboard 3 – Victim, Context & Enforcement** | Victim age histogram, victim descent × age group matrix, top premises type bar, gender split, resolution rate, investigation pending rate |
| **Main Filters** | Age Group, Crime Type, Hour of Day, Month — usable across all three dashboards |

Dashboard screenshots are stored in [`tableau/screenshots/`](tableau/screenshots/) and links are documented in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. **Crime peaks sharply at 8 PM** — incidents concentrate heavily in the 20:00 hour, accounting for 5.75% of all citywide crime. This single hour justifies a dedicated surge-deployment policy.

2. **Two precincts drive nearly a fifth of all crime** — 77th Street (24,124 incidents) and Central (20,291 incidents) together far exceed the combined volume of lower-risk divisions.

3. **Nearly 1 in 3 crimes happens at night** — the 30.57% Night Crime Ratio (21:00–05:00) confirms that graveyard-shift staffing is chronically under-resourced relative to actual demand.

4. **Assault and battery dominate the crime mix** — Battery/Simple Assault and Aggravated Assault with Deadly Weapon together represent 22.9% of all incidents, driving the 46.1% Violent Crime Ratio and dictating a need for physical response units rather than non-contact enforcement.

5. **Adults aged 35–49 face the highest victimization burden** — this cohort accounts for 111,000+ incidents, suggesting targeted community-safety programs for working-age adults are warranted in high-risk divisions.

6. **Crime is statistically non-random** — Chi-square tests confirm crime type has a statistically significant dependency on both Area (p = 0.00) and Hour (p = 0.00), validating the use of location and time as predictive deployment signals.

7. **Public streets and parking lots are the primary crime theatres** — beyond residences, these outdoor premises account for the next largest incident volumes, making visible vehicle patrols the highest-leverage deterrence tool.

8. **Only 17.47% of cases are resolved** — with 57.11% still under investigation, the department faces a case-clearance crisis; investigative resources are stretched thin across too many open cases.

9. **January 1, 2020 is a statistical anomaly** — Z-Score analysis flagged 506 crimes on this single date (Z > 4.5), confirming that automated anomaly detection can surface non-standard events requiring tactical review.

10. **A logistic regression model predicts violent crime at 61% accuracy** using only location, hour, and victim demographics — demonstrating that predictive pre-deployment is operationally viable without complex infrastructure.

11. **Crime shows seasonal Q3 concentration annually**, giving resource planners a repeatable summer-surge planning signal.

12. **Weekend crime ratio of 31.29%** is disproportionate to the 2/7 (28.6%) expected baseline, indicating weekend patrol strength should exceed weekday levels in hotspot divisions.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | 8 PM surge + 77th Street / Central concentration | Reallocate 10% of patrol units from low-risk divisions (West LA, Devonshire) to 77th Street and Central during the 19:00–21:00 window | Elevated coverage at peak risk with zero headcount increase |
| 2 | 30.57% night crime ratio | Restructure graveyard shift (21:00–05:00) staffing to match actual incident distribution rather than administrative tradition | Reduce incident-to-response time in under-patrolled night windows |
| 3 | 46.1% violent crime ratio dominated by assault/battery | Prioritize physical response units (not community liaison teams) in Part-1 hotspots; deploy de-escalation-trained officers to domestic assault clusters | Faster appropriate response, reduced officer injury risk |
| 4 | 17.47% resolution rate with 57.11% pending | Introduce case-triage protocols that fast-track high-evidence violent cases and administratively close low-probability cold cases to free investigator bandwidth | Improved clearance rate and investigator capacity |
| 5 | Chi-square confirms area + hour as significant crime predictors | Deploy the logistic regression violent-crime predictor as a shift-briefing tool so lieutenants receive a pre-shift probability map for their division | Shift from reactive dispatch to proactive positioning |

---

## Data Pipeline and Processing

The project follows a 5-stage notebook-driven pipeline:

**Stage 1 — Extraction** (`01_extraction.ipynb`): Loads the raw 1,004,894-row CSV and inspects initial schema and data quality issues.

**Stage 2 — Cleaning** (`02_cleaning.ipynb`): Converts date/time fields, deduplicates on `DR_NO`, normalizes victim attribute codes, replaces invalid ages (≤0) with median (35), drops sparse columns (`Crm Cd 2/3/4`, `Cross Street`), and exports the canonical 271,673-row cleaned file.

**Stage 3 — EDA** (`03_eda.ipynb`): Univariate and bivariate analysis across temporal, spatial, and victim dimensions; outlier detection and distribution inspection.

**Stage 4 — Statistical & ML Analysis** (`04_statistical_analysis.ipynb`): Chi-square, ANOVA, t-tests, Cramér's V, seasonal decomposition, Z-score anomaly detection, logistic regression (binary `is_violent`), Random Forest (multiclass crime type), and linear regression on aggregated crime trend.

**Stage 5 — Final KPI Prep** (`05_final_load_prep.ipynb`): Produces aggregated tables for all dashboard KPIs — volume, temporal, spatial concentration, category, and enforcement-context metrics.

The standalone ETL script ([`scripts/etl_pipeline.py`](scripts/etl_pipeline.py)) replicates the cleaning stage as a reproducible command-line pipeline:

```bash
python scripts/etl_pipeline.py \
  --input  data/raw/crime_dataset.csv \
  --output data/processed/crime_dataset_clean.csv
```

---

## Repository Structure

```text
SectionA_G15_FactorsAffectingCrime/
│
├── README.md
│
├── data/
│   ├── raw/                          # Original dataset (never edited)
│   │   └── crime_dataset.csv
│   └── processed/                    # Cleaned output from ETL pipeline
│       └── crime_dataset_clean.csv
│
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
│
├── scripts/
│   └── etl_pipeline.py              
│
├── tableau/
│   ├── screenshots/                  
│   └── dashboard_links.md           
│
├── reports/
│   ├── DVA_Capstone_Report.pdf
│   └── FactorsAffectingCrimeppt.pdf
│
├── docs/
│   └── data_dictionary.md           
│
├── DVA-oriented-Resume/
└── DVA-oriented-Portfolio/
```

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python 3 + Jupyter Notebooks | Mandatory | ETL, cleaning, EDA, statistical analysis, KPI computation |
| Google Colab | Used | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |

**Python libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `scikit-learn`

---

## Statistical & ML Methods

| Method | Purpose | Result |
|---|---|---|
| Chi-square test | Crime type dependency on Area and Hour | p = 0.00 — statistically significant |
| ANOVA / t-test | Comparative assessment across groups | Documented in `04_statistical_analysis.ipynb` |
| Cramér's V | Effect size for categorical associations | Documented in `04_statistical_analysis.ipynb` |
| Z-Score anomaly detection | Identify outlier crime-volume days | Jan 1 2020: 506 crimes, Z > 4.5 |
| Seasonal decomposition | Isolate trend, seasonality, residual | Q3 seasonal peak confirmed |
| Logistic Regression | Binary classification: `is_violent` | 61% accuracy |
| Random Forest Classifier | Multiclass: top crime type prediction | Documented in `04_statistical_analysis.ipynb` |
| Linear Regression | Aggregated crime trend over time | Ordinal date → Crime Count |

---

## Limitations

- **Reporting bias**: The dataset captures only reported incidents; systemic under-reporting in marginalized communities means true crime volume is higher than measured.
- **Contextual voids**: The analysis lacks external variables known to influence crime — live weather data, socioeconomic indicators, and city event schedules.
- **Terminal-month bias**: December 2024 shows very low counts due to partial-period data capture; naive trend comparisons should exclude this period.
- **Path inconsistency**: Some notebooks use Colab-style paths (`/content/...`); local execution requires path harmonization.
- **Missing `requirements.txt`**: A pinned dependency manifest is not yet committed; add one for full reproducibility.

---

## Contribution Matrix

| Team Member | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
|---|---|---|---|---|---|---|---|
| Apoorva (Project Lead) | Support | Support | Support | Support | Owner | Owner | Support |
| Arun Kumar | Owner | Support | Support | Support | Support | Support | Support |
| Ishan | Support | Owner | Support | Support | Support | Support | Support |
| Divyansh | Support | Support | Support | Owner | Support | Support | Support |
| Nakul | Support | Support | Support | Support | Owner | Support | Support |
| Archit | Support | Support | Support | Support | Support | Support | Owner |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead:** Apoorva | **Date:** April 29, 2026

---

## Links

| Resource | URL |
|---|---|
| GitHub Repository | [github.com/codeewizard/SectionA_G15_FactorsAffectingCrime](https://github.com/codeewizard/SectionA_G15_FactorsAffectingCrime) |
| Tableau Dashboard (Overview) | [Crime Overview & Trends](https://public.tableau.com/app/profile/apoorva.choudhary3398/viz/Factors_Affecting_Crime/CrimeOverviewandTrends?publish=yes) |
---

*Newton School of Technology — Data Visualization & Analytics | Capstone 2 | Section A, Group 15*
