# rd-carbon-intensity-exporter
An API wrapper and Prometheus exporter for monitoring the UK carbon intensity API: https://carbonintensity.org.uk/

## Setup
`pip install -e .`

`pip install -r requirements.txt`

## Deployment
To run the Prometheus server and expose the `/metrics` endpoint, run:

`python3 -m carbon_intensity_exporter`

## Carbon Minimiser
`carbon_minimiser/api/minimiser.py` provides a series of optimisation functions that calculate the ideal time and 
place to perform electricity intensive operations based on the forecasts of the Carbon Intensity API.

These optimisation functions are made available via an API, which can be launched by running:

`python3 -m carbon_minimiser`

It can also be imported directly, an example of which can be seen in `carbon_minimiser/scripts/example_driver.py`.

## Testing

To run tests against the Exporter and Minimiser, run:

`python3 -m pytest`