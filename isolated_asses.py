import pandas as pd
    
forecasts = pd.DataFrame(
    {
        "location": ["loc1", "loc1", "loc2", "loc2"],
        "time_period": ["2023-W01", "2023-W02", "2023-W01", "2023-W02"],
        "horizon_distance": [1, 2, 1, 2],
        "sample": [1, 1, 1, 1],
        "forecast": [10, 12, 21, 23],
    }
)


observations = pd.DataFrame(
    {
        "location": ["loc1", "loc1", "loc2", "loc2"],
        "time_period": ["2023-W01", "2023-W02", "2023-W01", "2023-W02"],
        "disease_cases": [11.0, 13.0, 19.0, 21.0],
    }
)


def my_metric(forecasts: pd.DataFrame, observations: pd.DataFrame) -> pd.DataFrame:
    # sum of absolute error per location and time_period
    merged = forecasts.merge(observations, on=["location", "time_period"], how="left")
    merged["metric"] = (merged["forecast"] - merged["disease_cases"]).abs()
    return merged[["location", "time_period", "metric"]]

print(my_metric(forecasts, observations))