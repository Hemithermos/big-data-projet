import pandas as pd

# path = "s3://nyc_processed/clean_data"
def load_raw_parquet(path:str):
    raw_data = pd.read_parquet(
        path,
        storage_options={
            "key": "minioadmin",
            "secret": "minioadmin",
            "client_kwargs": {"endpoint_url": "http://localhost:9000"}
        }
    )
    return raw_data


def clean_raw_data(raw_data:pd.DataFrame):
    # Restructuration of data
    raw_data["pickup_datetime"] = pd.to_datetime(raw_data["pickup_datetime"])
    raw_data["pickup_hour"] = raw_data["pickup_datetime"].dt.hour
    raw_data["pickup_day"] = raw_data["pickup_datetime"].dt.dayofweek

    # Filters
    clean_data = raw_data

    return clean_data

def get_features() -> list[str]:
    return []

def get_x_y(path:str):
    raw_data = load_raw_parquet(path)
    clean_data = clean_raw_data(raw_data=raw_data)

    X = clean_data[get_features()]
    y = clean_data["price"]

    return X, y
