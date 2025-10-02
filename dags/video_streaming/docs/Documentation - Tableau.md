 Phase Documentation - Tableau

## General Description
In this phase, I used *Tableau* to create interactive dashboards that analyze content consumption on the platform.  
The work was based on the CSV files generated in previous phases, connecting user data, viewing sessions, and content information.  

## Files Used
- viewing_sessions.csv → Records of each viewing session (user, content, duration, date, video quality).  
- users.csv → User information (country, subscription type, etc.).  
- content.csv → General details of the content.  
- content_genres.csv → Content genres.  
- movie_details.csv, series_details.csv, series_episodes.csv → Specific information about movies and series.  

## Process
1. *Loading Data in Tableau*  
   - Imported all CSV files.  
   - Established relationships using primary keys (user_id, content_id).  

2. *Data Modeling and Relationships*  
   - viewing_sessions.csv was used as the central table.  
   - Connected with users.csv for country and subscription analysis.  
   - Connected with content.csv and related tables to obtain genre and content type information.  

3. *Dashboards and Visualizations*  
   - *Country Map (Sheet 1)*  
     Shows the distribution of users by country (Mexico, Argentina, Colombia, Chile, and Peru).  
   - *Video Quality Consumption Table (Sheet 2)*  
     Displays the number of viewing hours in 4K, HD, and SD by country.  
   - *Subscription Types (Sheet 3)*  
     Bar chart showing the number of users with Basic, Standard, and Premium plans.  
   - *Country Distribution (Sheet 4)*  
     Bubble chart comparing the number of users in each country.  
   - *Top Genres (Sheet 5)*  
     Bar chart showing the total watch time by genre (Action, Horror, Romance, Drama, etc.).  

## Key Findings
- *Mexico* has the largest number of users (1,514), followed by Colombia and Argentina.  
- Users consume more content in *4K quality*, but HD and SD still have significant proportions.  
- The *Basic* plan is the most popular (2,003 users), while *Premium* is the least subscribed (1,214).  
- The most-watched genres are *Action, Horror, and Romance*, although all genres maintain relatively similar viewing hours.  

## Tools Used
- Tableau Public  
- CSV files generated in previous phases  

## Observations
- Defining relationships between tables was essential to avoid duplicated or inconsistent data.  
- Tableau makes it easy to build intuitive visualizations to analyze trends at different levels: country, user, and content.  

---