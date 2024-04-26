--will create table from orders.csv and solve the task:
DROP TABLE IF EXISTS orders_raw; 

CREATE TABLE orders_raw (
	Customer_name VARCHAR(32),
	Order_day DATE,
	Order_Id INTEGER,
	Prod_Name VARCHAR(32),
	Qty INTEGER,
	Price FLOAT);

--load CSV to orders_raw:
\copy orders_raw FROM 'orders.csv' WITH (FORMAT csv, header);

--Найти клиентов кто купил 7 iPhone и 2 Airpods:
WITH tab AS (
	SELECT 
		Customer_Name,
		SUM(Qty) FILTER (WHERE Prod_Name = 'iPhone') AS iPhone_ttl,
		SUM(Qty) FILTER (WHERE Prod_NAme = 'Airpods') AS Airpods_ttl
	FROM orders_raw
	GROUP BY 1 ORDER BY 1	
)

SELECT * 
FROM tab 
WHERE iPhone_ttl = 6 AND Airpods_ttl = 1
;


