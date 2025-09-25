import math
from typing import Dict, List, Tuple, Any
from representations import (
    DiseaseTimeSeries, Forecast,
    MultiLocationDiseaseTimeSeries, MultiLocationForecast, MultiLocationErrorTimeSeries
)

def mae_error(truth: float, predictions: List[float]) -> float:
    yhat = sum(predictions) / len(predictions)
    return abs(truth - yhat)

def abs_error(truth: float, predictions: List[float]) -> float:
    yhat = sum(predictions) / len(predictions)
    return abs(truth - yhat)

def mean_across_time(errors: List[float]) -> float:
    return sum(errors) / len(errors)

def mean_across_regions(errors: List[float]) -> float:
    return sum(errors) / len(errors)

def mse_error(truth: float, predictions: List[float]) -> float:
    return (truth - sum(predictions) / len(predictions)) ** 2

def sqrt_mean_across_time(errors: List[float]) -> float:
    return math.sqrt(sum(errors) / len(errors))

def absolute_target(truth: float, predictions: List[float]) -> float:
    return abs(truth)

def sum_across_time(values: List[float]) -> float:
    return sum(values)

def sum_across_regions(values: List[float]) -> float:
    return sum(values)

def smape_error(truth: float, predictions: List[float], eps: float = 1e-8) -> float:
    yhat = sum(predictions) / len(predictions)
    return 2.0 * abs(truth - yhat) / (abs(truth) + abs(yhat) + eps)

def mape_error(truth: float, predictions: List[float], eps: float = 1e-8) -> float:
    yhat = sum(predictions) / len(predictions)
    return abs(truth - yhat) / (abs(truth) + eps)

# season length needs to be passed in implementation
def seasonal_error(truth_series: List[float], season_length: int) -> float:
    errors: List[float] = []
    for t in range(season_length, len(truth_series)):
        errors.append(abs(truth_series[t] - truth_series[t - season_length]))
    return sum(errors) / len(errors) if errors else float("nan")

def seasonal_error_series(season_length: int):
    def _series_func(ts: DiseaseTimeSeries, _fc: Forecast):
        y = [float(o.disease_cases) for o in ts.observations]
        return {"seasonal_error": seasonal_error(y, season_length)}
    return _series_func

## NEW: ----------------------------------------------------------------------

def parse_ym(date: str) -> Tuple[int, int]:
    year, month = date.split("-")
    return int(year), int(month)

def month_index(date: str) -> int:
    year, month = parse_ym(date)
    return year * 12 + (month - 1)

def month_diff(date1: str, date2: str) -> int:
    return month_index(date2) - month_index(date1)

def mean_list(list: List[float]) -> float:
    return sum(list) / len(list) if list else float("nan")

def _peak_by_value_then_earliest(pairs: List[Tuple[str, float]]) -> Tuple[str, float]:
    best_month, best_value, best_index = None, float("-inf"), None
    for month, value in pairs:
        mi = month_index(month)
        if (value > best_value) or (value == best_value and (best_index is None or mi < best_index)):
            best_month, best_value, best_index = month, value, mi
    return best_month, best_value

def find_peak_truth(ts: DiseaseTimeSeries) -> Tuple[str, int]:
    pairs = [(o.time_period, float(o.disease_cases)) for o in ts.observations]
    month, value = _peak_by_value_then_earliest(pairs)
    return month, int(value)

def find_peak_pred(fc: Forecast) -> Tuple[str, float]:
    pairs = [(s.time_period, mean_list(s.disease_case_samples)) for s in fc.predictions]
    return _peak_by_value_then_earliest(pairs)

def print_peak(name: str, list: MultiLocationErrorTimeSeries) -> None:
    print(f"\n{name}:")
    for loc in list.locations():
        vals = {e.time_period: e.value for e in list[loc].observations}
        print(f"{loc}: value_diff={vals['peak_value_diff']:.3f}, month_lag={int(vals['peak_month_lag'])}")

def find_peak_truth_multiloc(list: MultiLocationDiseaseTimeSeries) -> Tuple[str, float, str]:
    best = None  # (value, month_idx, month_str, location)
    for loc in list.locations():
        month, value = find_peak_truth(list[loc])  # (month, int)
        idx = month_index(month)
        cand = (float(value), idx, month, loc)
        if best is None or cand[0] > best[0] or (cand[0] == best[0] and cand[1] < best[1]):
            best = cand
    _, _, month, loc = best
    return month, best[0], loc

def find_peak_pred_multiloc(list: MultiLocationForecast) -> Tuple[str, float, str]:
    best = None  # (value, month_idx, month_str, location)
    for loc, fc in list.timeseries.items():
        month, value = find_peak_pred(fc)  # (month, float)
        idx = month_index(month)
        cand = (float(value), idx, month, loc)
        if best is None or cand[0] > best[0] or (cand[0] == best[0] and cand[1] < best[1]):
            best = cand
    _, _, month, loc = best
    return month, best[0], loc

def compute_cross_dataset_peak_metrics(
    datasets: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    best_truth = None  # (value, month_idx, month_str, dataset, location)
    best_pred = None   # (value, month_idx, month_str, dataset, location)
    for data_name, items in datasets.items():
        l_truth: MultiLocationDiseaseTimeSeries = items["observations"]  # type: ignore[assignment]
        l_pred: MultiLocationForecast = items["samples"]                  # type: ignore[assignment]
        truth_month, truth_val, truth_loc = find_peak_truth_multiloc(l_truth)
        pred_month, pred_val, pred_loc = find_peak_pred_multiloc(l_pred)
        truth_cand = (float(truth_val), month_index(truth_month), truth_month, data_name, truth_loc)
        pred_cand = (float(pred_val), month_index(pred_month), pred_month, data_name, pred_loc)
        if (best_truth is None or truth_cand[0] > best_truth[0]
            or (truth_cand[0] == best_truth[0] and truth_cand[1] < best_truth[1])):
            best_truth = truth_cand
        if (best_pred is None or pred_cand[0] > best_pred[0]
            or (pred_cand[0] == best_pred[0] and pred_cand[1] < best_pred[1])):
            best_pred = pred_cand
    # Unpack
    truth_val, _, truth_month, truth_ds, truth_loc = best_truth
    pred_val, _, pred_month, pred_ds, pred_loc = best_pred
    value_diff = float(truth_val - pred_val)
    month_lag = month_diff(truth_month, pred_month)
    return {
        "truth":   {"dataset": truth_ds, "location": truth_loc, "month": truth_month, "value": float(truth_val)},
        "pred":    {"dataset": pred_ds, "location": pred_loc, "month": pred_month, "value": float(pred_val)},
        "metrics": {"peak_value_diff": value_diff, "peak_month_lag": month_lag},
    }
