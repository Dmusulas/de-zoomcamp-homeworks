#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse 
import os
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector

@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url):
    if url.endswith(".csv.gz"):
        csv_name = "yellow_tripdata_2021-01.csv.gz"
    else:
        csv_name = "output.csv"
    os.system(f"wget {url} -O {csv_name}")

    df_iter = pd.read_csv(csv_name, iterator = True, chunksize = 100000)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    return df

@task(log_prints=True)
def transform_data(df):
    print(f"Pre:missing passanger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"Post:missing passanger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, retries=3)
def ingest_data(table_name, df):
    
    connection_block = SqlAlchemyConnector.load("postgress")
    
    with connection_block.get_connection(begin=False) as engine:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
        
        df.to_sql(name=table_name, con=engine, if_exists="append")

#    while True:
#        t_start = time()
#
#        df = next(df_iter)
#
#        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
#        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
#
#        df.to_sql(name=table_name, con=engine, if_exists="append")
#
#        t_end = time()
#        print(f"inserted another chunk...took {(t_end - t_start):.3}")
#
@flow(name="Ingest flow")
def main():
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres.')
    parser.add_argument('--table_name', help='name of the table where we will write results to')
    parser.add_argument('--url', help='url of the csv file')

    params = parser.parse_args()

    table_name = params.table_name
    url = params.url

    raw_data = extract_data(url)
    data = transform_data(raw_data) 
    ingest_data(table_name, data)

if __name__ == "__main__":
    main()

