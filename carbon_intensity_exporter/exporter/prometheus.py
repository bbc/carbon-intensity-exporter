from prometheus_client.core import GaugeMetricFamily
from carbon_intensity_exporter.carbon_api_wrapper.carbon import CarbonAPI, REGIONS
import asyncio
from datetime import datetime


class Prometheus:
    def __init__(self):
        self.gauges = {
            'up': GaugeMetricFamily('up',
                                    'Collector Status',
                                    labels=["job"]),
            'carbon_intensity': GaugeMetricFamily('carbon_intensity',
                                           'Carbon Intensity',
                                           labels=["location"]),
            'carbon_fuel_mix': GaugeMetricFamily('carbon_fuel_mix',
                                          'Current Fuel Mix',
                                          labels=["location", "fuel_type"]),
            'carbon_forecast': GaugeMetricFamily('carbon_intensity_forecast',
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

    def collect_region(self, region):
        """Collect metrics for a single region"""
        api_calls = {
            "int": self.api.current_region_intensity(region),
            "mix": self.api.current_region_mix(region),
            "forecast": self.api.region_forecast_range(region, 48),
        }

        results = {}

        for metric, func in api_calls.items():
            # prometheus doesn't support an async collect function, so run carbon_api_wrapper calls synchronously
            results[metric] = self.execute_synchronously(func)

        timestamp = str(datetime.now().timestamp())

        self.gauges['carbon_intensity'].add_metric(labels=[region], timestamp=timestamp, value=results['int'][0])

        for fuel, percent in results['mix'].items():
            self.gauges['carbon_fuel_mix'].add_metric(labels=[region, fuel], timestamp=timestamp, value=percent)

        for forecast in results['forecast']:
            self.gauges['carbon_forecast'].add_metric(labels=[region,
                                                forecast['time']],
                                                timestamp=timestamp,
                                                value=forecast['forecast'])

    def collect(self):
        healthy = self.execute_synchronously(self.api.health_status())
        self.gauges['up'].add_metric(labels=["Carbon API Collector"], value=healthy)
        if healthy:
            for region in REGIONS.keys():
                self.collect_region(region)

            for name, gauge in self.gauges.items():
                yield gauge
        else:
            yield self.gauges['up']
