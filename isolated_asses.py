#from chap_core.api_types import PeriodObservation
#from chap_core.datatypes import HealthData
#from chap_core.spatio_temporal_data.temporal_dataclass import DataSet

from evaluator import ComponentBasedEvaluator
from example_component_based_evaluator import *
from example_evaluator import MAEonMeanPredictions
from peak_evaluator import PeakMetricsEvaluator
from SMAPE_evaluator import EvaluatorsonMeanPredictions
from representations import DiseaseObservation, Forecast, MultiLocationDiseaseTimeSeries, DiseaseTimeSeries, Samples, \
    MultiLocationForecast, MultiLocationErrorTimeSeries
from typing import List, Dict
from dataclasses import dataclass

#Or use HealthData class or HealthObservation class??
## TRUTH VALUES: ------------------------------------------------------
observations_a = MultiLocationDiseaseTimeSeries(
    timeseries_dict={
    "Oslo":
        DiseaseTimeSeries(observations=[
            DiseaseObservation(time_period="2020-01", disease_cases=0),
            DiseaseObservation(time_period="2020-02", disease_cases=10),
            DiseaseObservation(time_period="2020-03", disease_cases=35)]),
    "Bergen":
        DiseaseTimeSeries(observations=[
            DiseaseObservation(time_period="2020-01", disease_cases=100),
            DiseaseObservation(time_period="2020-02", disease_cases=120),
            DiseaseObservation(time_period="2020-03", disease_cases=140)])}
)

observations_b = MultiLocationDiseaseTimeSeries(
    timeseries_dict={
    "Oslo":
        DiseaseTimeSeries(observations=[    
            DiseaseObservation(time_period="2020-06", disease_cases=1),
            DiseaseObservation(time_period="2020-07", disease_cases=11),
            DiseaseObservation(time_period="2020-08", disease_cases=36)]),
    "Bergen":
        DiseaseTimeSeries(observations=[
            DiseaseObservation(time_period="2020-06", disease_cases=90),
            DiseaseObservation(time_period="2020-07", disease_cases=110),
            DiseaseObservation(time_period="2020-08", disease_cases=150)])}
)

## PREDICTION VALUES: ------------------------------------------------------
samples_a = MultiLocationForecast(
    timeseries={"Oslo":
        Forecast(predictions=[
            Samples(time_period="2020-01", disease_case_samples=[0,2]),
            Samples(time_period="2020-02", disease_case_samples=[9,13]),
            Samples(time_period="2020-03", disease_case_samples=[31,41])]),
    "Bergen":
        Forecast(predictions=[
            Samples(time_period="2020-01", disease_case_samples=[100,100]),
            Samples(time_period="2020-02", disease_case_samples=[110,120]),
            Samples(time_period="2020-03", disease_case_samples=[140,160])])}
)
samples_b = MultiLocationForecast(
    timeseries={"Oslo":
        Forecast(predictions=[
            Samples(time_period="2020-06", disease_case_samples=[1,3]),
            Samples(time_period="2020-07", disease_case_samples=[10,14]),
            Samples(time_period="2020-08", disease_case_samples=[34,44])]),
    "Bergen":
        Forecast(predictions=[
            Samples(time_period="2020-06", disease_case_samples=[90,90]),
            Samples(time_period="2020-07", disease_case_samples=[100,110]),
            Samples(time_period="2020-08", disease_case_samples=[130,150])])}
)

datasets: Dict[str, Dict[str, object]] = {
    "dataset_a": {
        "observations": observations_a,
        "samples": samples_a
    },
    "dataset_b": {
        "observations": observations_b,
        "samples": samples_b
    }
}
# samples_dataset = DataSet.from_period_observations_a(samples)
MAE_evaluator = MAEonMeanPredictions()
mae = MAE_evaluator.evaluate(observations_a, samples_a)
print(f"\nMAE: {mae}")

NEW_evaluator = EvaluatorsonMeanPredictions()
smape = NEW_evaluator.evaluate(observations_a, samples_a)
print(f"\nSMAPE: {smape}")

# ---- Example: run it on both datasets and print ----
peak_evaluator = PeakMetricsEvaluator()

peak_a = peak_evaluator.evaluate(datasets["dataset_a"]["observations"], datasets["dataset_a"]["samples"])
peak_b = peak_evaluator.evaluate(datasets["dataset_b"]["observations"], datasets["dataset_b"]["samples"])

print_peak("\nPeak metrics - dataset_a", peak_a) 
print_peak("\nPeak metrics - dataset_b", peak_b)

cross = compute_cross_dataset_peak_metrics(datasets)
print("\nCross-dataset peak metrics", cross)
## COMPONENT BASED EVALUATORS: ------------------------------------------------------

# Point forecast error: 
abs_error_timepoint_evaluator = ComponentBasedEvaluator("AbsError", abs_error, None, None)
abs_errors = abs_error_timepoint_evaluator.evaluate(observations_a, samples_a)
print(f"\nAbsolute error timepoint: {abs_errors}")

abs_target_mean_evaluator = ComponentBasedEvaluator("AbsError target mean", absolute_target, mean_across_time, None)
abs_target_mean = abs_target_mean_evaluator.evaluate(observations_a, samples_a)
print(f"\nAbsolute target mean: {abs_target_mean}")

abs_target_sum_evaluator = ComponentBasedEvaluator("AbsError target sum", absolute_target, sum_across_time, None)
abs_target_sum = abs_target_sum_evaluator.evaluate(observations_a, samples_a)
print(f"\nAbsolute target sum: {abs_target_sum}")

mse_evaluator = ComponentBasedEvaluator("MSE", mse_error, mean_across_time, None)
mse = mse_evaluator.evaluate(observations_a, samples_a)
print(f"\nMSE component-based: {mse}")

#Percentage error:
mape_evaluator = ComponentBasedEvaluator("MAPE", mape_error, mean_across_time, None)
mape = mape_evaluator.evaluate(observations_a, samples_a)
print(f"\nMAPE component-based: {mape}")

smape_component_evaluator = ComponentBasedEvaluator("SMAPE", smape_error, mean_across_time, None)
smape2 = smape_component_evaluator.evaluate(observations_a, samples_a)
print(f"\nSMAPE component-based: {smape2}")

smape_country_evaluator = ComponentBasedEvaluator("SMAPE country", smape_error, mean_across_time, mean_across_regions)
smape_country = smape_country_evaluator.evaluate(observations_a, samples_a)
print(f"\nSMAPE country: {smape_country}")

# Scaled error with seasonality (Not done):

# MAE
mae_component_evaluator = ComponentBasedEvaluator("MAE", mae_error, mean_across_time, None)
mae2 = mae_component_evaluator.evaluate(observations_a, samples_a)
print(f"\nMAE component-based: {mae2}")

mae_country_evaluator = ComponentBasedEvaluator("MAE country", mae_error, mean_across_time, mean_across_regions)
mae_country = mae_country_evaluator.evaluate(observations_a, samples_a)
print(f"\nMAE country: {mae_country}")

rmse_evaluator = ComponentBasedEvaluator("rmse", mse_error, sqrt_mean_across_time, None)
rmse = rmse_evaluator.evaluate(observations_a, samples_a)
print(f"\nRMSE component-based: {rmse}")

absError_timepoint_evaluator = ComponentBasedEvaluator("MAE timpeoint", mae_error, None, None)
mae_timepoint = absError_timepoint_evaluator.evaluate(observations_a, samples_a)
print(f"\nMAE timpeoint: {mae_timepoint}")

