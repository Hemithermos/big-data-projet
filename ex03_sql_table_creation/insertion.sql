BEGIN;



-- dim vendor
INSERT INTO dim_vendor (vendor_id, vendor_name) VALUES
    (0, 'Unknown'),
    (1, 'Creative Mobile Technologies, LLC'),
    (2, 'Curb Mobility, LLC'),
    (6, 'Myle Technologies Inc'),
    (7, 'Helix')
ON CONFLICT (vendor_id) DO NOTHING;


-- dim ratecode
INSERT INTO dim_ratecode (ratecode_id, ratecode_label) VALUES
    (1 , 'Standard rate'),
    (2 , 'JFK'),
    (3 , 'Newark'),
    (4 , 'Nassau or Westchester'),
    (5 , 'Negotiated fare'),
    (6 , 'Group ride'),
    (99 , 'Null/unknown')
ON CONFLICT (ratecode_id) DO NOTHING;

-- dim payment type
INSERT INTO dim_payment_type (payment_type_id, payment_type_label) VALUES
    (0, 'Flex Fare trip'),
    (1, 'Credit card'),
    (2, 'Cash'),
    (3, 'No charge'),
    (4, 'Dispute'),
    (5, 'Unknown'),
    (6, 'Voided trip')
ON CONFLICT (payment_type_id) DO NOTHING;

-- store and fwd flag
INSERT INTO dim_store_and_fwd (store_and_fwd_flag, label) VALUES
  ('Y', 'Store and forward trip'),
  ('N', 'Not a store and forward trip')
ON CONFLICT (store_and_fwd_flag) DO NOTHING;

-- date
INSERT INTO dim_date (date_key, full_date, year, month, day, day_of_week, is_weekend)
SELECT
  to_char(d::date, 'YYYYMMDD')::int AS date_key,
  d::date AS full_date,
  extract(year from d)::smallint AS year,
  extract(month from d)::smallint AS month,
  extract(day from d)::smallint AS day,
  extract(isodow from d)::smallint AS day_of_week,
  (extract(isodow from d) IN (6, 7)) AS is_weekend
FROM generate_series(date '2025-01-01', date '2025-12-31', interval '1 day') AS d
ON CONFLICT (date_key) DO NOTHING;

-- DIM_TIME : une ligne par seconde (00:00:00 -> 23:59:59)
INSERT INTO dim_time (time_key, full_time, hour, minute, second)
SELECT
  ( (s / 3600) * 10000 + ((s % 3600) / 60) * 100 + (s % 60) )::int             AS time_key,
  make_time((s / 3600)::int, ((s % 3600) / 60)::int, (s % 60)::double precision) AS full_time,
  (s / 3600)::smallint                                                         AS hour,
  ((s % 3600) / 60)::smallint                                                  AS minute,
  (s % 60)::smallint                                                           AS second
FROM generate_series(0, 86399) AS s
ON CONFLICT (time_key) DO NOTHING;



TRUNCATE TABLE dim_zone, fact_trip CASCADE;

\copy dw.dim_zone(location_id, borough, zone_name, service_zone) FROM 'data/external/taxi_zone_lookup.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"');



COMMIT;