# Phase Documentation - Spotify (Tableau) - Project

## General Description
In this phase, I used *Tableau* to analyze and visualize trends in music popularity, artist influence, and track characteristics on Spotify.  
The dataset included diverse musical metrics and popularity indicators, allowing for the formulation of analytical objectives and hypotheses about user behavior and music evolution between 2010 and 2020.  

The visualizations aim to understand **how different musical features, genres, and artists influence popularity** and what patterns emerge across years and playlists.

---

## Files Used
- **spotify_tracks.csv** → Contains all track-level information and metrics.  
- **playlist_data.csv** → Lists playlists, genres, and subgenres.  
- **artist_data.csv** → Contains artist names and identifiers.  

**Key columns used:**  
`track_id`, `track_name`, `track_artist`, `track_popularity`,  
`track_album_id`, `track_album_name`, `track_album_release_date`,  
`playlist_name`, `playlist_genre`, `playlist_subgenre`,  
`danceability`, `energy`, `key`, `loudness`, `mode`,  
`speechiness`, `acousticness`, `instrumentalness`, `liveness`,  
`valence`, `tempo`, `duration_ms`.

---

## Process
1. **Data Loading and Connection**  
   - Imported all CSV files into Tableau.  
   - Established relationships through `track_id` and `playlist_id`.  

2. **Data Modeling and Cleaning**  
   - Used *track_album_release_date* to filter and organize trends from 2010–2020.  
   - Joined metrics tables to analyze correlations between song features and popularity.  

3. **Visualizations Created**
   - **The Evolution of Music (Area Chart):**  
     Displays the growth of total track popularity by year and genre.
   - **Playlist Genre Popularity (Bar Chart):**  
     Shows the aggregated popularity by playlist genre.
   - **Treemap by Song Danceability:**  
     Highlights which tracks and artists have the highest danceability and popularity.  
   - **Top Artists (Bar Chart):**  
     Compares total popularity among the top 10 artists.
   - **Track Feature Correlation (Bubble Chart):**  
     Cross-analyzes *danceability*, *energy*, *valence*, and *track_popularity*.

---

## Analysis Objectives
- Identify and characterize **popularity trends** of songs and artists from 2010 to 2020.  
  - *Key columns:* `track_album_release_date`, `track_popularity`, `playlist_genre`.  
- Determine **which genres gained or lost popularity** over the years.  
  - *Key columns:* `playlist_genre`, `track_popularity`, `track_album_release_date`.  
- Analyze the **relationship between musical features and track popularity**.  
  - *Key columns:* `danceability`, `energy`, `loudness`, `valence`, `tempo`, `track_popularity`.  
- Identify **the most popular artists and genre concentration**.  
  - *Key columns:* `track_artist`, `track_popularity`, `playlist_genre`.  
- Understand **which playlists have the greatest influence** on song popularity.  
  - *Key column:* `playlist_name`, `track_popularity`.

---

## Derived Hypotheses

### **Evolution of Music (Area Chart)**
- **H1:** Music popularity on Spotify (*track_popularity*) grew significantly between 2010–2020.  
  *Justification:* The “Evolution of Music” area chart shows a steady rise in total popularity, especially after 2017.  
- **H2:** Pop and Rap genres are the main drivers of Spotify’s popularity growth from 2018–2020.  
  *Justification:* Pop and Rap areas dominate the visualization and exhibit the sharpest increases.

### **Track Features and Genre Correlation (Treemap & Bar Chart)**
- **H3:** There is a positive correlation between *danceability* and *track_popularity*.  
  *Justification:* The Treemap groups the most popular songs (“Dance Monkey”, “Sunflower”) in the high danceability range.  
- **H4:** Pop, Rap, and Latin are the genres with the highest average track popularity.  
  *Justification:* Bar charts by genre display these three as the top categories.

### **Playlist Influence and Artist Popularity**
- **H5:** Songs with high *danceability*, *energy*, and *valence* are more likely to appear in the most popular playlists.  
  *Justification:* Playlists like “PEARLMENT WAVE” and “URBAN CONTEMPO” favor tracks with engaging audio features.  
- **H6:** The popularity of top artists is driven by a few viral hits rather than consistent catalog performance.  
  *Justification:* The top 10 artists’ chart suggests that hits dominate overall popularity metrics.  
- **H7:** Artists can achieve high popularity even outside dominant genres (Pop, Rap).  
  *Justification:* Examples like *Kygo (EDM)* and *The Weeknd (R&B)* appear among top artists, showing cross-genre appeal.

---

## Key Findings
- The **2010–2020 period** shows consistent growth in global music popularity, especially for Pop and Rap.  
- **Danceability** and **energy** are strong predictors of song success.  
- **Latin music** gained notable presence in recent years, reflecting cultural diversification.  
- Most artists’ popularity is heavily influenced by specific *hit songs* rather than a uniform catalog.  
- Playlist curation plays a central role in amplifying a track’s reach and visibility.

---

## Tools Used
- Tableau Public  
- CSV datasets with audio features and popularity metrics  

---

## Observations
- Integrating multiple tables (tracks, artists, and playlists) allowed a multi-dimensional perspective on popularity.  
- Tableau facilitated dynamic exploration through filters and time sliders to reveal musical evolution patterns.  
- The correlation between *danceability* and *popularity* supports the idea that rhythm and mood are key drivers of listener engagement.  

------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------
------------------------------------------------------------------------
------------------------------------------------------------------------

# AI Assistance Disclosure - Project

# AI Tool Used
ChatGPT (GPT-5)

# Overall Assistance Level
Estimated: 12% (Minimal Assistance)

---

# Primary Use Cases
- **Concept clarification:** 6%  
  Used AI to understand how to connect SQL databases and Docker environments with Tableau.  
- **Troubleshooting and setup support:** 4%  
  Clarified connection errors and configuration steps.  
- **Documentation refinement:** 2%  
  Assisted with text organization and clarity improvements.  

---

# Human Contributions
- Built all dashboards, relationships, and analyses directly in Tableau.  
- Designed all chart layouts and selected metrics manually.  
- Performed data modeling, interpretation, and results validation independently.  
- Used AI exclusively for learning and clarification, not for dashboard creation.  

---

# Verification Process
- All dashboards were tested in Tableau Public to confirm data accuracy.  
- Each visualization was validated against raw CSV values.  
- All text was reviewed and adjusted to accurately reflect personal work.  

---

# Self-Assessment Framework

| **Category** | **Selected Level** | **Score** |
|---------------|--------------------|-----------|
| **1. Initiative and Conceptualization** | I completely defined the problem and analytical approach. | 10% |
| **2. Implementation** | I wrote all content and configured Tableau manually; AI clarified minor steps. | 10% |
| **3. Understanding and Validation** | I fully understand every visualization and relationship created. | 10% |
| **4. Problem Solving** | I identified and resolved all issues independently. | 10% |
| **→ Self-Assessment Average** | — | **10%** |

---

# AI Assistance Calculation

| **Component** | **Weight** | **Estimated AI Use** | **Weighted Contribution** |
|----------------|-------------|----------------------|----------------------------|
| **Time %** | 25% | 10% | 2.5% |
| **Content %** | 35% | 8% | 2.8% |
| **Complexity %** | 25% | 15% | 3.8% |
| **Self-Assessment Score** | 15% | 10% | 1.5% |
| **→ Final AI Assistance %** | — | — | **≈ 10.6% (rounded to 12%)** |

**Formula Used:**  
**Final AI Assistance % = (0.25 × Time %) + (0.35 × Content %) + (0.25 × Complexity %) + (0.15 × Self-Assessment Score)**  

---

# Assistance Level Interpretation
**Level 1 – Minimal Assistance (0–20%)**

AI was used only to clarify conceptual and connection-related questions.  
All analytical and visual processes were executed manually by the student.  

---
# Reflection
AI tools were used responsibly to enhance understanding of technical setup processes such as SQL–Tableau and Docker connectivity.  
All visualization, data modeling, and analysis work was performed independently, demonstrating autonomy and comprehension of the full workflow.  
This project represents a minimal and ethical integration of AI aligned with UPY academic standards.  

---




