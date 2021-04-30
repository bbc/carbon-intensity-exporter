from carbon_intensity_exporter.exporter.prometheus import Prometheus
from prometheus_client import start_http_server
import time
from prometheus_client.core import REGISTRY


def main():
    start_http_server(8000)
    REGISTRY.register(Prometheus())
    while True:
        time.sleep(10)


main()
