from dataclasses import dataclass
from typing import Callable, Optional, Dict, List

@dataclass
class MetricMetadata:
    name: str
    display_name: str
    description: str
    formula: str
    input_type: str
    aggregation: List[str] | str

# Example usage
metrics_metadata = [
    MetricMetadata(
        name="abs_error",
        display_name="Absolute Error",
        description="Sum of absolute forecast errors",  
        formula="abs_error = sum(|Y - Y^|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "region", 
            "time"
        ],
    ), 
    MetricMetadata(
        name="abs_target_mean",
        display_name="Absolute Target Mean",
        description="Mean magnitude of true series",
        formula="abs_target_mean = mean(|Y|)",
        input_type="MultiLocationDiseaseTimeSeries",
        aggregation= [
            "time"
        ]
    ),
    MetricMetadata(
        name="abs_target_sum",
        display_name="Absolute Target Sum",
        description="Total magnitude of true series",
        formula="abs_target_sum = sum(|Y|)",
        input_type="MultiLocationDiseaseTimeSeries",
        aggregation= [
            "time"
        ]
    ),
    MetricMetadata(
        name="mse",
        display_name="Mean Squared Error",
        description="Average squared difference – heavily penalizes large errors",
        formula="mse = mean((Y - Y^ )^2)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="seasonal_error",
        display_name="Seasonal Error",
        description="Mean change over one seasonal period",
        formula="seasonal_error = mean(|Y[t] - Y[t-m]|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="mase",
        display_name="Mean Absolute Scaled Error",
        description="Error scaled by seasonal variation",
        formula="mase = mean(|Y - Y^|) / seasonal_error",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="msis",
        display_name="Mean Squared Interval Score",
        description="Interval score normalized by seasonal error",
        formula="msis = mean(U - L + 2/alpha*(L - Y)*I[Y < L] + 2/alpha*(Y - U)*I[Y > U]) / seasonal_error",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="mape",
        display_name="Mean Absolute Percentage Error",
        description="Avg. percentage error (not symmetric)",
        formula="mape = mean(|Y - Y^| / |Y|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="smape",
        display_name="Symmetric Mean Absolute Percentage Error",
        description="Avg. symmetric percentage error",
        formula="smape = 2 * mean(|Y - Y^| / (|Y| + |Y^|))",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="mae",
        display_name="Mean Absolute Error",
        description="Average absolute forecast error per observation",
        formula="mae = mean(|Y - Y^|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="coverage",
        display_name="Prediction Interval Coverage",
        description="Fraction of observations within forecast",
        formula="coverage = mean(Y <= Y^)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="quantile_loss",
        display_name="Quantile Loss",
        description="Asymmetric error loss per quantile",
        formula="quantile_loss = 2 * sum(|(Y - Y^) * (Y <= Y^) - q|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="rmse",
        display_name="Root Mean Squared Error",
        description="Square-root of the average squared error, emphasizing larger mistakes",
        formula="rmse = sqrt(mean((Y - Y^ )^2))",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation= [
            "time"
        ],
    ),
    MetricMetadata(
        name="peak_value_diff",
        display_name="Peak Value Difference",
        description="Difference between the highest observed peak and the highest predicted peak",
        formula="peak_value_diff = max(Y) - max(Y^)",
        input_type="Dict[str, {observations: MultiLocationDiseaseTimeSeries, samples: MultiLocationForecast}]",
        aggregation= [
            "dataset"
        ],
    ),
]

def get_metric_metadata(name: str):
    for meta in metrics_metadata:
        if meta.name == name:
            return meta
    return None
