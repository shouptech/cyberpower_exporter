# Copyright 2020 Mike Shoup
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


import socket
import time
import prometheus_client


def main():
    prometheus_client.start_http_server(10100)
    # Check once every second and update the prometheus gauges
    while True:
        set_prometheus_values()
        time.sleep(1)


def set_prometheus_values():
    data = get_data()
    info = prometheus_client.Info("cyberpower_info", "Information about UPS")
    info.info(
        {
            "model_name": data["model_name"],
            "firmware_num": data["firmware_num"],
            "input_rating_volut": float(data["input_rating_volt"]) / 1000,
            "output_rating_watt": float(data["output_rating_watt"]) / 1000,
        }
    )

    utility_volt = prometheus_client.Gauge(
        "utility_volt", "Voltage from the utility"
    )
    utility_volt.set(float(data["utility_volt"]) / 1000)

    output_volt = prometheus_client.Gauge("output_volt", "Voltage output")
    output_volt.set(float(data["output_volt"]) / 1000)


def get_data():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/pwrstatd.ipc")
    s.sendall(b"STATUS\n\n")
    data = s.recv(512)

    result = {}

    for line in data.decode("ascii").splitlines():
        col = line.split("=")
        result[col[0]] = col[1]

    return result
