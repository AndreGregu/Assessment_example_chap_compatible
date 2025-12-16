# Tutorial: Implementing Metrics Using the Example Metric System

*Andre Gregussen*

This tutorial demonstrates how to implement metrics and components in CHAP. The goal of this repository version is to learn how to implement metrics specifically.

A metric is a way of evaluating a model based on its performance. By comparing observed *(truth)* values with forecasted *(prediction)* values, we can analyze how well a model performs in specific scenarios.

## 1. Setting up a virtual environment

It is recommended to set up a virtual environment to isolate project dependencies and avoid conflicts with system-wide packages.

To create a virtual environment, navigate to the project folder and run:

```bash

python -m venv venv

```
This creates a virtual environment in the project directory. Activate it using:

```bash

source venv/bin/activate

```

**Note:** Activating the environment using source requires a WSL or Unix-like terminal.


## 2. Pre-requirements

The following dependency packages are required to run this system:

- `jsonschema`

- `pandera` 

Activate the virtual environment and install the dependencies:

```bash

pip install jsonschema

pip install pandera

```

## 3. Data explanation

This tutorial uses flat CSV data located in the following directory:

```bash

example_data/

```

The data is considered flat because all values exist in a single table without nested lists, hierarchical structures, or multi-level JSON objects.

### 3.1 forecast.csv

The `forecasts.csv` file contains prediction data. The header defines the following fields:

- location - *The location for which predictions are made*

- time_period - *The time period being predicted*

- horizon_distance - *How far in advance the prediction was made*

- sample - *Sample identifier for multiple predictions per time period*

- forecast - *The predicted value*

Each location contains predictions for two time periods:

- Weeks 1-2 in 2023

- Weeks 8-9 in 2023

### 3.2 observations.csv

The `observations.csv` file contains observed *(actual)* values. The fields are:

- location

- time_period

- disease_cases - *The observed (truth) value*

The observations correspond to the same time periods as the forecast data.

## 4. Functionality

### 4.1 Isolated metric implementation

`isolated_assess.py` is an isolated example demonstrating how a simple metric can be implemented and executed independently.

In this example, the forecast and observation data are hard-coded as pandas DataFrames:

```python

forecasts = pd.DataFrame(
    {
        "location": ["loc1", "loc1", "loc2", "loc2"],
        "time_period": ["2023-W01", "2023-W02", "2023-W01", "2023-W02"],
        "horizon_distance": [1, 2, 1, 2],
        "sample": [1, 1, 1, 1],
        "forecast": [10, 12, 21, 23],
    }
)


observations = pd.DataFrame(
    {
        "location": ["loc1", "loc1", "loc2", "loc2"],
        "time_period": ["2023-W01", "2023-W02", "2023-W01", "2023-W02"],
        "disease_cases": [11.0, 13.0, 19.0, 21.0],
    }
)

```
The forecast and observation data are passed to the metric function:

```python

def my_metric(forecasts: pd.DataFrame, observations: pd.DataFrame) -> pd.DataFrame:

```
The error function used in this example is **Absolute Error**, defined as:

```bash

Absolute Error = |Forecast - Observation|

```

Forecast and observation values are merged on the `location` and `time_period` columns. The absolute error is computed, and a final DataFrame containing `location`, `time_period`, and `metric` is returned:

```python

def my_metric(forecasts: pd.DataFrame, observations: pd.DataFrame) -> pd.DataFrame:
    merged = forecasts.merge(observations, on=["location", "time_period"], how="left")
    merged["metric"] = (merged["forecast"] - merged["disease_cases"]).abs()
    return merged[["location", "time_period", "metric"]]

```

In order to run the isolated example, insert the following command line code: 

```bash

User:/../ProjectFolder/$ python isolated_asses.py

```

### 4.2 CHAP-compatible metric implementation

The rest of the system teaches you have to implement a CHAP-compatible metric which is part of a larger ecosystem.

#### 4.2.1 example_metric.py

`example_metric.py` demonstrates how to implement a CHAP-compatible metric using flat data stored in the `example_data` folder. 

The class definition creates a custom metric named `ExampleMetric` which inherits from `MetricBase`, the base class for all metrics in CHAP:

```python

class ExampleMetric(MetricBase):

``` 

Each metric requires a specification *(`MetricSpec`)*, which provides metadata describing the metric to the framework:

```python

spec = MetricSpec(
        output_dimensions=(DataDimension.time_period, DataDimension.location),
        metric_name="Example Absolute Error",
        metric_id="example_metric",
        description="Sum of absolute error per location and time_period",
    )

```
This specification defines the output dimensions of the metric, a human-readable name, a unique identifier, and a description of the metric.

This metric calculates **absolute error** which, the same error metric used in the `isolated_asses` example.

In addition to the metric specification, all metrics must implement a `compute` function that performs the actual metric calculation: 

```python

def compute(self, observations: FlatObserved, forecasts: FlatForecasts) -> pd.DataFrame:
    merged = forecasts.merge(observations, on=["location", "time_period"], how="left")
    merged["metric"] = (merged["forecast"] - merged["disease_cases"]).abs()
    return merged[["location", "time_period", "metric"]]

```

This function merges forecast and observed data on `location` and `time_period`, computes the absolute error for each row, and returns a DataFrame containing the required columns: `location`, `time_period`, and `metric` *(the computed error value)*. 

A noticeable difference from the `isolated_asses` example is that the compute function receives data wrapped in `FlatObserved` and `FlatForecasts` objects, which are standardized data containers provided by CHAP. These classes enforce consistent schema and validation for observed and forecast data and are imported via:

```python

from chap_core.assessment.flat_representations import DataDimension, FlatForecasts, FlatObserved

```

#### 4.2.2 Integrating the metric in the rest of the system

To integrate a custom metric in the CHAP system, we first need to clone a working version of the CHAP-core repository locally. The official CHAP-core codebase is avaliable at: 

https://github.com/dhis2-chap/chap-core. 

A step-by-step guide on how to set up and run CHAP-core can be found here: 

https://dhis2-chap.github.io/chap-core/contributor/index.html.

Once CHAP-core is running, the new metric file should be placed in the metrics directory located at: 

```bash

chap-core/chap_core/assessment/metrics/

``` 

This directory contains all existing metrics, including the `example_metric.py` used in this tutorial. 

For the metric to be functional, it must be registered in the metrics registry. This registry is defined in the `__init__.py` file within the same metrics folder. 

First, the metric must be imported from its module. 

```python

from chap_core.assessment.metrics.example_metric import ExampleMetric

```

Next, the metric must be added to both the `__all__` list and the `available_metrics` dictionary:

```python

__all__ = [
    "ExampleMetric",
]

available_metrics = {
    "example_metric": ExampleMetric,
}

```

Registering the metric in this way allows it to be discovered, instantiated, and used throughout the CHAP assessment framework. 

## 5. File Structure
 
```bash  

project_root/

├── example_data/

│   └── forecasts.csv

│   └── observations.csv

├── example_metric.py

├── isolated_asses.py

├── README.md

├── representations.py

├── TUTORIAL.md  


```

## 6. Flaws in this system

In order to implement the `peak_value.py´`, we have to have two seperate classes as two individual metrics. 

This is because of the structure that is allowed in `MetricBase`. We can only return one metric value to this class. 

Since this metric requires both monthly lag and peak value difference, we need two values to be returned.