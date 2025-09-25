from typing import Callable, Optional, Dict, List
from representations import Forecast, DiseaseTimeSeries, MultiLocationDiseaseTimeSeries, MultiLocationForecast, \
    MultiLocationErrorTimeSeries, ErrorTimeSeries, Error



from abc import ABC, abstractmethod

# class Evaluator(ABC):
#     @abstractmethod
#     def evaluate(self, truth: DataSet, all_forecasts: dict[str, DataSet[Samples]], ) -> dict[str, DataSet[float]]:
#         pass

class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:
        pass

    def get_name(self) -> str:
        return self.__class__.__name__


class ComponentBasedEvaluator(Evaluator):
    def __init__(self, name, errorFunc, timeAggregationFunc, regionAggregationFunc, metadata,
                 seriesErrorFunc: Optional[Callable[[DiseaseTimeSeries, Forecast], Dict[str,float] | float]] = None):
        self._name = name
        self._errorFunc = errorFunc
        self._timeAggregationFunc = timeAggregationFunc
        self._regionAggregationFunc = regionAggregationFunc
        self.metadata = metadata
        self._seriesErrorFunc = seriesErrorFunc
    def get_name(self):
        return self._name

    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:

        if self._seriesErrorFunc is not None:
            evaluation_result = MultiLocationErrorTimeSeries(timeseries_dict={})
            for location in all_truths.locations():
                current_error_series = ErrorTimeSeries(observations=[])
                truth_ts = all_truths[location]
                forecast_series = all_forecasts.timeseries[location]
                out = self._seriesErrorFunc(truth_ts, forecast_series)
                # Allow either a single float or a dict[str,float]
                if isinstance(out, dict):
                    for key, val in out.items():
                        current_error_series.observations.append(
                            Error(time_period=key, value=float(val))
                        )
                else:
                    current_error_series.observations.append(
                        Error(time_period="Full_period", value=float(out))
                    )
                evaluation_result[location] = current_error_series
            # Optional region aggregation: aggregate per time_period key across locations
            if self._regionAggregationFunc is not None:
                final_eval = MultiLocationErrorTimeSeries(
                    timeseries_dict={"Full_region": ErrorTimeSeries(observations=[])}
                )
                # bucket values by time_period
                buckets: Dict[str, List[float]] = {}
                for loc in evaluation_result.locations():
                    for e in evaluation_result[loc].observations:
                        buckets.setdefault(e.time_period, []).append(e.value)
                for tp, vals in buckets.items():
                    agg = self._regionAggregationFunc(vals)
                    final_eval["Full_region"].observations.append(
                        Error(time_period=tp, value=float(agg))
                    )
                return final_eval
            return evaluation_result
        evaluation_result = MultiLocationErrorTimeSeries(timeseries_dict={})
        for location in all_truths.locations():
            current_error_series = ErrorTimeSeries(observations=[])
            forecast_series = all_forecasts.timeseries[location]
            assert len(all_truths[location].observations) == len(forecast_series.predictions)
            truth_and_forecast_series = zip(all_truths[location].observations, forecast_series.predictions)
            errors = []
            for truth,prediction in truth_and_forecast_series:

                assert truth.time_period == prediction.time_period
                errors.append( self._errorFunc(truth.disease_cases, prediction.disease_case_samples) )
                if self._timeAggregationFunc is None:

                    current_error_series.observations.append(Error(time_period=truth.time_period, value=errors[-1]))
            if self._timeAggregationFunc is not None:
                current_error_series.observations.append(Error(time_period="Full_period",
                    value=self._timeAggregationFunc(errors)))
            evaluation_result[location] = current_error_series

        if self._regionAggregationFunc is not None:
            final_evaluation_result = MultiLocationErrorTimeSeries(timeseries_dict={"Full_region" : ErrorTimeSeries(observations=[])})
            for locationvalues in evaluation_result.locationvalues_per_timepoint():
                
                aggregated_error = self._regionAggregationFunc([error.value for error in locationvalues.values()])
                final_evaluation_result["Full_region"].observations.append(Error(time_period="Full_period", value=aggregated_error))
        else:
            final_evaluation_result = evaluation_result

        return final_evaluation_result

