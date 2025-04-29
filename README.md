# IMDb 2024 Movies Analysis Project


A comprehensive data pipeline for scraping, processing, analyzing, and visualizing 2024 movie data from IMDb.

## Project Overview

This project consists of four main components:
1. Web scraping IMDb for 2024 movie data by genre
2. Cleaning and combining the scraped data
3. Storing the data in a MySQL database
4. Interactive dashboard for data visualization and analysis

## Features

- **Scraping**: Collects movie data (title, rating, votes, duration, genre) from IMDb
- **Data Processing**: Cleans and transforms raw data into analysis-ready format
- **Database Integration**: Stores processed data in MySQL
- **Interactive Dashboard**: Streamlit app with filters and visualizations

## Technologies Used

- Python 3.x
- Selenium (Web scraping)
- Pandas (Data processing)
- MySQL (Database)
- SQLAlchemy (Database ORM)
- Streamlit (Dashboard)
- Matplotlib/Seaborn (Visualization)


## Usage

### 1. Scrape Data
Run the scraping script:
```bash
python scrape.py
This will create CSV files for each genre in csv_files/ directory.

### 2. Combine and Clean Data
```bash
python csv_combine.py
Creates combined_cleaned_file.csv with all movies.

### 3. Load to Database
```bash
python sql.py
Loads cleaned data into MySQL.

### 4. Launch Dashboard
```bash
streamlit run stream.py
Access the interactive dashboard at http://localhost:8501


## Dashboard Features

### Filtering Options
- **By Genre**: Select one or multiple genres
- **By Rating Range**: Slider for minimum/maximum ratings (0-10 scale)
- **By Votes**: Set minimum vote threshold
- **By Duration**: Filter by short/medium/long movies

### Visualizations
- **Genre Distribution**  
  ![Genre Distribution](https://via.placeholder.com/300x200?text=Genre+Distribution+Chart)
  - Pie charts and bar graphs showing genre popularity

- **Rating vs. Votes Correlation**  
  ![Rating vs Votes](https://via.placeholder.com/300x200?text=Rating+vs+Votes+Scatter)
  - Interactive scatter plot with logarithmic scale

- **Duration Analysis**  
  ![Duration Analysis](https://via.placeholder.com/300x200?text=Duration+Histogram)
  - Histograms showing movie length distribution

### Top Performers
- **Highest Rated Movies**  
  - Table of top 10 movies by IMDB rating
- **Most Voted Movies**  
  - Table of most popular movies by vote count
- **Duration Extremes**  
  - Lists of shortest and longest movies

### Advanced Analysis
- **Heatmaps**  
  ![Heatmap](https://via.placeholder.com/300x200?text=Genre+Rating+Heatmap)
  - Genre vs. rating intensity maps
- **Scatter Plots**  
  - Duration vs. rating relationships
- **Histograms**  
  - Rating distribution analysis
