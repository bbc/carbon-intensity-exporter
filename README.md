# rd-carbon-intensity-exporter
An API wrapper and Prometheus exporter for monitoring the UK carbon intensity API: https://carbonintensity.org.uk/

## Setup
`pip install -e .`

`pip install -r requirements.txt`

## Deployment
To run the Prometheus server and expose the `/metrics` endpoint, run:

`python3 -m carbon_intensity_exporter`

## Carbon Minimiser
`carbon_minimiser/carbon_minimise.py` provides a series of optimisation functions that calculate the ideal time and 
place to perform electricity intensive operations based on the forecasts of the Carbon Intensity API.

An example of its usage can be seen in `carbon_minimiser/example_driver.py`.