#!/usr/bin/env python3

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class PrometheusPushToGateway:
    def __init__(self, server, port, DEBUG=False):
        self.DEBUG = DEBUG
        self.prometheus_url = "http://%s:%s" % (server, port)

    def submit_readings(self, sensor, temp, hum, bat, up):
        registry = CollectorRegistry()

        temp = Gauge('temp_celsius', 'Temperature, celsius', registry=registry, labelnames=('sensor', ))
        hum = Gauge('humidity_pct', 'Humidity, percentage', registry=registry, labelnames=('sensor', ))
        bat = Gauge('battery_voltage', 'Battery, voltage', registry=registry, labelnames=('sensor', ))
        up = Gauge('uptime', 'Uptime, seconds', registry=registry, labelnames=('sensor', ))

        temp.labels(sensor).set(temp)
        hum.labels(sensor).set(hum)
        bat.labels(sensor).set(bat)
        up.labels(sensor).set(up)

        print( "Submitting Prometheus Push-to-Gateway: sensor: %s | temperature: %s | hummidity: %s | battery: %s | uptime: %s" % ( name, temp, hum, bat, up ) )
        push_to_gateway(self.prometheus_url, job='tempBatch', grouping_key={'sensor': sensor}, registry=registry)
