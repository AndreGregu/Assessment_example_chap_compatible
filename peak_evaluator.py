# ADD these imports near the top with your others:
from evaluator import Evaluator  # base class
from example_component_based_evaluator import find_peak_truth, find_peak_pred, month_diff  # helpers
from representations import MultiLocationDiseaseTimeSeries, MultiLocationForecast, \
    MultiLocationErrorTimeSeries, ErrorTimeSeries, Error


# ------- Peak metrics evaluator (value diff + month lag) -------
class PeakMetricsEvaluator(Evaluator):
    """
    For each location, emits two Error entries:
      - time_period='peak_value_diff' with value = truth_peak_value - pred_peak_mean_value
      - time_period='peak_month_lag' with value = months between truth_peak_month and pred_peak_month
        (positive if prediction peaks LATER than truth, negative if earlier)
    """
    def evaluate(self, all_truths: MultiLocationDiseaseTimeSeries, all_forecasts: MultiLocationForecast) -> MultiLocationErrorTimeSeries:
        result = MultiLocationErrorTimeSeries(timeseries_dict={})
        for loc in all_truths.locations():
            truth_ts = all_truths[loc]
            pred_fc  = all_forecasts.timeseries[loc]

            # optional sanity check if you expect same length:
            assert len(truth_ts.observations) == len(pred_fc.predictions), f"Length mismatch for {loc}"

            t_month, t_val = find_peak_truth(truth_ts)
            p_month, p_val = find_peak_pred(pred_fc)

            value_diff = float(t_val - p_val)
            month_lag  = float(month_diff(t_month, p_month))

            result.timeseries_dict[loc] = ErrorTimeSeries(observations=[
                Error(time_period="peak_value_diff", value=value_diff),
                Error(time_period="peak_month_lag", value=month_lag),
            ])
        return result
