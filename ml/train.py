import os
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

import joblib

# ===============================
# CONFIG
# ===============================
TARGET_COL = os.environ.get("TARGET_COL", "ratings_count")
DATA_CSV = os.environ.get("DATA_CSV", "data/sample.csv")

MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

RANDOM_STATE = 42


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    if "released" in df.columns:
        released_dt = pd.to_datetime(df["released"], errors="coerce")
        df["release_year"] = released_dt.dt.year
        df["release_month"] = released_dt.dt.month
    else:
        df["release_year"] = np.nan
        df["release_month"] = np.nan
    return df


def select_features(df: pd.DataFrame) -> pd.DataFrame:
    features = [
        "rating",
        "rating_top",
        "metacritic",
        "added",
        "playtime",
        "reviews_text_count",
        "suggestions_count",
        "reddit_count",
        "twitch_count",
        "youtube_count",
        "has_website",
        "release_year",
        "release_month",
    ]

    for col in features:
        if col not in df.columns:
            df[col] = np.nan

    X = df[features].copy()

    if "has_website" in X.columns:
        X["has_website"] = X["has_website"].astype("float64")

    return X


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = pd.read_csv(DATA_CSV)
    if TARGET_COL not in df.columns:
        raise ValueError(f"Target column '{TARGET_COL}' not found in dataset")

    df = add_date_features(df)

    y_raw = df[TARGET_COL].fillna(0).astype("float64")
    y = np.log1p(y_raw)

    X = select_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("rf", RandomForestRegressor(
                n_estimators=200,
                random_state=RANDOM_STATE,
                n_jobs=-1
            )),
        ]
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        "target": TARGET_COL,
        "transform": "log1p",
        "model": "RandomForestRegressor",
        "rows": int(df.shape[0]),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "r2": float(r2_score(y_test, y_pred)),
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    joblib.dump(model, MODEL_PATH)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Training complete")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
