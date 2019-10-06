
CREATE TABLE IF NOT EXISTS calendar_listing (
  listing_id INTEGER,
  year int,
  month int,
  city VARCHAR(256),
  room_type VARCHAR(32),
  accommodates VARCHAR(32),
  property_type VARCHAR(32),
  bathrooms VARCHAR(512), --
  bedrooms VARCHAR(512), --
  zipcode VARCHAR(256),
  latitude VARCHAR(32), -- TODO: handle
  longitude VARCHAR(32), -- TODO: raw to processed types
  review_scores_location FLOAT,
  review_scores_cleanliness FLOAT,
  review_scores_rating FLOAT,
  price FLOAT
);
COMMIT;

INSERT INTO calendar_listing
SELECT
  l.id AS listing_id,
  extract(year from date) as year,
  extract(month from date) as month,
  l.city,
  l.room_type,
  l.accommodates,
  l.property_type,
  l.bathrooms,
  l.bedrooms,
  l.zipcode,
  l.latitude,
  l.longitude,
  AVG(NULLIF(l.review_scores_location, '')::FLOAT),
  AVG(NULLIF(l.review_scores_cleanliness, '')::FLOAT),
  AVG(NULLIF(l.review_scores_rating, '')::FLOAT),
  AVG(NULLIF(c.price, '')::FLOAT)
FROM calendar_2 c
JOIN listings_2 l
ON c.listing_id = l.id
AND review_scores_location ~ '^\\d+$'
AND review_scores_cleanliness ~ '^\\d+$'
AND review_scores_rating ~ '^\\d+$'
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
;
COMMIT;

