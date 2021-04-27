from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from api.carbon import CarbonAPI
import asyncio

LONDON = 13
NW_ENGLAND = 3


class Prometheus:
    def __init__(self):
        self.gauges = {
                        'intensity': GaugeMetricFamily('intensity',
                                                       'Carbon Intensity',
                                                       labels=["location", "intensity"]),
                        'fuel_mix': GaugeMetricFamily('fuel_mix',
                                                      'Current Fuel Mix',
                                                      labels=["location", "fuel_type"])
                      }
        self.api = CarbonAPI()

    def execute_synchronously(self, func):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        t = loop.create_task(func)
        r = loop.run_until_complete(t)
        return r

    def collect(self):
        api_calls = {
            "lon_int": self.api.current_region_intensity(LONDON),
            "man_int": self.api.current_region_intensity(NW_ENGLAND),
            "lon_mix": self.api.current_region_mix(LONDON),
            "man_mix": self.api.current_region_mix(NW_ENGLAND)
        }

        results = {}
        for metric, func in api_calls.items():
            # prometheus doesn't support an async collect function, so run api calls syncronously
            results[metric] = self.execute_synchronously(func)

        self.gauges['intensity'].add_metric(labels=["london", "intensity"], value=results['lon_int'][0])
        self.gauges['intensity'].add_metric(labels=["manchester", "intensity"], value=results['man_int'][0])
        for fuel, percent in results['lon_mix'].items():
            self.gauges['fuel_mix'].add_metric(labels=["london", fuel], value=percent)
        for fuel, percent in results['man_mix'].items():
            self.gauges['fuel_mix'].add_metric(labels=["manchester", fuel], value=percent)

        for name, gauge in self.gauges.items():
            yield gauge


def main():
    REGISTRY.register(Prometheus())
    import time
    while True:
        time.sleep(10)


if __name__ == '__main__':
    start_http_server(8000)
    main()
