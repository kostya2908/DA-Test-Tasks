--Please find distinct names of users who bought books but not clothes.

DROP TABLE IF EXISTS apalon_purchases;
CREATE TABLE apalon_purchases (
	id SERIAL NOT NULL PRIMARY KEY,
	userid INT,
	item VARCHAR(16));
\copy apalon_purchases (userid, item) FROM './06_apalon_4_2_purchases.csv' WITH (FORMAT csv, header);
--ALTER TABLE apalon_purchases ADD COLUMN xtr INT DEFAULT 1;
SELECT * FROM apalon_purchases;

DROP TABLE IF EXISTS apalon_users;
CREATE TABLE apalon_users (
	userid INT PRIMARY KEY,
	name VARCHAR(10));
\copy apalon_users FROM './06_apalon_4_2_users.csv' WITH (FORMAT csv, header);
SELECT * FROM apalon_users;

WITH TAB AS (
	SELECT
		au.name,
		COUNT(ap.item) FILTER (WHERE ap.item = 'Books') AS books,
		COUNT(ap.item) FILTER (WHERE ap.item = 'Clothes') AS clothes
	FROM apalon_purchases AS ap
	LEFT JOIN apalon_users AS au USING (userid)
	GROUP BY 1 ORDER BY 1
)

SELECT name FROM tab WHERE books > 0 AND clothes = 0;


