from sqlalchemy import create_engine, text, String, Float, Integer
import pandas as pd
import os

# 1. Establish MySQL connection
engine = create_engine('mysql+pymysql://root:root@localhost:3306/testdb')

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies_2024_new (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            Rating FLOAT,
            Votes INTEGER,
            Duration VARCHAR(20),
            Genre VARCHAR(50),
            Duration_Minutes INTEGER,          
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()

csv_path = 'combined_cleaned_file.csv'  # Adjust path as needed
# Validate CSV exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

df = pd.read_csv(csv_path)

# Define your table name
table_name = 'movies_2024_new'

# Define SQL data types mapping  

dtype_mapping = {
    'Name': String(255),          # VARCHAR(255)
    'Rating': Float(),            # FLOAT
    'Votes': Integer(),          # VARCHAR(50) - to preserve "K" notation
    'Duration': String(20),       # VARCHAR(20)
    'Genre': String(50),           # VARCHAR(50)
    'Duration_Minutes': Integer()
}

try:
    # Push data to MySQL
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',       # Options: 'fail', 'replace', 'append'
        index=False,
        dtype=dtype_mapping,
        chunksize=1000           # Process in chunks for large files
    )
    print(f"Successfully loaded data into MySQL table '{table_name}'")
    
except Exception as e:
    print(f"Error loading data into MySQL: {str(e)}")
    
finally:
    engine.dispose()  # Close the connection