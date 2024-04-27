DROP TABLE IF EXISTS history;

CREATE TABLE history (
	customer_id INT,
	membership_start_date DATE,
	membership_end_date DATE,
	membership_status VARCHAR(10));

\copy history FROM 'transitions.csv' WITH (FORMAT csv, header);

SELECT * FROM history LIMIT 20;
ALTER TABLE history ADD COLUMN id SERIAL PRIMARY KEY;
SELECT * FROM history LIMIT 20;


CREATE TABLE transitions AS (
	WITH tab AS (
		SELECT 
			h.id,
			h.customer_id,
			h.membership_end_date AS change_date,
			h.membership_status AS ms,
			ex.membership_status AS sh_ms
		FROM history AS h
		LEFT JOIN history AS ex ON h.id = ex.id - 1
		--LIMIT 20
	)

	SELECT
		id,
		customer_id,
		change_date,
		CASE
			WHEN (ms = 'Free') AND (sh_ms = 'Paid') THEN 'Convert'
			WHEN (ms = 'Paid') AND (sh_ms = 'Free') THEN 'ReverseConvert'
			WHEN (ms = 'Paid') AND (sh_ms = 'Non-member') THEN 'Cancel'
			WHEN (ms = 'Free') AND (sh_ms = 'Non-member') THEN 'Cancel'
			WHEN (ms = 'Non-member') AND (sh_ms = 'Paid') THEN 'ColdStart'
			WHEN (ms = 'Non-member') AND (sh_ms = 'Free') THEN 'WarmStart'
			WHEN (ms = 'Paid') AND (sh_ms = 'Paid') THEN 'Renewal'
			WHEN (ms = 'Free') AND (sh_ms = 'Free') THEN 'Renewal'
			END AS event
	FROM tab
);

DELETE FROM transitions WHERE event IS NULL;
SELECT * FROM transitions ORDER BY id DESC LIMIT 10;

