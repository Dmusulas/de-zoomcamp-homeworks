# Homework

## Question 1

What is the count for fhv vehicle records for year 2019?

``` sql
SELECT COUNT(1)
FROM `trips.fhv_rides_2019_materialized`
```

ANSWER: 43,244,696

## Question 2

Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```sql
SELECT COUNT(DISTINCT affiliated_base_number)
FROM `trips.fhv_rides_2019_materialized`
```

For materialized table: 317.94MB
For external table: 0B

This however does not mean external table won't consume bytes, BQ just does not know how much. And actually it does process 3GBs which is much more than BQ table.
## Question 3 
How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?

```sql
SELECT COUNT(1)
FROM `trips.fhv_rides_2019_materialized`
WHERE PUlocationID IS NULL AND DOlocationID IS NULL
```

ANSWER: 717748

## Question 4
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

ANSWER: Partition by pickup_datetime Cluster by affiliated_base_number
## Question 5 
Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).
Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

**To create a partition table**
```sql
CREATE OR REPLACE TABLE `de-zoomcamp-375120.trips.fhv_rides_2019_partitioned` 
PARTITION BY DATE(pickup_datetime)
CLUSTER BY (affiliated_base_number)
AS (
SELECT *  
FROM `de-zoomcamp-375120.trips.fhv_rides_2019_materialized` )
```

Query to retrieve distinct affiliated_base_number between above mentioned dates:

```sql
SELECT DISTINCT affiliated_base_number
FROM de-zoomcamp-375120.trips.fhv_rides_2019_materialized
WHERE pickup_datetime BETWEEN "2019-03-01" AND "2019-03-31"
```

Bytes processed without partition: 648.87MB
Bytes processed with partitions: 23.05MB

## Question 6 
Where is the data stored in the External Table you created?

Answer: GCP Bucket

## Question 7
It is best practice in Big Query to always cluster your data:

Answer: FALSE

If your table is smaller than 1Gb, clustering it may cause more overhead due to metadata than it creates benefit. So costs will outweight gains.

