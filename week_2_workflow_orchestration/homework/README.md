# Homework week 2

## Question 1

Using the etl_web_to_gcs.py flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

### Answer

run `python green_taxi_202001.py`, observe that it has 447,770 rows.

## Question 2

Cron is a common scheduling specification for workflows.

Using the flow in etl_web_to_gcs.py, create a deployment to run on the first of every month at 5am UTC. What’s the cron schedule for that?

### Answer

0 5 1 * *

## Question 3

Using etl_gcs_to_bq.py as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. This new script should not fill or remove rows with missing values. (The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color.

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

### Answer

Run the following commands:

- `prefect deployment run etl-parent-flow/docker-flow -p "months=[2,3]" -p "year=2019"` - this utilized previoud deployment made during tutorial video.
- `prefect deployment build homework/parametrized_gcs_to_bgq.py:etl_parent_flow -n gcs_to_bq --apply` create new deployment for gcs_to_bq.py file.
- prefect deployment run etl-parent-flow/gcs_to_bq -p "months=[2,3]" -p "year=2019"

Observe logs add up showing row nums.

## Question 4

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. Prefect can look in the GitHub repo to find your flow code and read it. Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image.

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

### Answer


