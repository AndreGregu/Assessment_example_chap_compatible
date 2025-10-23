Turtorial for how to implement metrics based on this example metric system - Andre Gregussen.

# Tutorial

## Pre-requirements

* Install pandas

* Install numpy

```bash

pip install pandas

pip install numpy scikit-learn matplotlib

```



## File Structure

```bash

project_root/

├── Minimalist_example/

│   ├── input/

│   │   ├── futureClimateData.csv

│   │   ├── futureDiseaseData.csv

│   │   ├── trainData.csv

│   ├── output/

│   │   ├── model.bin

│   │   ├── predictions.csv

│   ├── __init__.py

│   ├── isolated_run.py

│   ├── MLproject.txt

│   ├── predict.py

│   ├── train.py

├── asses_minimalist.py   (or a folder representations/)

├── evaluator.py

├── example_component_based_evaluator.py

├── example_evaluator.py

├── isolated_asses.py

├── metadata.py

├── peak_evaluator.py

├── README.md

├── representations.py

├── SMAPE_evaluator.py

└── TUTORIAL.md

```



## Functionality

`asses_minimalist.py` runs an isolated metric which is implemented in `example_evaluator.py`.

This type of metric is non-component based so the structure can not be reused, but the metric can be used as a whole thorugh imports. 

This is not optimal for implementing a CHAP-compatible metric, but serves as an example of how a metric works. 



`example_component_based_evaluator.py` stores helper functions that calculate the error for each metric. 

This code serves as a component in the component-based system of implementing metrics. 

Theese functions are imported in `isolated_asses.py` where the error functions are sendt to `evaluator.py` together with time- and region-aggregation (both optional), and metadata related to the metric which is retrieved from `metadata.py`.

`evaluator.py` has a constructor class that consists of: 

- A decorator.

- An evaluate-function where the data is evaluated on the metric error.

- A get-function to retrieve the name of the metric beeing used.

The class `ComponentBasedEvaluator` then performes the nessesary computing to calculate the errors for the data recieved.

If several `Dict`s are passed to the evaluate-function, the data will be processed differently then if it is a single Dict is passed. 

This is nessesary to process data for the metrics `peak_evaluator` and `seasonal_error`.

