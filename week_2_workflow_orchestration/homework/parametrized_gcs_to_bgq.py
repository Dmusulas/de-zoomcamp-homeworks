from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(month: int, year: int,color:str) -> Path:
    """Download trip data from GCS"""

    gcs_path = f'data/{color}/{color}_tripdata_{year}-{month:02}.parquet'
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path = gcs_path)

    return Path(f'{gcs_path}')

def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)

    return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-credentials")

    df.to_gbq(
        destination_table="trips_data_all.rides",
        project_id="de-zoomcamp-375120",
        credentials= gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow(log_prints=True)
def etl_gcs_to_bq(year: int, month: int, color: str):
    """Main ETL flow to load data into BigQuery from GCS"""

    path = extract_from_gcs(month, year, color)
    df = transform(path)
    print(f'Processed dataframe has {len(df)} rows')
    write_bq(df)


@flow()
def etl_parent_flow(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    for month in months:
        etl_gcs_to_bq(year, month, color)


if __name__ == "__main__":
    color="yellow"
    year=2019
    months=[2, 3]

    etl_parent_flow(months, year, color)
