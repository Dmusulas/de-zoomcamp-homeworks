from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries = 3, cache_key_fn= task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas Dataframe
    """

    df = pd.read_csv(dataset_url, encoding="latin1")
    return df

@task(log_prints=True)
def clean(df:pd.DataFrame, color: str) -> pd.DataFrame:
    """Fix some dtype issues"""
    if color == "yelow":
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    elif color == "green":
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    elif color == "fhv":
        pass
    print(df.head(2))
    print(f'Columns are: {df.dtypes}')
    print(f'Rows: {len(df)}')

    return df

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str, storage_format:str) -> Path:
    """Write DataFrame out locally as a parquet file."""
    if storage_format == "parquet":
        path = Path(f'data/{color}/{dataset_file}.parquet.gzip')
        df.to_parquet(path)

    elif storage_format == "csv":
        path = Path(f'data/{color}/{dataset_file}.csv.gzip')
        df.to_csv(path, encoding = "utf-8")

    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS."""

    gcp_cloud_storage_bucket_block = GcsBucket.load("zoom-gcs")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path=path,
        to_path=path
    )

    return

@flow()
def etl_web_to_gcs(year: int, month: int, color: str, storage_format: str) -> None:
    """The main ETL function"""
    dataset_file = f'{color}_tripdata_{year}-{month:02}'
    dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz'
    
    df = fetch(dataset_url)
    df_clean = clean(df, color)
    path = write_local(df_clean, color, dataset_file, storage_format)
    write_gcs(path)

@flow()
def etl_parent_flow(
        months: list[int] = [1, 2], year: int = 2021, color: str = "yellow", 
        storage_format: str = "csv" 
):
    for month in months:
        etl_web_to_gcs(year, month, color, storage_format)

if __name__ == "__main__":
    color = "fhv"
    months = [1, 2, 3]
    year = 2021
    storage_format = "csv"
    etl_parent_flow(months, year, color, storage_format)
