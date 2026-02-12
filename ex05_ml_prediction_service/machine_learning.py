from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np
import argparse
import sys

from data_preprocessing import get_x_y

SEED = 42
SAVE_PATH = "models/random_forest_model.joblib"

def train_model(X_train, y_train):

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=SEED,
        n_jobs=-1
    )

    print("Training Phase of RandomForestRegressor")
    model.fit(X_train, y_train)
    return model

def test_model(model:RandomForestRegressor, X_test, y_test):
    print("Testing Phase of RandomForestRegressor")
    preds = model.predict(X_test)
    # RMSE: Root Mean Square Error = (MSE)**1/2
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    return rmse

def save_model(model:RandomForestRegressor):
    joblib.dump(model, SAVE_PATH)

def main(path:str):
    print("Loading Clean Data: X=inputs, y=labels")
    X, y = get_x_y(path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

    model = train_model(X_train,y_train)
    rmse = test_model(model, X_test, y_test)
    print(f"RMSE: {rmse}")
    if rmse < 10:
        save_model(model)
    else:
        print("Current ML model not saved for underperforming, RMSE should be under 10!")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    args = p.parse_args()

    if args.data.endswith(".parquet"):
        main(args.data)
    else:
        print(f"Data format required: path/to/data/*.parquet (Given: {args.data})\n P.S: Data should be placed/located in ../data/processed/ or ../data/interim/")
        sys.exit(1)
