Cleaning and Normalization report

> End‑to‑end pipeline to load a user dataset, assess data quality, engineer age groups, remove outliers iteratively (IQR), compute descriptive statistics, generate SVG visualizations, and render a final HTML report via Jinja2.

---

## Table of Contents

- [Overview](#overview)
- [Stack and Libraries](#stack-and-libraries)
- [Requirements and Installation](#requirements-and-installation)
- [File Structure](#file-structure)
- [Execution](#execution)
- [Inputs and Outputs](#inputs-and-outputs)
- [Dataset Assumptions](#dataset-assumptions)
- [Process Flow](#process-flow)
- [Script API (Functions)](#script-api-functions)
- [Report Template (Jinja2)](#report-template-jinja2)
- [Visualizations Generated](#visualizations-generated)


---

## Overview

This project provides a reproducible workflow to:

1. **Load** a CSV dataset.
2. **Assess data quality** (schema info, null counts, duplicate rows).
3. **Engineer age groups** (10‑year bins).
4. **Remove outliers iteratively** on `total_watch_time_hours` using the **IQR** rule.
5. **Summarize numerically** (`age`, `total_watch_time_hours`) with mean, median, mode, range, variance, std. dev., CV, and quantiles.
6. **Visualize** distributions and category counts (SVG).
7. **Render** a self‑contained **HTML report** using **Jinja2** (`report.html`).

---

## Stack and Libraries

| Library | Purpose |
|---|---|
| **pandas** | CSV I/O, data wrangling, descriptive stats, HTML tables |
| **matplotlib.pyplot** | Figure handling and saving images |
| **seaborn** | Bar charts, histograms, boxplots |
| **Jinja2** | HTML templating for the final report |
| **os** | Paths and filesystem operations |
| **io** / **sys** | Capturing `DataFrame.info()` output into strings |


---

## Requirements and Installation

Suggested `requirements.txt`:

```txt
pandas>=2.0.0
matplotlib>=3.7
seaborn>=0.12
Jinja2>=3.1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## File Structure

```
.
├── users.csv                     # Input dataset (expected)
├── template.html                 # Jinja2 template (provided)
├── script.py                     # Your Python script
├── report.html                   # (generated)
├── plot_country.svg              # (generated)
├── plot_subscription.svg         # (generated)
├── plot_age_original.svg         # (generated)
├── plot_watch_time_original.svg  # (generated)
├── plot_age_cleaned.svg          # (generated)
└── plot_watch_time_cleaned.svg   # (generated)
```

---

## Execution

From the project root:

```bash
python script.py
```

- If the CSV path is wrong or missing, the loader returns:
  `Error: The file 'users.csv' was not found.`
- On success, the script prints that the report and SVGs were generated and also writes two CSVs with and without outliers.

---

## Inputs and Outputs

**Input**

- `users.csv` – must include at least: `age`, `total_watch_time_hours`, `subscription_type`, `country`.

**Outputs**

- **HTML report**: `report.html` (rendered via `template.html`).
- **SVG charts**: country counts, subscription counts, age/watch time (original & cleaned).
- **Data CSVs**:
  - `df_users_normal.csv` – data after removing outliers.
  - `df_users_outlier.csv` – rows identified as outliers.

---

## Dataset Assumptions

- `age` is numeric and non‑negative.
- `total_watch_time_hours` is numeric (continuous) and suitable for IQR outlier detection.
- `subscription_type` and `country` are categorical (strings).
- The CSV has a header row and uses a comma delimiter (customize `pd.read_csv` if needed).

---

## Process Flow

1. **Load & summarize** → `load_and_summarize_data('users.csv')`.
2. **Quality analysis** → `analyze_data_quality(df)`:
   - captures `df.info()`,
   - null counts,
   - duplicate row count.
3. **Age groups** → `create_age_groups(df)`:
   - 10‑year bins with labels like `1-10 years`, `11-20 years`, …
4. **Outlier cleaning (IQR)** → `handle_outliers_iteratively(df, "total_watch_time_hours")`.
5. **Stats (original & cleaned)** → `analyze_numerical_summary(...)` for `age` and `total_watch_time_hours`.
6. **Visualizations** → barplots, histograms, boxplots (saved as SVG).
7. **Report render** → `generate_report(report_data, '.')` with Jinja2 template.

---

## Script API

### `load_and_summarize_data(file_path: str) -> tuple[pd.DataFrame|None, str]`
Reads a CSV and returns `(DataFrame, status_message)`. Handles `FileNotFoundError` gracefully.

---

### `analyze_data_quality(dataframe) `
Returns a dict with:
- `info`: textual output of `dataframe.info()`,
- `null_values`: per‑column null counts (string),
- `duplicate_rows`: number of duplicated rows.

---

### `analyze_numerical_summary(dataframe, columns: list[str])` 
For each numeric column in `columns`, computes:
- `mean`, `median`, `mode` (as string), `range`, `variance`, `std_dev`,
- `cv` (coefficient of variation = std / mean),
- `quantiles` at 25%, 50%, 75% (as string).

---

### `create_age_groups(dataframe) -> tuple[pd.DataFrame, str]`
Adds `age_group` using 10‑year bins and returns the modified DataFrame plus the age‑group distribution (string).

---

### `handle_outliers_iteratively(dataframe, column: str) -> pd.DataFrame`
Removes outliers in `column` using the **IQR** method **iteratively** until no points fall outside `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`. Returns a filtered copy.

> Designed for continuous metrics like `total_watch_time_hours`.

---

### Plot Generators

- `generate_country_plot(df, report_path)` → `plot_country.svg`
- `generate_subscription_plot(df, report_path)` → `plot_subscription.svg`
- `generate_age_plot(df, report_path, prefix)` → `plot_age_{prefix}.svg` (histogram & boxplot)
- `generate_watch_time_plot(df, report_path, prefix)` → `plot_watch_time_{prefix}.svg` (histogram & boxplot)

---

### `generate_report(report_data: dict, report_path: str) -> None`
Creates SVG charts (original & cleaned), then renders `report.html` using `template.html` and the provided `report_data` dictionary.

---

### `main() -> None`
Orchestrates the full pipeline, saves CSVs with/without outliers, builds `report_data`, generates charts, and renders the final HTML report.

---

## Report Template (Jinja2)

The provided `template.html` expects these keys inside `report_data`:

- `load_message`, `initial_shape`, `initial_head` (HTML table)
- `subscription_counts`, `country_counts`, `quality_info` (`info`, `null_values`, `duplicate_rows`)
- `age_distribution`
- `original_stats`, `cleaned_stats` (dicts per column)
- `original_summary_table`, `cleaned_summary_table` (HTML)
- `original_rows`, `cleaned_rows`
- `df_original`, `df_cleaned` (used by plot functions prior to rendering)

**Image references inside the template** (must exist in the report directory):

- `plot_age_original.svg`, `plot_watch_time_original.svg`
- `plot_age_cleaned.svg`, `plot_watch_time_cleaned.svg`
- `plot_country.svg`, `plot_subscription.svg`

---

## Visualizations Generated

- **Category distributions**: `plot_country.svg`, `plot_subscription.svg`
- **Age** (original & cleaned): histograms + boxplots → `plot_age_original.svg`, `plot_age_cleaned.svg`
- **Total watch time** (original & cleaned): histograms + boxplots → `plot_watch_time_original.svg`, `plot_watch_time_cleaned.svg`

All figures are saved as **SVG** to keep them crisp in HTML and scalable for print.

-----------------------------------------------------------------

AI ASSISTANCE DISCLOSURE GUIDE

Estimation Methods

    Time-Based Method

Basic calculation:

AI Assistance % = (3.2 / 10) × 100

Total project time: 10 hours
Time using AI: 3.2 hours
Estimation: 32% AI assistance

    Content/Code Lines Method

For code:

AI Assistance % = (85 / 250) × 100

Total code: 250 lines
AI-generated code: 85 lines
Estimation: 34% AI assistance

For documentation:

AI Assistance % = (300 / 1200) × 100

Total documentation: 1200 words
AI-generated documentation: 300 words
Estimation: 25% AI assistance

    Project Components Method
    Component //    Weight /    AI Assistance / Contribution
    Data Cleaning   40%     35%     14%
    Data Analysis   30%     25%     7.5%
    Report Generation   30%     45%     13.5%
    TOTAL           100%     -    35%

Assistance Levels by Activity
According to the result before, my part of the project is on Level 2

Level 2: Moderate Assistance (21-50%)

Base code generation: Basic structures, templates
Guided analysis: Methodological approach suggestions
Content review: Improvements to existing documentation

Examples:

Complete AI-generated dashboard
Complete technical documentation
Automatically generated presentation

Self-Assessment Framework
Guiding Questions for Students

    Initiative and Conceptualization (Who defined WHAT to do?)

    AI helped me refine the project scope and define key functions (35%)

    Implementation (Who did the technical work?)

    AI generated code that I significantly modified and integrated into the pipeline (40%)

    Understanding and Validation (Do you understand what you did?)

    I understand and can explain every line/concept (80%)

    Problem Solving (Who solved the errors?)

    AI helped me identify problems that I solved independently (30%)

Formula:

Self-Assessment Score = (35 + 40 + 80 + 30) / 4
Self-Assessment Score = 46.25%

AI Usage Log Template
For each work session:

Session [September 20th, 2025]

Duration: 3 hours
Objectives: Initial data loading and quality assessment

AI Usage:

    Tool: Gemini

    Time with AI: 45 minutes

    Prompts used: 5

    Type of assistance:

        [ ] data cleaning process

        [ ] data missing values

Results:

    Generated by AI: 

    https://g.co/gemini/share/26f82b18102c

    Modified by me: I adapted the generated code to fit into my script's API, adding detailed docstrings and comments.

    Created by me: The overall script structure and the main function to orchestrate the pipeline.

Session [September 8th, 2025]

Duration: 4 hours
Objectives: Outlier removal (IQR) and data normalization

AI Usage:

    Tool: Gemini

    Time with AI: 2 hours

    Prompts used: 2

    Type of assistance:

          [ ] data cleaning process

        [ ] data missing values

Results:

    Generated by AI: 

    https://g.co/gemini/share/26f82b18102c

    Modified by me: I significantly modified the loop to handle edge cases, such as empty dataframes, and implemented a cleaner way to track the number of removed outliers.

    Created by me: I developed the full handle_outliers_iteratively function and the logic for creating age groups and computing descriptive statistics.

Assistance estimation for this session: 50%

BEST PRACTICE: Commit regularly and document session details in commit messages
Suggested Final Calculation
Combined Formula:

Final AI Assistance % = (0.25 × Time %) + (0.35 × Content %) + (0.25 × Complexity %) + (0.15 × Self-Assessment Score)

Where:

Time %: Proportion of time using AI
Content %: Proportion of content generated by AI
Complexity %: Complexity level of tasks performed by AI
Self-Assessment Score: Based on the Self-Assessment Framework

Practical Examples
Example: Database Project
Activity: Relational database design
Time % = (6 / 20) × 100 = 30%
Time Contribution = 0.25 × 30% = 7.5%

Content % = (200 / 500) × 100 = 40%
Content Contribution = 0.35 × 40% = 14%

Complexity Score = 62.5% (Significant level)
Complexity Contribution = 0.25 × 62.5% = 15.625%

Self-Assessment Score = (25 + 75 + 25 + 25) / 4 = 37.5%
Self-Assessment Contribution = 0.15 × 37.5% = 5.625%

Final AI Assistance % = 7.5% + 14% + 15.625% + 5.625% = 42.75%
Recommendations for Professors

    Establish Acceptable Ranges

    Learning projects: 0-30% recommended
    Intermediate projects: 31-60% acceptable
    Advanced projects: 61-80% with justification
    Research projects: Variable according to objectives

    Require Evidence

    Git control version or similar
    AI conversation history
    Detailed time log
    Explanation of modifications made

    Complementary Assessment

    Oral exams about the project
    Specific technical questions
    Request live modifications
    Peer review among students

Documentation Standards
Required AI Disclosure Elements
Basic Template:

AI Assistance Disclosure

    AI Tool Used: Gemini

    Overall Assistance Level: 33.74%

    Primary Use Cases: - Code generation: 50%

        Debugging: 30%

        Conceptual guidance: 20%

    Human Contributions:

        I designed the full end-to-end pipeline, including the script.py and the overall process flow.

        I wrote the core logic for the data quality analysis, summary statistics, and all the plot generation functions.

        I performed significant modifications to the AI-generated code to ensure it was robust and integrated seamlessly with my project.

    Verification Process: I manually tested each function with both clean and messy datasets to ensure the outputs (clean CSVs, SVGs, and the final HTML report) were correct and reproducible.

