#!/usr/bin/env python3

import sys
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class PrometheusPushToGateway:
    def __init__(self, server, port):
        self.prometheus_url = "http://%s:%s"

    def submit_readings(self, sensor, temp, hum, bat):
        registry = CollectorRegistry()

        t = Gauge('temp_celsius', 'Temperature, celsius', registry=registry, labelnames=('sensor', ))
        h = Gauge('humidity_pct', 'Humidity, percentage', registry=registry, labelnames=('sensor', ))
        bv = Gauge('battery_voltage', 'Battery, voltage', registry=registry, labelnames=('sensor', ))

        t.labels(sensor).set(temp)
        h.labels(sensor).set(hum)
        bv.labels(sensor).set(bat)

        push_to_gateway(self.prometheus_url, job='tempBatch', grouping_key={'sensor': sensor}, registry=registry)
