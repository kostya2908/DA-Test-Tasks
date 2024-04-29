--1. Please find the absolute difference in revenue
--(price multiplied by quantity) between the last purchase in the status Regular
--and the first purchase in the status 'Loyal' for each userid;

--2. Please calculate the number of unique daily purchases in the status regular and loyal
--for each userid. The output should have a format - userid, number of regular purchases,
--number of loyal purchases;

--3. Find the difference in days between the first regular purchase and
--the second loyal purchase for each userid;

DROP TABLE IF EXISTS apalon_orders;
CREATE TABLE apalon_orders (
	userid INT,
	status VARCHAR,
	order_id VARCHAR,
	date_of_purchase DATE,
	price INT,
	quantity INT);
\copy apalon_orders FROM './06_apalon_4_1_orders.csv' WITH (FORMAT csv, header);
SELECT * FROM apalon_orders LIMIT 3;

----------------------------------------------------------------------------------------------
--3
WITH tab AS (
	SELECT
		userid,
		status,
		date_of_purchase,
		CASE
			WHEN status = 'regular'
				THEN FIRST_VALUE(date_of_purchase) OVER (PARTITION BY userid, status)
			WHEN status = 'loyal'
				THEN NTH_VALUE(date_of_purchase, 2) OVER (PARTITION BY userid, status)
		END AS dates
	FROM apalon_orders
)

SELECT
	DISTINCT userid,
	FIRST_VALUE(dates) OVER (PARTITION BY userid) -
	LAST_VALUE(dates) OVER (PARTITION BY userid) AS diff_dates
FROM tab ORDER BY 1;


--------------------------------------------------------------------------------------------
--2
SELECT
	userid,
	COUNT(status) FILTER (WHERE status = 'regular') AS no_of_regular,
	COUNT(status) FILTER (WHERE status = 'loyal') AS no_of_loyal
FROM apalon_orders
GROUP BY 1 ORDER BY 1;

-------------------------------------------------------------------------------------------
--1
WITH tab AS (
	SELECT
		userid,
		status,
		price * quantity AS revenue,
		CASE 
			WHEN status = 'regular'
				THEN LAST_VALUE(price*quantity) OVER (PARTITION BY userid, status)
			WHEN status = 'loyal'
				THEN FIRST_VALUE(price*quantity) OVER (PARTITION BY userid, status)
		END AS new
	FROM apalon_orders
)

SELECT
	DISTINCT userid,
	ABS(
		(FIRST_VALUE(new) OVER (PARTITION BY userid)) - 
		(LAST_VALUE(new) OVER (PARTITION BY userid))
	) AS diff
FROM tab
GROUP BY userid, new;

--в решении выше один, в случае, если у юзера отсутствует одна из категорий diff = 0




/* The following code works cool:
SELECT
	userid,
	status,
	date_of_purchase,
	revenue,
	LAST_VALUE(CASE WHEN status = 'regular' THEN revenue END) 
		OVER (PARTITION BY userid, status) AS last_reg_rev,
	FIRST_VALUE(CASE WHEN status = 'loyal' THEN revenue END)
		OVER (PARTITION BY userid, status) AS first_loyal_rev
FROM sorted;
*/
