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
		Prod_Name,
		SUM(Qty)
	FROM orders_raw
	GROUP BY 1, 2
	HAVING (Prod_Name = 'iPhone' AND SUM(Qty) = 7)
		OR
		(Prod_Name = 'Airpods' AND SUM(Qty) = 2)
	Order BY 1, 2
)

SELECT Customer_Name FROM tab;


