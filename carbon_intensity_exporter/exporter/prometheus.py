# Copyright 2022 British Broadcasting Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from prometheus_client.core import GaugeMetricFamily
from carbon_intensity_exporter.carbon_api_wrapper.carbon import CarbonAPI, REGIONS
import asyncio
from datetime import datetime

REGION_GEOHASH = {
    'N_SCOTLAND': "gfk8", 'S_SCOTLAND': "gfj0", 'NW_ENGLAND': "gcw2", 'NE_ENGLAND': "gcy8", 'YORKSHIRE': "gcx4", 'N_WALES': "gcmm", 'S_WALES': "gcjt",
    'W_MIDLANDS': "gcqf", 'E_MIDLANDS': "gcrs", 'E_ENGLAND': "u129", 'SW_ENGLAND': "gcj3", 'S_ENGLAND': "gcnf", 'LONDON': "gcpv",
    'SE_ENGLAND': "u107"
}

class Prometheus:
    def __init__(self):
        self.gauges = {}
        self.api = CarbonAPI()

    async def execute_collect_region(self):
        await asyncio.gather(*(self.collect_region(region) for region in REGIONS.keys()))

    async def collect_region(self, region):
        """Collect metrics for a single region"""
        api_calls = {
            "int": self.api.current_region_intensity(region),
            "mix": self.api.current_region_mix(region),
            "forecast": self.api.region_forecast_range(region, 48),
        }

        results = {}

        for metric, func in api_calls.items():
            # prometheus doesn't support an async collect function, so run carbon_api_wrapper calls synchronously
            result = await func
            if result is None:
                return
            results[metric] = result

        timestamp = str(datetime.now().timestamp())

        self.gauges['carbon_intensity'].add_metric(labels=[region, REGION_GEOHASH.get(region,"")], timestamp=timestamp, value=results['int'][0])

        for fuel, percent in results['mix'].items():
            self.gauges['carbon_fuel_mix'].add_metric(labels=[region, REGION_GEOHASH.get(region,""), fuel], timestamp=timestamp, value=percent)

        for forecast in results['forecast']:
            self.gauges['carbon_forecast'].add_metric(labels=[
                                                region,
                                                REGION_GEOHASH.get(region,""),
                                                forecast['time']],
                                                timestamp=timestamp,
                                                value=forecast['forecast'])

    def collect(self):
        self.gauges = {
            'up': GaugeMetricFamily('up',
                                    'Collector Status',
                                    labels=["job"]),
            'carbon_intensity': GaugeMetricFamily('carbon_intensity',
                                           'Carbon Intensity',
                                           labels=["location", "geohash"]),
            'carbon_fuel_mix': GaugeMetricFamily('carbon_fuel_mix',
                                          'Current Fuel Mix',
                                          labels=["location", "geohash", "fuel_type"]),
            'carbon_forecast': GaugeMetricFamily('carbon_intensity_forecast',
                                          'Current Fuel Mix',
                                          labels=["location", "geohash", "time"])
        }
        healthy = asyncio.run(self.api.health_status())
        self.gauges['up'].add_metric(labels=["Carbon API Collector"], value=healthy)
        if healthy:
            asyncio.run(self.execute_collect_region())

            for name, gauge in self.gauges.items():
                yield gauge
        else:
            yield self.gauges['up']
