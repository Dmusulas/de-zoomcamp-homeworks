/* Question 3: Count records  (Multiple choice)
How many taxi trips were totally made on January 15?
*/

SELECT COUNT(*)
FROM green_taxi_trips
WHERE DATE("lpep_pickup_datetime") = '2019-01-15';

/*
Question 4: Largest trip for each day (Multiple choice)
Which was the day with the largest trip distance?
*/

WITH prep AS (SELECT
	DATE("lpep_pickup_datetime")
	,MAX("trip_distance") AS max_trip_for_day
FROM green_taxi_trips
GROUP BY DATE("lpep_pickup_datetime")
)

SELECT *
FROM prep
ORDER BY max_trip_for_day DESC
LIMIT 1;

/*
Question 5: The number of passengers  (Multiple choice)
In 2019-01-01 how many trips had 2 and 3 passengers?
*/

SELECT passenger_count, COUNT(1)
FROM green_taxi_trips
WHERE DATE("lpep_pickup_datetime") = '2019-01-01'
GROUP BY passenger_count;

/*
Question 6: Largest tip (Multiple choice)
For the passengers picked up in the Astoria Zone which was the drop up zone that had the largest tip?
*/

WITH prep AS (
	SELECT zonp."Zone" AS pickup_zone,
		zond."Zone" AS dropoff_zone,
		gtt."tip_amount"
	FROM green_taxi_trips AS gtt
	JOIN zones AS zonp
		ON gtt."PULocationID" = zonp."LocationID"
	JOIN zones AS zond
		ON gtt."DOLocationID" = zond."LocationID")

SELECT dropoff_zone, tip_amount
FROM prep
WHERE pickup_zone = 'Astoria'
ORDER BY tip_amount DESC
LIMIT 1;