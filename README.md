# movie_pipeline

# 🎬 Movie Data Pipeline

## 📘 Overview
This project implements a simple **ETL (Extract, Transform, Load) data pipeline** for movie data.  
It ingests datasets from **MovieLens (CSV files)** and enriches them using the **OMDb API**, then loads the processed data into a **SQLite database** for analysis.

This assignment demonstrates data engineering skills in:
- Data ingestion
- Data transformation & enrichment
- Database design
- Analytical querying using SQL

---

## ⚙️ Tech Stack
- **Python 3.10+**
- **Pandas** → Data manipulation  
- **Requests** → API integration  
- **SQLAlchemy** → Database connection  
- **SQLite** → Relational database  
- **OMDb API** → External movie metadata source  
- **dotenv** → Securely store API key

---

## 🧩 Project Structure
```
movie_pipeline/
├── data/
│   ├── movies.csv
│   └── ratings.csv
├── etl.py
├── schema.sql
├── queries.sql
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🗂️ Dataset

**Source:** [MovieLens Small Dataset](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)  
Extract the ZIP and place the following inside the `data/` folder:
- `movies.csv`
- `ratings.csv`

---

## 🔑 OMDb API Key Setup (Hide Your Key)

### 1️⃣ Get your key:
- Visit [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)
- Choose the **Free plan**
- Copy the API key sent to your email

### 2️⃣ Create a `.env` file in your project root:
```
OMDB_API_KEY=your_actual_api_key_here
```

### 3️⃣ Make sure `.env` is ignored by Git:
Add this line to `.gitignore`:
```
.env
movies.db
```

---

## 🧱 Database Schema (`schema.sql`)

```sql
CREATE TABLE IF NOT EXISTS movies (
    movieId INTEGER PRIMARY KEY,
    title TEXT,
    genres TEXT,
    director TEXT,
    plot TEXT,
    box_office TEXT,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS ratings (
    userId INTEGER,
    movieId INTEGER,
    rating REAL,
    timestamp INTEGER,
    FOREIGN KEY (movieId) REFERENCES movies(movieId)
);
```

---

## 🔄 ETL Pipeline (`etl.py`)

The ETL script performs:
1. **Extract:** Reads `movies.csv` and `ratings.csv`
2. **Transform:**  
   - Cleans titles and extracts release years  
   - Fetches extra details (Director, Plot, Box Office) from the OMDb API  
3. **Load:**  
   - Writes the cleaned and enriched data into an SQLite database (`movies.db`)

### Run the ETL pipeline:
```bash
python etl.py
```

You’ll see:
```
🔹 Reading CSV files...
🔹 Cleaning and processing data...
🔹 Fetching additional movie data from OMDb API...
🔹 Loading data into database...
✅ ETL process completed successfully!
```

---

## 🧮 Analytical Queries (`queries.sql`)

You can run these queries directly inside **DB Browser for SQLite** or via Python.

### Example Queries:
1. **Movie with the highest average rating**
    ```sql
    SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_rating
    FROM movies m
    JOIN ratings r ON m.movieId = r.movieId
    GROUP BY m.title
    ORDER BY avg_rating DESC
    LIMIT 1;
    ```

2. **Top 5 genres by rating**
    ```sql
    SELECT g.genre, ROUND(AVG(r.rating), 2) AS avg_rating
    FROM (
        SELECT movieId, TRIM(value) AS genre
        FROM movies, json_each('["' || REPLACE(genres, '|', '","') || '"]')
    ) g
    JOIN ratings r ON g.movieId = r.movieId
    GROUP BY g.genre
    ORDER BY avg_rating DESC
    LIMIT 5;
    ```

3. **Director with most movies**
    ```sql
    SELECT director, COUNT(*) AS movie_count
    FROM movies
    WHERE director IS NOT NULL
    GROUP BY director
    ORDER BY movie_count DESC
    LIMIT 1;
    ```

4. **Average rating per release year**
    ```sql
    SELECT m.year, ROUND(AVG(r.rating), 2) AS avg_rating
    FROM movies m
    JOIN ratings r ON m.movieId = r.movieId
    GROUP BY m.year
    ORDER BY m.year;
    ```

---

## 🧰 Installation & Setup

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Pipeline
```bash
python etl.py
```

### 3️⃣ Inspect Database
Use DB Browser for SQLite or Python’s `sqlite3` module:
```python
import sqlite3
conn = sqlite3.connect('movies.db')
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
```

---

## 📊 Outputs
- Database file: `movies.db`
- Tables: `movies`, `ratings`
- Enriched movie metadata (Director, Plot, Box Office)
- Ready-to-use analytical queries

---

## 💡 Improvements & Scaling Ideas
- Use **async or multithreading** to speed up API calls  
- Add **caching** for repeated titles  
- Implement with **Airflow / Prefect** for production scheduling  
- Store final data in **PostgreSQL** or **BigQuery**  
- Create **Dash / Streamlit dashboard** for movie insights

---

## 👨‍💻 Author
Developed by **[Your Name]**  
for **TSWorks Data Engineering Assignment**

📧 *Replace this with your contact email (optional)*
