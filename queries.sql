-- 1️⃣ Movie with the highest average rating
SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.title
ORDER BY avg_rating DESC
LIMIT 1;

-- 2️⃣ Top 5 genres with the highest average rating
SELECT g.genre, ROUND(AVG(r.rating), 2) AS avg_rating
FROM (
    SELECT movieId, TRIM(value) AS genre
    FROM movies, json_each('["' || REPLACE(genres, '|', '","') || '"]')
) g
JOIN ratings r ON g.movieId = r.movieId
GROUP BY g.genre
ORDER BY avg_rating DESC
LIMIT 5;

-- 3️⃣ Director with the most movies
SELECT director, COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;

-- 4️⃣ Average rating of movies released each year
SELECT m.year, ROUND(AVG(r.rating), 2) AS avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.year
ORDER BY m.year;
