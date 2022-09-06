#!/usr/bin/env python3
from influxdb import InfluxDBClient

class InfluxDbTarget:
    def __init__(self, server, port, database, username, password, DEBUG=False):
        self.DEBUG = DEBUG

        self.client = InfluxDBClient(
            host = server, 
            port = port,
            database = database
        )

    def submit_readings(self, name, temp, hum, bat, up):
        print( "Submitting InfluxDB: sensor: %s | temperature: %s | hummidity: %s | battery: %s | uptime: %s" % ( name, temp, hum, bat, up ) )

        self.client.write_points([
            {
                "measurement": "temperature", 
                "tags": {
                    "unit": "degrees",
                    "name": name
                },
                "fields": {
                    "value": temp
                }
            },
            {
                "measurement": "hummidity", 
                "tags": {
                    "unit": "percent",
                    "name": name
                    },
                "fields": {
                    "value": hum
                }
            },
            {
                "measurement": "battery", 
                "tags": {
                    "unit": "volts",
                    "name": name
                    },
                "fields": {
                    "value": bat
                }
            },
                        {
                "measurement": "uptime", 
                "tags": {
                    "unit": "seconds",
                    "name": name
                    },
                "fields": {
                    "value": up
                }
            }
        ])  
