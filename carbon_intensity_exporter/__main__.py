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

from carbon_intensity_exporter.exporter.prometheus import Prometheus
from prometheus_client import start_http_server
import time
from prometheus_client.core import REGISTRY
import argparse


def main(port):
    start_http_server(port)
    REGISTRY.register(Prometheus())
    while True:
        time.sleep(10)


parser = argparse.ArgumentParser()
parser.add_argument('-p')
args = parser.parse_args()
if args.p:
    port = int(args.p)
else:
    port = 8000

main(port)
