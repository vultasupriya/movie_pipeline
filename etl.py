import pandas as pd
import requests
from sqlalchemy import create_engine
import time

from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY not set. Add to environment or .env")


# ========== CONFIGURATION ==========
MOVIES_CSV = 'data/movies.csv'
RATINGS_CSV = 'data/ratings.csv'
DATABASE_URI = 'sqlite:///movies.db'

# ===================================

# 1️⃣ Extract
print("🔹 Reading CSV files...")
movies = pd.read_csv(MOVIES_CSV)
ratings = pd.read_csv(RATINGS_CSV)

# 2️⃣ Transform
print("🔹 Cleaning and processing data...")
# Extract year from title
movies['year'] = movies['title'].str.extract(r'\((\d{4})\)').astype(float)
movies['title'] = movies['title'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()

# Define OMDb fetch function
def fetch_omdb_details(title):
    """Fetch details from OMDb API using movie title."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('Response') == 'True':
            return pd.Series({
                'director': data.get('Director'),
                'plot': data.get('Plot'),
                'box_office': data.get('BoxOffice'),
            })
        else:
            return pd.Series({'director': None, 'plot': None, 'box_office': None})
    except Exception:
        return pd.Series({'director': None, 'plot': None, 'box_office': None})

# Apply API enrichment (limit to 50 to avoid free plan limits)
print("🔹 Fetching additional movie data from OMDb API...")
sampled_movies = movies.head(50).copy()
sampled_movies[['director', 'plot', 'box_office']] = sampled_movies['title'].apply(fetch_omdb_details)
time.sleep(1)

# Merge enriched data back
movies = movies.merge(sampled_movies[['movieId', 'director', 'plot', 'box_office']], on='movieId', how='left')

# 3️⃣ Load
print("🔹 Loading data into database...")
engine = create_engine(DATABASE_URI)

# Create tables
movies.to_sql('movies', con=engine, if_exists='replace', index=False)
ratings.to_sql('ratings', con=engine, if_exists='replace', index=False)

print("✅ ETL process completed successfully!")
