
CREATE TABLE IF NOT EXISTS listings (
  city VARCHAR(256),
  load_date DATE,
  id INTEGER,
  room_type VARCHAR(32),
  accommodates VARCHAR(32),
  property_type VARCHAR(32),
  bathrooms VARCHAR(512), --
  bedrooms VARCHAR(512), --
  zipcode VARCHAR(256),
  latitude VARCHAR(32), -- TODO: handle
  longitude VARCHAR(32), -- TODO: raw to processed types
  review_scores_location VARCHAR(64), -- TODO: handle to INT
  review_scores_cleanliness VARCHAR(64),
  review_scores_rating VARCHAR(64)
)
DISTKEY(id)
SORTKEY(id)
;

DROP TABLE IF EXISTS _temp;

CREATE TEMP TABLE _temp (
 id INTEGER,
 listing_url VARCHAR(256),
 scrape_id VARCHAR(32),
 last_scraped VARCHAR(32),
 name VARCHAR(1024),
 summary VARCHAR(MAX),
 space VARCHAR(MAX),
 description VARCHAR(MAX),
 experiences_offered VARCHAR(MAX),
 neighborhood_overview VARCHAR(MAX),
 notes VARCHAR(MAX),
 transit VARCHAR(MAX),
 access VARCHAR(MAX),
 interaction VARCHAR(MAX),
 house_rules VARCHAR(MAX),
 thumbnail_url VARCHAR(256),
 medium_url VARCHAR(128),
 picture_url VARCHAR(512),
 xl_picture_url VARCHAR(512),
 host_id VARCHAR(512),
 host_url VARCHAR(1024),
 host_name VARCHAR(MAX),
 host_since VARCHAR(MAX),
 host_location VARCHAR(1024),
 host_about VARCHAR(MAX),
 host_response_time VARCHAR(128),
 host_response_rate VARCHAR(256),
 host_acceptance_rate VARCHAR(1024),
 host_is_superhost VARCHAR(128),
 host_thumbnail_url VARCHAR(512),
 host_picture_url VARCHAR(512),
 host_neighbourhood VARCHAR(256),
 host_listings_count VARCHAR(256),
 host_total_listings_count VARCHAR(256),
 host_verifications VARCHAR(256),
 host_has_profile_pic VARCHAR(128),
 host_identity_verified VARCHAR(256),
 street VARCHAR(1024),
 neighbourhood VARCHAR(128),
 neighbourhood_cleansed VARCHAR(256),
 neighbourhood_group_cleansed VARCHAR(256),
 city VARCHAR(1024),
 state VARCHAR(512),
 zipcode VARCHAR(256),
 market VARCHAR(128),
 smart_location VARCHAR(1024),
 country_code VARCHAR(32),
 country VARCHAR(32),
 latitude VARCHAR(32),
 longitude VARCHAR(32),
 is_location_exact VARCHAR(32),
 property_type VARCHAR(32),
 room_type VARCHAR(32),
 accommodates VARCHAR(32),
 bathrooms VARCHAR(512),
 bedrooms VARCHAR(512),
 beds VARCHAR(32),
 bed_type VARCHAR(32),
 amenities VARCHAR(2048),
 square_feet VARCHAR(32),
 price VARCHAR(32),
 weekly_price VARCHAR(512),
 monthly_price VARCHAR(32),
 security_deposit VARCHAR(32),
 cleaning_fee VARCHAR(512),
 guests_included VARCHAR(32),
 extra_people VARCHAR(32),
 minimum_nights VARCHAR(32),
 maximum_nights INTEGER,
 minimum_minimum_nights VARCHAR(16),
 maximum_minimum_nights VARCHAR(16),
 minimum_maximum_nights VARCHAR(16),
 maximum_maximum_nights VARCHAR(16),
 minimum_nights_avg_ntm VARCHAR(16),
 maximum_nights_avg_ntm VARCHAR(16),
 calendar_updated VARCHAR(16),
 has_availability VARCHAR(16),
 availability_30 VARCHAR(16),
 availability_60 VARCHAR(16),
 availability_90 VARCHAR(16),
 availability_365 VARCHAR(16),
 calendar_last_scraped VARCHAR(32),
 number_of_reviews VARCHAR(32),
 number_of_reviews_ltm VARCHAR(512),
 first_review VARCHAR(512),
 last_review VARCHAR(512),
 review_scores_rating VARCHAR(64),
 review_scores_accuracy VARCHAR(1024),
 review_scores_cleanliness VARCHAR(64),
 review_scores_checkin VARCHAR(16),
 review_scores_communication VARCHAR(16),
 review_scores_location VARCHAR(64),
 review_scores_value VARCHAR(16),
 requires_license VARCHAR(32),
 license VARCHAR(1024),
 jurisdiction_names VARCHAR(512),
 instant_bookable VARCHAR(10),
 is_business_travel_ready VARCHAR(8),
 cancellation_policy VARCHAR(32),
 require_guest_profile_picture VARCHAR(8),
 require_guest_phone_verification VARCHAR(8),
 calculated_host_listings_count INT,
 calculated_host_listings_count_entire_homes INTEGER,
 calculated_host_listings_count_private_rooms INTEGER,
 calculated_host_listings_count_shared_rooms INTEGER,
 reviews_per_month FLOAT
);

COPY _temp
FROM 's3://airbnb-1/v2/listings/{{ city}}_{{ date }}.csv'
iam_role 'arn:aws:iam::045852796978:role/redshift_s3_read_write'
FORMAT AS CSV
IGNOREHEADER 1
FILLRECORD
;

INSERT INTO listings
SELECT
  '{{ city }}' AS city,
  '{{ date }}' AS load_date,
  id AS listing_id,
  room_type,
  accommodates,
  property_type,
  bathrooms,
  bedrooms,
  zipcode,
  latitude,
  longitude,
  review_scores_location,
  review_scores_cleanliness,
  review_scores_rating
FROM _temp;

COMMIT;

ANALYZE listings;