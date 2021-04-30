from prometheus_client.core import GaugeMetricFamily
from carbon_intensity_exporter.carbon_api_wrapper.carbon import CarbonAPI
import asyncio
from datetime import datetime


class Prometheus:
    def __init__(self):
        self.gauges = {
            'up': GaugeMetricFamily('up',
                                    'Collector Status',
                                    labels=["job"]),
            'intensity': GaugeMetricFamily('intensity',
                                           'Carbon Intensity',
                                           labels=["location"]),
            'fuel_mix': GaugeMetricFamily('fuel_mix',
                                          'Current Fuel Mix',
                                          labels=["location", "fuel_type"]),
            'forecast': GaugeMetricFamily('intensity_forecast',
                                          'Current Fuel Mix',
                                          labels=["location", "time"])
        }
        self.api = CarbonAPI()

    def execute_synchronously(self, func):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        t = loop.create_task(func)
        r = loop.run_until_complete(t)
        return r

    def collect(self):
        healthy = self.execute_synchronously(self.api.health_status())
        self.gauges['up'].add_metric(labels=["Carbon API Collector"], value=healthy)
        if healthy:
            api_calls = {
                "lon_int": self.api.current_region_intensity("LONDON"),
                "man_int": self.api.current_region_intensity("NW_ENGLAND"),
                "lon_mix": self.api.current_region_mix("LONDON"),
                "man_mix": self.api.current_region_mix("NW_ENGLAND"),
                "lon_forecast": self.api.region_forecast_range("LONDON", 48),
                "man_forecast": self.api.region_forecast_range("NW_ENGLAND", 48)
            }
            results = {}
            for metric, func in api_calls.items():
                # prometheus doesn't support an async collect function, so run carbon_api_wrapper calls syncronously
                results[metric] = self.execute_synchronously(func)

            timestamp = str(datetime.now().timestamp())

            self.gauges['intensity'].add_metric(labels=["london"], timestamp=timestamp, value=results['lon_int'][0])
            self.gauges['intensity'].add_metric(labels=["manchester"], timestamp=timestamp, value=results['man_int'][0])

            for fuel, percent in results['lon_mix'].items():
                self.gauges['fuel_mix'].add_metric(labels=["london", fuel], timestamp=timestamp, value=percent)
            for fuel, percent in results['man_mix'].items():
                self.gauges['fuel_mix'].add_metric(labels=["manchester", fuel], timestamp=timestamp, value=percent)

            for forecast in results['lon_forecast']:
                self.gauges['forecast'].add_metric(labels=["london",
                                                   forecast['time']],
                                                   timestamp=timestamp,
                                                   value=forecast['forecast'])
            for forecast in results['man_forecast']:
                self.gauges['forecast'].add_metric(labels=["manchester",
                                                   forecast['time']],
                                                   timestamp=timestamp,
                                                   value=forecast['forecast'])

            for name, gauge in self.gauges.items():
                yield gauge
        else:
            yield self.gauges['up']