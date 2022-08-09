# rd-carbon-intensity-exporter
An API wrapper and Prometheus exporter for monitoring the GB carbon intensity API: https://carbonintensity.org.uk/

## Setup
`pip install -e .`

`pip install -r requirements.txt`

## Carbon Intensity Exporter

To run the Prometheus exporter server and expose the `/metrics` endpoint, run:

`python3 -m carbon_intensity_exporter`

```
curl localhost:8000/metrics
```

### Metrics

Name     | Sample Labels | Sample Value | Description
---------|---------------|--------------|------------
up |  | 1 or 0 (bool) | Boolean set to true if metrics successfully scraped from carbon intensity API
carbon_intensity | geohash="gcmm",location="N_WALES" | 203.0 gCO2/kWh(float)| Carbon intensity of location in gCO2/kWh
carbon_fuel_mix | fuel_type="biomass",geohash="gcpv",location="LONDON" | 61.3 %(float)| Fuel mix percentage of location
carbon_intensity_forecast | geohash="gcpv",location="LONDON",time="+00:30" | 203.0 gCO2/kWh(float) | Forecast of carbon intensity of location in 30min intervals

## Testing

To run tests against the Exporter, run:

`python3 -m pytest`
