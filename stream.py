import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Page configuration
st.set_page_config(page_title="IMDb 2024 Movies Dashboard", layout="wide")
st.title("🎬 IMDb 2024 Movies Analysis Dashboard")

# Database connection function
@st.cache_resource
def get_db_connection():
    return create_engine('mysql+pymysql://root:root@localhost:3306/testdb')

# Load and preprocess data
@st.cache_data(ttl=3600)
def load_data():
    engine = get_db_connection()
    query = "SELECT Name, Rating, Votes, Duration, Genre, Duration_minutes FROM movies_2024_new"
    df = pd.read_sql(query, engine)
    
    # Clean data
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce').fillna(0).astype(int)
    
    # Handle movies with multiple genres (split and explode)
    df['Genre'] = df['Genre'].str.split(', ')
    df = df.explode('Genre')
    
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Movies")
selected_genres = st.sidebar.multiselect(
    "Select genres",
    options=sorted(df['Genre'].unique()),
    default=None
)

rating_range = st.sidebar.slider(
    "Select rating range",
    min_value=0.0,
    max_value=10.0,
    value=(5.0, 10.0),
    step=0.1
)

min_votes = st.sidebar.number_input(
    "Minimum votes",
    min_value=0,
    max_value=df['Votes'].max(),
    value=10000,
    step=1000
)

duration_filter = st.sidebar.selectbox(
    "Duration range",
    options=["All", "Short (< 2 hrs)", "Medium (2-3 hrs)", "Long (> 3 hrs)"],
    index=0
)

# Apply filters
filtered_df = df.copy()
if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]
filtered_df = filtered_df[(filtered_df['Rating'] >= rating_range[0]) & 
                         (filtered_df['Rating'] <= rating_range[1])]
filtered_df = filtered_df[filtered_df['Votes'] >= min_votes]

if duration_filter == "Short (< 2 hrs)":
    filtered_df = filtered_df[filtered_df['Duration_minutes'] < 120]
elif duration_filter == "Medium (2-3 hrs)":
    filtered_df = filtered_df[(filtered_df['Duration_minutes'] >= 120) & 
                             (filtered_df['Duration_minutes'] <= 180)]
elif duration_filter == "Long (> 3 hrs)":
    filtered_df = filtered_df[filtered_df['Duration_minutes'] > 180]

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎭 Genres", "🏆 Top Movies", "📈 Analysis"])

with tab1:
    st.header("Overview Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Movies", len(filtered_df['Name'].unique()))
    with col2:
        st.metric("Average Rating", f"{filtered_df['Rating'].mean():.1f}")
    with col3:
        st.metric("Average Votes", f"{filtered_df['Votes'].mean():,.0f}")
    
    st.subheader("Filtered Movies")
    st.dataframe(filtered_df.drop_duplicates(subset='Name')[['Name', 'Rating', 'Votes', 'Genre', 'Duration']]
                 .sort_values('Rating', ascending=False)
                 .reset_index(drop=True))

with tab2:
    st.header("Genre Analysis")
    
    # Prepare genre data
    genre_stats = filtered_df.groupby('Genre').agg(
        Movie_Count=('Name', 'nunique'),
        Avg_Rating=('Rating', 'mean'),
        Avg_Duration=('Duration_minutes', 'mean'),
        Total_Votes=('Votes', 'sum')
    ).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Genre Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=genre_stats.sort_values('Movie_Count', ascending=False).head(10),
                    y='Genre', x='Movie_Count', palette='viridis')
        plt.title('Top 10 Genres by Movie Count')
        st.pyplot(fig)
        
        st.subheader("Average Duration by Genre")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=genre_stats.sort_values('Avg_Duration'),
                    y='Genre', x='Avg_Duration', palette='rocket')
        plt.title('Average Duration (minutes)')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Most Popular Genres by Votes")
        fig, ax = plt.subplots(figsize=(8, 8))
        genre_stats_top = genre_stats.sort_values('Total_Votes', ascending=False).head(10)
        ax.pie(genre_stats_top['Total_Votes'], 
               labels=genre_stats_top['Genre'], 
               autopct='%1.1f%%')
        plt.title('Vote Distribution by Genre (Top 10)')
        st.pyplot(fig)
        
        st.subheader("Voting Trends by Genre")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=genre_stats.sort_values('Total_Votes'),
                    y='Genre', x='Total_Votes', palette='mako')
        plt.title('Total Votes by Genre')
        st.pyplot(fig)

with tab3:
    st.header("Top Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Movies by Rating")
        top_rated = filtered_df.sort_values(['Rating', 'Votes'], ascending=[False, False])\
                              .drop_duplicates('Name')\
                              .head(10)
        st.dataframe(top_rated[['Name', 'Rating', 'Votes', 'Genre', 'Duration']]
                     .reset_index(drop=True))
        
        st.subheader("Shortest Movies")
        shortest = filtered_df.sort_values('Duration_minutes')\
                            .drop_duplicates('Name')\
                            .head(5)
        st.dataframe(shortest[['Name', 'Duration', 'Genre', 'Rating']]
                     .reset_index(drop=True))
    
    with col2:
        st.subheader("Top 10 Movies by Votes")
        top_voted = filtered_df.sort_values(['Votes', 'Rating'], ascending=[False, False])\
                              .drop_duplicates('Name')\
                              .head(10)
        st.dataframe(top_voted[['Name', 'Votes', 'Rating', 'Genre', 'Duration']]
                     .reset_index(drop=True))
        
        st.subheader("Longest Movies")
        longest = filtered_df.sort_values('Duration_minutes', ascending=False)\
                           .drop_duplicates('Name')\
                           .head(5)
        st.dataframe(longest[['Name', 'Duration', 'Genre', 'Rating']]
                     .reset_index(drop=True))
    
    st.subheader("Genre-Based Rating Leaders")
    genre_leaders = filtered_df.loc[filtered_df.groupby('Genre')['Rating'].idxmax()]
    st.dataframe(genre_leaders[['Genre', 'Name', 'Rating', 'Votes', 'Duration']]
                 .sort_values('Rating', ascending=False)
                 .reset_index(drop=True))

with tab4:
    st.header("Advanced Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rating Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(filtered_df['Rating'], bins=20, kde=True)
        plt.title('Distribution of Movie Ratings')
        st.pyplot(fig)
        
        st.subheader("Ratings by Genre (Heatmap)")
        pivot_df = filtered_df.pivot_table(index='Genre', values='Rating', aggfunc='mean')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot_df, annot=True, cmap='coolwarm', fmt=".1f")
        plt.title('Average Ratings by Genre')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Rating vs Votes Correlation")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=filtered_df, x='Rating', y='Votes', hue='Genre')
        plt.yscale('log')
        plt.title('Rating vs Votes (log scale)')
        st.pyplot(fig)
        
        st.subheader("Duration vs Rating")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=filtered_df, x='Duration_minutes', y='Rating', hue='Genre')
        plt.title('Duration vs Rating')
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("**Data Source:** IMDb | **Analysis Date:** " + pd.Timestamp.now().strftime('%Y-%m-%d'))