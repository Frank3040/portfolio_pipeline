# Video Streaming Platform Performance Analysis

**Author(s):** Francisco Chan, Daniel Valdes, Valeria Ramirez, Rogelio Novelo, Esther Apaza, Carlos Helguera  
**Date:** September 28th, 2025  
**Course:** Visual Modeling For Information  
**Program:** Data Engineering  
**Institution:** Universidad Politécnica de Yucatán  

---

## AI Assistance Disclosure

This document was created with assistance from AI tools. The following outlines the nature and extent of AI involvement:

- **AI Tool Used:** ChatGPT  
- **Type of Assistance:** Documentation writing, formatting, structuring README content  
- **Extent of Use:** Moderate assistance in drafting and organizing sections, placeholders for incomplete phases were replaced with actual content based on project files and analysis scripts  
- **Human Contribution:** The team provided all project information, selected objectives, and guided the scope. All technical content and analysis were developed by the team. AI support was limited to some code changes, formatting, and documentation.  

**Academic Integrity Statement:** All AI-generated content has been reviewed, understood, and verified by the authors. The authors take full responsibility for the accuracy and appropriateness of all content in this document. 

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Objectives](#objectives)  
3. [Methodology](#methodology)  
4. [Implementation](#implementation)  
5. [Results](#results)  
6. [Conclusions](#conclusions)  
7. [References](#references)  

---

## Project Overview

This project focuses on analyzing the performance of a **video streaming platform** using synthetic datasets. The datasets include **users, content, and viewing sessions** that simulate the behavior of a real platform. The purpose of this project is to design relational and NoSQL database models, perform descriptive and inferential statistical analyses, and prepare for the development of dashboards and ETL pipelines in later phases.  

---

## Directory Overview
The following tree diagram shows the content of the repository and indicates where each part of the project is:
~~~
── dags/
│   └── spotify_/
│       ├── dashboard/
│       ├── data/
│       ├── docs/
│       ├── nosql/
│       ├── sql/
│       ├── scripts/
│       ├── utils/
│       └── dag.py
├── config/
├── logs/
├── init-scripts/
└── plugins/
~~~

---


## Objectives

### Main Objectives
- To apply concepts of visual modeling and data analysis for a comprehensive study of a video streaming platform.  
- To design and implement relational and NoSQL database models for structured and unstructured data.  
- To perform statistical analysis in order to extract insights from user behavior and content performance.  

### Secondary Objectives
- To create and normalize an ER relational database model.  
- To implement complex SQL queries with joins, subqueries, and aggregations.  
- To design NoSQL collections and aggregation pipelines for MongoDB.  
- To perform descriptive statistics on user engagement, content popularity, and device usage.  
- To conduct inferential analysis, including hypothesis testing, correlation, clustering, and predictive modeling (Phase 2).  

---

## Methodology

### Data Sources
- **users.csv:** Contains user demographic and subscription information.  
- **content.json:** Contains structured information about movies and series.  
- **viewing_sessions.csv:** Contains detailed viewing session data including device, duration, and quality.  

### Tools and Technologies
- **Database:** PostgreSQL, MongoDB  
- **Programming Language:** Python  
- **Libraries:** pandas, numpy, scipy, scikit-learn, matplotlib, seaborn  
- **Visualization (planned for Phase 3):** Tableau  

### Approach
- **Phase 1:** Database design in both relational and NoSQL models.  
- **Phase 2:** Statistical analysis (descriptive and inferential).  
- **Phase 3:** Interactive dashboards and data storytelling using Tableau.  
- **Phase 4:** ETL pipeline for automated data ingestion, cleaning, and loading into the relational and NoSQL databases.  

---

## Implementation

### Phase 1: Database Design
- **Relational Model:**  
  - ER diagram created for users, content, and viewing sessions.  
  - Tables normalized with primary keys, foreign keys, and constraints.  
  - Scripts: `load_sql.py` for creating tables and inserting CSV data in batches.  
- **NoSQL Model:**  
  - MongoDB collections for content and user analytics.  
  - Indexes created on `content_id` and `user_id` to optimize queries.  
  - Aggregation pipelines prepared for summarizing content views and user engagement.  

### Phase 2: Statistical Analysis
- **Descriptive Statistics:**  
  - Average, median, min, max, standard deviation calculated for user watch time, content rating, and production budget.  
  - Distribution plots and outlier detection performed using matplotlib and seaborn.  
- **Inferential Analysis:**  
  - Correlation between user age, subscription type, and watch duration.  
  - Clustering of users by watch behavior.  
  - Regression modeling for predicting content popularity based on production budget and rating.  

### Phase 3: Data Visualization
- **Interactive Dashboards:**  
  - Planned dashboards include KPIs such as average watch time per user, most popular content by type, and engagement trends.  
  - Tableau will connect directly to PostgreSQL to retrieve processed datasets (`users`, `viewing_sessions`, `entertainment_content`, `movie_details`, `series_details`).  
  - Charts include line charts for trends, bar charts for categorical comparisons, and heatmaps for correlations.  

### Phase 4: ETL Pipeline Development
- **Data Extraction:** `extract_and_normalize.py` converts `content.json` to CSVs and preprocesses users and sessions datasets.  
- **Data Loading:** `load_sql.py` and `load_nosql.py` load data into PostgreSQL and MongoDB respectively.  
- **Automation & Monitoring:** Scripts include batch inserts, error handling, and logging to ensure reliable ETL execution. 
- Airflow was the tool selected for ETL implementation.

---

## Results

### Key Findings

1. **User Engagement Patterns:** Users with longer subscription durations tend to watch more content and spend more hours per week streaming.  
2. **Content Popularity:** Movies with higher production budgets and ratings generally have higher total views, while series popularity correlates with the number of seasons and average episode duration.  
3. **Device and Quality Trends:** Most sessions are completed on mobile devices at medium to high quality; lower quality levels correlate with lower completion percentages.  

### Visualizations

- Histograms for user watch time and content ratings.  
- Boxplots for production budget vs. content views.  
- Correlation heatmaps between user demographics and viewing behavior.  
- Dashboards for top 10 movies and series by views, average watch time per user, and completion percentage trends.  

### Performance Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| Accuracy | N/A | Not applicable, descriptive statistics and clustering used |
| Processing Time | ~15 min for full ETL batch | Time measured for CSV ingestion and table creation in PostgreSQL |
| Memory Usage | ~1.5 GB | Measured during batch insertion of all datasets |

---

## Conclusions

### Summary
At this stage, the project includes the **relational and NoSQL database design** as well as the **descriptive and inferential statistical analysis** of the datasets. Phase 3 and 4 build on these foundations with dashboards and automated ETL processes.  

### Lessons Learned
- Normalization and indexing are essential for query efficiency and scalability.  
- MongoDB allows flexible analytics on content and user behavior that complement relational modeling.  
- Statistical analysis provides actionable insights for user engagement and content performance.  

### Future Work
- Completion of Phase 3 dashboards in Tableau for visual storytelling and KPI tracking.  
- Full implementation of Phase 4 ETL pipeline with logging, error handling, and automated schedule.  
- Integration with cloud services for scalable deployment and analytics monitoring.  

---

## References

1. PostgreSQL Documentation. (n.d.). https://www.postgresql.org/docs/  
2. MongoDB Manual. (n.d.). https://www.mongodb.com/docs/manual/  
3. Pandas Documentation. (n.d.). https://pandas.pydata.org/docs/  
4. Scikit-learn User Guide. (n.d.). https://scikit-learn.org/stable/user_guide.html  
5. Plotly Documentation. (n.d.). https://plotly.com/python/  

---

**Note:** This document is part of the academic portfolio for the Data Engineering program at Universidad Politécnica de Yucatán.