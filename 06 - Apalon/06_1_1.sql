--1. Describe how the app* metrics were developing during the last year. 
--What trends do you observe?
--Provide your explanation of the trends and mention all details that may matter.

DROP TABLE IF EXISTS apalon_app_usage;
CREATE TABLE apalon_app_usage (
	day DATE,
	median_sess_len VARCHAR,
	total_time_spent VARCHAR,
	avg_sess_len VARCHAR,
	new_users INT,
	active_users INT,
	sessions INT,
	_1_sess INT,
	_2_sess INT,
	_3_4_sess INT,
	_5_6_sess INT,
	_7_9_sess INT,
	_10_14_sess INT,
	_15_19_sess INT,
	_20plus_sess INT,
	no_of_events_A INT,
	unique_users_event_A INT);

\copy apalon_app_usage FROM '/home/kostya/DA Test Tasks/06 - Apalon/06_apalon_app_usage.csv' WITH (FORMAT csv, header);

UPDATE apalon_app_usage
	SET total_time_spent = REPLACE (total_time_spent, 'yr', 'years');
UPDATE apalon_app_usage
	SET total_time_spent = REPLACE (total_time_spent, 'mo', 'months');
UPDATE apalon_app_usage
	SET total_time_spent = REPLACE (total_time_spent, 'dy', 'days');
UPDATE apalon_app_usage
	SET total_time_spent = REPLACE (total_time_spent, 'hr', 'hours');

ALTER TABLE apalon_app_usage 
	ALTER COLUMN median_sess_len TYPE INTERVAL USING (median_sess_len::INTERVAL),
	ALTER COLUMN total_time_spent TYPE INTERVAL USING (total_time_spent::INTERVAL),
	ALTER COLUMN avg_sess_len TYPE INTERVAL USING (avg_sess_len::INTERVAL);

SELECT 
	day,
	median_sess_len,
	total_time_spent,
	avg_sess_len
FROM apalon_app_usage;



