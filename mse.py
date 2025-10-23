import pandas as pd
from chap_core.assessment.flat_representations import (
    DataDimension, FlatForecasts, FlatObserved
)
from chap_core.assessment.metrics.base import MetricBase, MetricSpec


# -------------------------------------------
# 1) MSE per (location, time_period)
# -------------------------------------------
class MsePerTimepointMetric(MetricBase):
    spec = MetricSpec(
        output_dimensions=(DataDimension.time_period, DataDimension.location),
        metric_name="MSE (per time period)",
        metric_id="mse_per_timepoint",
        description="Squared error per (location, time_period) using mean forecast.",
    )

    def compute(self, observations: FlatObserved, forecasts: FlatForecasts) -> pd.DataFrame:
        fc_mean = (
            forecasts
            .groupby(['location', 'time_period'], as_index=False)['forecast']
            .mean()
            .rename(columns={'forecast': 'forecast_mean'})
        )

        obs = observations[['location', 'time_period', 'disease_cases']].copy()
        merged = fc_mean.merge(obs, on=['location', 'time_period'], how='inner')

        merged['metric'] = (merged['forecast_mean'] - merged['disease_cases']) ** 2

        return merged[['location', 'time_period', 'metric']]


# -------------------------------------------
# 2) MSE averaged over time per location
# -------------------------------------------
class MseByLocationMetric(MetricBase):
    spec = MetricSpec(
        output_dimensions=(DataDimension.location,),
        metric_name="MSE (mean over time)",
        metric_id="mse_by_location",
        description="Mean squared error across time periods per location using mean forecast.",
    )

    def compute(self, observations: FlatObserved, forecasts: FlatForecasts) -> pd.DataFrame:
        fc_mean = (
            forecasts
            .groupby(['location', 'time_period'], as_index=False)['forecast']
            .mean()
            .rename(columns={'forecast': 'forecast_mean'})
        )

        obs = observations[['location', 'time_period', 'disease_cases']].copy()
        merged = fc_mean.merge(obs, on=['location', 'time_period'], how='inner')

        merged['se'] = (merged['forecast_mean'] - merged['disease_cases']) ** 2

        out = (
            merged.groupby('location', as_index=False)['se']
            .mean()
            .rename(columns={'se': 'metric'})
        )

        return out[['location', 'metric']]


# ---------------------------
# Standalone runner (optional)
# ---------------------------
if __name__ == "__main__":
    forecasts_df = pd.read_csv("example_data/forecasts.csv")
    observations_df = pd.read_csv("example_data/observations.csv")

    flat_forecasts = FlatForecasts(forecasts_df)
    flat_observations = FlatObserved(observations_df)

    metric_1 = MsePerTimepointMetric()
    result_1 = metric_1.get_metric(flat_observations, flat_forecasts)
    print("\nMSE per (location, time_period):")
    print(result_1)

    metric_2 = MseByLocationMetric()
    result_2 = metric_2.get_metric(flat_observations, flat_forecasts)
    print("\nMSE mean over time per location:")
    print(result_2)
