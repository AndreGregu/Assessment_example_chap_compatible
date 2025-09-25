from dataclasses import dataclass

@dataclass
class MetricMetadata:
    name: str
    description: str
    formula: str
    input_type: str
    aggregation: str

# Example usage
metrics_metadata = [
    MetricMetadata(
        name="abs_error",
        description="Absolute error",  
        formula="abs_error = sum(|Y - Y^|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ), 
    MetricMetadata(
        name="abs_target_mean",
        description="Absolute target mean ",
        formula="abs_target_mean = mean(|Y|)",
        input_type="MultiLocationDiseaseTimeSeries",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="abs_target_sum",
        description="Total magnitude of the true values",
        formula="abs_target_sum = sum(|Y|)",
        input_type="MultiLocationDiseaseTimeSeries",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="mse",
        description="Mean squared error",
        formula="mse = mean((Y - Y^ )^2)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="seasonal_error",
        description="Seasonal error",
        formula="seasonal_error = mean(|Y[t] - Y[t-m]|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="mase",
        description="Mean absolute scaled error",
        formula="mase = mean(|Y - Y^|) / seasonal_error",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="msis",
        description="Mean squared interval score",
        formula="msis = mean(U - L + 2/alpha*(L - Y)*I[Y < L] + 2/alpha*(Y - U)*I[Y > U]) / seasonal_error",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast", 
        aggregation="region, time",
    ),
    MetricMetadata(
        name="mape",
        description="Mean Absolute Percentage Error",
        formula="mape = mean(|Y - Y^| / |Y|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="smape",
        description="Symmetric Mean Absolute Percentage Error",
        formula="smape = 2 * mean(|Y - Y^| / (|Y| + |Y^|))",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ), 
    MetricMetadata(
        name="mae",
        description="Mean Absolute Error",
        formula="mae = mean(|Y - Y^|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="coverage",
        description="Prediction interval coverage", 
        formula="coverage = mean(Y <= Y^)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="quantile_loss",
        description="Quantile Loss",
        formula="quantile_loss = 2 * sum(|(Y - Y^) * (Y <= Y^) - q|)",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="rmse",
        description="Root Mean Squared Error",
        formula="rmse = sqrt(mean((Y - Y^ )^2))",
        input_type="MultiLocationDiseaseTimeSeries, MultiLocationForecast",
        aggregation="region, time",
    ),
    MetricMetadata(
        name="peak_value_diff",
        description="Difference between the highest observed peak and the highest predicted peak (across datasets; ties broken by earliest month).",
        formula="peak_value_diff = max(Y) - max(Y^)",
        input_type="Dict[str, {observations: MultiLocationDiseaseTimeSeries, samples: MultiLocationForecast}]",
        aggregation="dataset",
    ),
]

def get_metric_metadata(name: str):
    for meta in metrics_metadata:
        if meta.name == name:
            return meta
    return None
