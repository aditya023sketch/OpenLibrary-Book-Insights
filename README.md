Open Library Data Pipeline
Overview
This project demonstrates a Big Data pipeline using the Open Library API to fetch book-related metadata, process and clean the data, store it in a distributed database (MongoDB), and perform data analysis and visualization. The pipeline showcases how raw data is transformed into actionable insights through ingestion, cleaning, aggregation, and visualization.

Features
Data Ingestion:

Extracted data from the Open Library API using Python's requests library.
The dataset includes book titles, authors, publication years, languages, publishers, and other metadata.
Saved the raw data in CSV format and imported it into MongoDB for storage.
Data Cleaning:

Handled missing values, standardized formats, and removed duplicates using Python and MongoDB queries.
Ensured data integrity for meaningful analysis.
Data Aggregation:

Generated insights such as the most prolific authors, publication trends over decades, and linguistic distribution of books.
Visualizations:

Created three visualizations:
Horizontal Bar Chart: Top 10 authors with the most books.
Line Chart: Publication trends over decades for the top 5 authors.
Donut Chart: Distribution of books by the top 5 languages.
Project Workflow
1. Data Ingestion (Bronze Layer)
Used the Open Library API to fetch metadata for books based on keywords, genres, and authors.
Stored the raw dataset in MongoDB for efficient querying and analysis.
2. Data Cleaning (Silver Layer)
Processed the raw data to:
Remove duplicates and handle missing values.
Standardize column names and data formats.
Perform exploratory data analysis (EDA) to identify inconsistencies.
3. Data Aggregation and Insights (Gold Layer)
Aggregated data to answer questions such as:
Which authors have published the most books?
How do publication trends vary over decades?
What is the linguistic distribution of books?
4. Visualizations
Visualization 1: Horizontal Bar Chart
Highlighted the top 10 authors with the most books, showcasing their contributions across genres.
Visualization 2: Line Chart
Showed publication trends over decades for the top 5 authors, comparing their productivity over time.
Visualization 3: Donut Chart
Displayed the percentage of books published in the top 5 languages, emphasizing the dominance of English.
Technologies Used
Programming Languages:
Python
Libraries:
requests: For API calls.
pandas: For data processing and cleaning.
matplotlib and seaborn: For data visualization.
Database:
MongoDB (document-oriented, distributed database).
How to Run the Project
Prerequisites
Install Python 3.x and MongoDB.
Install required Python libraries:
bash
Copy code
pip install -r requirements.txt
Steps
Data Ingestion:

Run the Python script to fetch data from the Open Library API and save it as a CSV:
bash
Copy code
python scripts/fetch_data.py
Load Data into MongoDB:

Use insert_to_mongo.py to insert the CSV data into MongoDB:
bash
Copy code
python scripts/insert_to_mongo.py
Data Cleaning:

Perform data cleaning using the script:
bash
Copy code
python scripts/clean_data_db.py
Data Aggregation and Visualization:

Generate visualizations using:
bash
Copy code
python scripts/visualize.py
Visualizations
Top 10 Authors by Number of Books:
Horizontal bar chart ranking the most prolific authors.
Publication Trends Over Decades:
Line chart showing the publishing activity of the top 5 authors over time.
Top 5 Languages by Book Count:
Donut chart illustrating the linguistic distribution of the dataset.
