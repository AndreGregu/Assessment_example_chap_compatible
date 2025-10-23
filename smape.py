import pandas as pd
from chap_core.assessment.flat_representations import DataDimension, FlatForecasts, FlatObserved
from chap_core.assessment.metrics.base import MetricBase, MetricSpec

def _smape(y_true: pd.Series, y_pred: pd.Series, eps: float = 1e-8) -> pd.Series:
    return 2.0 * (y_true - y_pred).abs() / (y_true.abs() + y_pred.abs() + eps)

# ============================================================
# 1) SMAPE per (location, time_period)
# ============================================================
class SmapePerTimepointMetric(MetricBase):
    spec = MetricSpec(
        output_dimensions=(DataDimension.time_period, DataDimension.location),
        metric_name="SMAPE (per time period)",
        metric_id="smape_per_timepoint",
        description="SMAPE per (location, time_period) using mean forecast.",
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

        merged['metric'] = _smape(merged['disease_cases'], merged['forecast_mean'])

        return merged[['location', 'time_period', 'metric']]
    
# ============================================================
# 2) SMAPE averaged over time per location
# ============================================================
class SmapeByLocationMetric(MetricBase):
    spec = MetricSpec(
        output_dimensions=(DataDimension.location,),
        metric_name="SMAPE (mean over time)",
        metric_id="smape_by_location",
        description="Mean SMAPE across time periods per location using mean forecast.",
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

        merged['smape'] = _smape(merged['disease_cases'], merged['forecast_mean'])

        out = (
            merged.groupby('location', as_index=False)['smape']
            .mean()
            .rename(columns={'smape': 'metric'})
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

    metric_1 = SmapePerTimepointMetric()
    result_1 = metric_1.get_metric(flat_observations, flat_forecasts)
    print("\nSMAPE per (location, time_period):")
    print(result_1)

    metric_2 = SmapeByLocationMetric()
    result_2 = metric_2.get_metric(flat_observations, flat_forecasts)
    print("\nSMAPE mean over time per location:")
    print(result_2)