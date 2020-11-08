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

import os
import socket
import time
import prometheus_client


def main():
    prometheus_client.start_http_server(10100)
    # Check once every second and update the prometheus gauges
    collectors = register_prometheus_collectors()
    while True:
        set_prometheus_values(collectors)
        time.sleep(os.getenv("CYBERPOWER_EXPORTER_POLL_INTERVAL", 5))


def register_prometheus_collectors():
    collectors = {}
    collectors["info"] = prometheus_client.Info(
        "cyberpower", "Information about UPS"
    )
    collectors["utility_volt"] = prometheus_client.Gauge(
        "cyberpower_utility_volt", "Voltage from the utility"
    )
    collectors["output_volt"] = prometheus_client.Gauge(
        "cyberpower_output_volt", "Voltage output"
    )
    collectors["diagnostic_result"] = prometheus_client.Gauge(
        "cyberpower_diagnostic_result", "Result of last diagnostic"
    )
    collectors["battery_remainingtime"] = prometheus_client.Gauge(
        "cyberpower_battery_remainingtime", "Seconds of battery time remaining"
    )
    collectors["battery_charging"] = prometheus_client.Gauge(
        "cyberpower_battery_charging", "Is battery charging"
    )
    collectors["battery_discharging"] = prometheus_client.Gauge(
        "cyberpower_battery_discharging", "Is battery discharging"
    )
    collectors["ac_present"] = prometheus_client.Gauge(
        "cyberpower_ac_present", "Is AC power present"
    )
    collectors["load"] = prometheus_client.Gauge(
        "cyberpower_load", "Load percentage"
    )
    collectors["battery_capacity"] = prometheus_client.Gauge(
        "cyberpower_battery_capacity", "Percentage of battery remaining"
    )
    collectors["input_rating_volt"] = prometheus_client.Gauge(
        "cyberpower_input_rating_volt", "Input voltage rating"
    )
    collectors["output_rating_watt"] = prometheus_client.Gauge(
        "cyberpower_output_rating_watt", "Output watts rating"
    )
    return collectors


def set_prometheus_values(collectors):
    data = get_data()
    collectors["info"].info(
        {
            "model_name": data["model_name"],
            "firmware_num": data["firmware_num"],
        }
    )
    collectors["utility_volt"].set(float(data["utility_volt"]) / 1000)
    collectors["output_volt"].set(float(data["output_volt"]) / 1000)
    collectors["diagnostic_result"].set(int(data["diagnostic_result"]))
    collectors["battery_remainingtime"].set(int(data["battery_remainingtime"]))
    collectors["battery_charging"].set(
        1 if data["battery_charging"] == "yes" else 0
    )
    collectors["battery_discharging"].set(
        1 if data["battery_discharging"] == "yes" else 0
    )
    collectors["ac_present"].set(1 if data["ac_present"] == "yes" else 0)
    collectors["load"].set(float(data["load"]) / 100000)
    collectors["battery_capacity"].set(float(data["battery_capacity"]) / 100)
    collectors["output_rating_watt"].set(
        float(data["output_rating_watt"]) / 1000
    )
    collectors["input_rating_volt"].set(
        float(data["input_rating_volt"]) / 1000
    )


def get_data():
    # Sample output:
    # state=0
    # model_name=PR750LCD
    # firmware_num=PQ6BN2001641
    # battery_volt=24000
    # input_rating_volt=120000
    # output_rating_watt=525000
    # avr_supported=yes
    # online_type=no
    # diagnostic_result=1
    # diagnostic_date=2020/03/19 15:05:30
    # power_event_result=0
    # battery_remainingtime=621
    # battery_charging=no
    # battery_discharging=no
    # ac_present=yes
    # boost=no
    # buck=no
    # utility_volt=122000
    # output_volt=122000
    # load=50000
    # battery_capacity=100

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/pwrstatd.ipc")
    s.sendall(b"STATUS\n\n")
    data = s.recv(512)

    result = {}

    for line in data.decode("ascii").splitlines():
        col = line.split("=")
        if len(col) != 2:
            continue
        result[col[0]] = col[1]

    return result
