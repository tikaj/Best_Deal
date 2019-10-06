
CREATE TABLE IF NOT EXISTS calendar (
  listing_id INTEGER,
  date DATE,
  price FLOAT
)
DISTKEY(listing_id)
SORTKEY(listing_id)
;

DROP TABLE IF EXISTS _temp;

CREATE TEMP TABLE _temp (
  listing_id INTEGER,
  date DATE,
  available CHARACTER,
  price VARCHAR(32),
  adjusted_price VARCHAR(32),
  minimum_nights INTEGER,
  maximum_nights INTEGER
)
DISTKEY(listing_id)
SORTKEY(listing_id)
;

COPY _temp
FROM 's3://airbnb-1/v2/calendar/{{ city}}_{{ date }}.csv'
iam_role 'arn:aws:iam::045852796978:role/redshift_s3_read_write'
FORMAT AS CSV
IGNOREHEADER 1
FILLRECORD
;

INSERT INTO calendar
SELECT
  listing_id,
  date,
  REPLACE(
    SUBSTRING(price FROM 2),
   ',',
   ''
   )::FLOAT AS price
FROM _temp
WHERE price != ''
;

COMMIT;

ANALYZE calendar;

