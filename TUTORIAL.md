Turtorial for how to implement metrics based on this example metric system
-Andre Gregussen

This system is a tutorial for how to implement metrics and components in chap. The goal of this repository-version is to learn how to implement metrics spesifically. A metric is a way of evaluating a models based on its perfromance. By comparing the truth- and prediction values, we can analyse the models performance on spesific cases.  

# Tutorial




## Pre-requirements

- install jsonschema package

- install pandera package 

```bash

pip install jsonschema

pip install pandera

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



## Functionality

`example_metric.py` displays how a metric is implemented in order to be CHAP-compatible. 

This code uses data formated in a pandas dataframe that can be found in the `example_data` folder. 

The class contains: 

- `MetricSpec()` which identifies which metric is used, in addition to relevant metadata related to the metric. 

- `def compute()` where the error function is calculated. 

The initialiser retrieves the metric, calles the function and prints the values. 



`isolated_asses.py` displays a single metric with hard-coded forecasts and predictions.

The metric recieves the data and calculates absolute error, then prints the result. 

**NOTE** This example is just an example of a metric, but not how it should be propperly implemented. 



`representations.py` defines the representations used in the system. 



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