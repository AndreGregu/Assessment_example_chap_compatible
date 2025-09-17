from evaluator import Evaluator
from representations import (
    MultiLocationDiseaseTimeSeries, 
    MultiLocationForecast, 
    MultiLocationErrorTimeSeries,
    ErrorTimeSeries, 
    Error,
)

def mean(samples):
    return sum(samples)/len(samples)

def smape_pair(y, yhat, eps: float = 1e-8):
    return 2.0 * abs(y - yhat) / (abs(y) + abs(yhat) + eps)

def mape_pair(y, yhat, eps: float = 1e-8):
    return abs(y - yhat) / (abs(y) + eps)

class EvaluatorsonMeanPredictions(Evaluator):
    def evaluate(self, 
                 all_truths: MultiLocationDiseaseTimeSeries, 
                 all_forecasts: MultiLocationForecast
                 ) -> MultiLocationErrorTimeSeries:

        evaluation_result = MultiLocationErrorTimeSeries(timeseries_dict={})

        for location in all_truths.locations(): 
            truth_series = all_truths[location]
            forecast_series = all_forecasts.timeseries[location]

            assert len(truth_series.observations) == len(forecast_series.predictions), (len(truth_series.observations), len(forecast_series.predictions))

            truth_and_forecast_series = zip(truth_series.observations, forecast_series.predictions)

            smape_sum = 0.0 
            n = 0

            for truth, prediction in truth_and_forecast_series:
                assert truth.time_period == prediction.time_period, (truth.time_period, prediction.time_period)
                y = truth.disease_cases
                y_hat = mean(prediction.disease_case_samples)
                smape_sum += smape_pair(y, y_hat)
                n += 1

            smape_mean = smape_sum / n if n > 0 else float("nan")

            evaluation_result[location] = ErrorTimeSeries(
                observations=[Error(time_period="Full_period", value=smape_mean)]
            )

        return evaluation_result
    
