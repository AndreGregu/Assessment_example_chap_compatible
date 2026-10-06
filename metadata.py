"""Aggregation levels the metric SUPPORTS, not the levels a given
evaluator applies. An evaluator built from this metric may use any
subset of them, including none."""

from dataclasses import dataclass
from typing import Dict, List, Optional
 
 
@dataclass
class MetricMetadata:
    name: str
    display_name: str
    description: str
    formula: str
    input_type: str
    aggregation: List[str] | str
 
metrics_metadata = [
    # ---- point-error metrics -------------------------------------
    MetricMetadata(
        name="abs_error",
        display_name="Absolute Error",
        description="Absolute error per observation, scored against the "
                    "sample mean",
        formula="abs_error_t = |y_t - mean(x_t)|",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region", "time"],
    ),
    MetricMetadata(
        name="mae",
        display_name="Mean Absolute Error",
        description="Mean absolute error, scored against the sample mean",
        formula="mae = mean_t(|y_t - mean(x_t)|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region", "time"],
    ),
    MetricMetadata(
        name="mse",
        display_name="Mean Squared Error",
        description="Mean squared error; penalises large errors more heavily "
                    "than absolute error does",
        formula="mse = mean_t((y_t - mean(x_t))^2)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region", "time"],
    ),
    MetricMetadata(
        name="rmse",
        display_name="Root Mean Squared Error",
        description="Square root of the mean squared error, reported in the "
                    "units of the observations",
        formula="rmse = sqrt(mean_t((y_t - mean(x_t))^2))",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region", "time"],
    ),
 
    # ---- percentage-error metrics --------------------------------
    MetricMetadata(
        name="mape",
        display_name="Mean Absolute Percentage Error",
        description="Mean absolute error relative to the observation; "
                    "undefined when y_t = 0",
        formula="mape = mean_t(|y_t - mean(x_t)| / |y_t|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region", "time"],
    ),
    MetricMetadata(
        name="smape",
        display_name="Symmetric Mean Absolute Percentage Error",
        description="Error relative to the sum of observation and forecast; "
                    "not symmetric in the sense the name suggests, and "
                    "unstable near zero",
        formula="smape = 2 * mean_t(|y_t - mean(x_t)| "
                "/ (|y_t| + |mean(x_t)|))",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region", "time"],
    ),
 
    # ---- target-magnitude summaries (observations only) ----------
    MetricMetadata(
        name="abs_target_mean",
        display_name="Absolute Target Mean",
        description="Mean magnitude of the observed series; a denominator "
                    "for scale-free metrics, not an error measure",
        formula="abs_target_mean = mean_t(|y_t|)",
        input_type="MultiLocationDiseaseTimeSeries",
        aggregation=["region", "time"],
    ),
    MetricMetadata(
        name="abs_target_sum",
        display_name="Absolute Target Sum",
        description="Total magnitude of the observed series; a denominator "
                    "for scale-free metrics, not an error measure",
        formula="abs_target_sum = sum_t(|y_t|)",
        input_type="MultiLocationDiseaseTimeSeries",
        aggregation=["region", "time"],
    ),
    MetricMetadata(
        name="seasonal_error",
        display_name="Seasonal Error",
        description="Mean absolute change across one seasonal period; the "
                    "scaling denominator used by MASE, not an error measure",
        formula="seasonal_error = mean_t(|y_t - y_{t-s}|)",
        input_type="MultiLocationDiseaseTimeSeries",
        aggregation=["region", "time"],
    ),
 
    # ---- peak-based ----------------------------------------------
    # Both are produced by one seriesErrorFunc (peak_series_error) but
    # are declared separately: they are in different units and use
    # opposite sign conventions.
    MetricMetadata(
        name="peak_value_diff",
        display_name="Peak Value Difference",
        description="Observed peak value minus predicted peak value; "
                    "positive means the forecast under-predicts the peak",
        formula="peak_value_diff = y_{t*} - mean(x_{t^}), "
                "t* = argmax_t y_t, t^ = argmax_t mean(x_t)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region"],
    ),
    MetricMetadata(
        name="peak_month_lag",
        display_name="Peak Month Lag",
        description="Signed number of months from the observed peak to the "
                    "predicted peak; positive means the forecast peaks late",
        formula="peak_month_lag = t^ - t*, "
                "t* = argmax_t y_t, t^ = argmax_t mean(x_t)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation=["region"],
    ),
    MetricMetadata(
        name="peak_value_diff_cross_dataset",
        display_name="Peak Value Difference (cross-dataset)",
        description="Difference between the single largest observed peak and "
                    "the single largest predicted peak, taken across all "
                    "locations and datasets",
        formula="peak_value_diff_cross = max_{d,l,t}(y) "
                "- max_{d,l,t}(mean(x))",
        input_type="Dict[str, {observations: MultiLocationDiseaseTimeSeries, "
                   "samples: MultiLocationForecast}]",
        aggregation=["dataset"],
    ),
]
 
 
def get_metric_metadata(name: str) -> Optional[MetricMetadata]:
    for meta in metrics_metadata:
        if meta.name == name:
            return meta
    return None
 
 
_by_name: Dict[str, MetricMetadata] = {m.name: m for m in metrics_metadata}
assert len(_by_name) == len(metrics_metadata), "duplicate metric name"
