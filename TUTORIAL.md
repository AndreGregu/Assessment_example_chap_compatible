Turtorial for how to implement metrics based on this example metric system
-Andre Gregussen

This system is a tutorial for how to implement metrics and components in chap. The goal of this repository-version is to learn how to implement metrics spesifically. A metric is a way of evaluating a models based on its perfromance. By comparing the truth- and prediction values, we can analyse the models performance on spesific cases.  

# Tutorial

## 1. Setting up a virtual environment

Usually we set up an environment on our comptuer that acts as a box for our dependencies, in order to keep the computer clean. This will allows us to download spesific packages for this system that does not affect the version models of other system-packages. 

In order to create a virutal environment, go to the project folder and insert the following command line code: 

```bash

User:/../ProjectFolder$ python -m venv venv

```
This creates a virtual environment in your project folder that can be activated by inserting the following command line code: 

```bash

User:/../ProjectFolder$ surce venv/bin/activate

```

In order to run source you have to be in a wsl-terminal.


## 2. Pre-requirements

There are some dependency pakages that are required in order to run this system: 

- jsonschema package

- pandera package 

Activate the virtual environment you have created in your project folder and run the following commands: 

```bash

pip install jsonschema

pip install pandera

```

## 3. Data explanation

In this tutorial based system, we use flat data in CSV files located in the following folder: 

```bash

User:/../ProjectFolder/example_data/$

```

The data is defined as "flat" because all the data lives in one table wihtout any nested lists, hierarchical structures, or multi-level JSON objects.

### 3.1 forecast.csv

The forecast data in `forecast.csv` visualizes the predictions. The first row is a header defining the fields: 

- location *(The designnated location for which the predictions are located)*

- time_period *(Which time period is beeing predicted)*

- horizon_distance *(How many months/weeks prior to the time period the prediction was made)*

- sample *(Sample identifier for several values per time_period)*

- forecast *(Prediction value)*

Each location has predictions in two seperate time sections: 

- Week 1-2 in 2023

- Week 8-9 in 2023

### 3.2 observations.csv

Similarly, the observation data visualizes the observations *(actual values)*. The first row is a header defining the fields: 

- location

- time_period

- disease_cases *(Truth value)*

The observations represent the same time sections as the prediction values.

## 4. Functionality

### 4.1 Isolated metric implementation

`isolated_asses.py` is an isolated example of how a simple metric can be implemented and run independently.
The data is hard-coded as a pandas Dataframe into the script: 

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
The forecast and observation data is then passed to the metric: 

```python

def my_metric(forecasts: pd.DataFrame, observations: pd.DataFrame) -> pd.DataFrame:

```
The error function in this example is Absolute Error which is defined as:

```bash

Absolute Error = |Forecast - Observation|

```

The forecast values are merged with the observation values where the `location` and `time_period` collumns match. 

The absolute error is calculated from the values, and a final dataframe with the columns `location`, `time_period`, and `metric` *(which is the metric error-function value)* is returned: 

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

The rest of the system teaches you have to implement a CHAP-compatible metric which is part of a larger ecosystem. The tutorial displays how to create reusable components which can be ...

### 4.2.1 example_metric.py

`example_metric.py` displays how a metric is implemented in order to be CHAP-compatible. This code uses the flat data in the `example_data` folder. 

The class definition defines a custom class named `ExampleMetric` which builds on the base class for all metrics called `MetricBase`:

```python

class ExampleMetric(MetricBase):

``` 

Each Metric requires specifications which is a requirement by the metric base class, which serves as metadata describing the metric to the framework:

```python

spec = MetricSpec(
        output_dimensions=(DataDimension.time_period, DataDimension.location),
        metric_name="Example Absolute Error",
        metric_id="example_metric",
        description="Sum of absolute error per location and time_period",
    )

```

This metric calculates Absolute Error which is the same metric which was used in `isolated_asses`.

In addition to the metric spesification, all metrics require a compute function which calculates the metric error value: 

```python

def compute(self, observations: FlatObserved, forecasts: FlatForecasts) -> pd.DataFrame:
    merged = forecasts.merge(observations, on=["location", "time_period"], how="left")
    merged["metric"] = (merged["forecast"] - merged["disease_cases"]).abs()
    return merged[["location", "time_period", "metric"]]

```

Similarly to the `isolated_asses` example, this function calculates absolute error from the values, and a final dataframe with the columns `location`, `time_period`, and `metric` *(which is the metric error-function value)* is returned. 

A noticeable difference is that this compute function receives data in the format of FlatObserved and FlatForecasts which are predefined validation classes to ensure correct structure on data dimensions imported through: 

```python

from chap_core.assessment.flat_representations import DataDimension, FlatForecasts, FlatObserved

```


## File Structure
 
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

## Implementing A New Metric

In order to implement a new metric, the structure in `example_metric.py` should be followed. 

Use `peak_value.py` as an example: 

- If the metric requires complex mathematical formulas, the calculations should be component based. 
     
    In this code, `_parse_year_week`, `_week_index`, `_week_diff`, and `_pick_peak` are examples of this. 

- The metric requires two classes since the structure of `MetricBase` only allows spesific attributes to be returned.

- One class computes the value between the peaks in each location, and the other computes the weekly lag between the peaks. 


## Flaws in this system

In order to implement the `peak_value.py´`, we have to have two seperate classes as two individual metrics. 

This is because of the structure that is allowed in `MetricBase`. We can only return one metric value to this class. 

Since this metric requires both monthly lag and peak value difference, we need two values to be returned.