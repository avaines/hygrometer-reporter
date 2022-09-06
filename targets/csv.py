#!/usr/bin/env python3
import csv
from datetime import datetime
import os

class CSVTarget:
    def __init__(self, name, path, DEBUG=False):
        self.target_name = name
        self.csvpath = "%s" % (path)
        self.DEBUG = DEBUG

        # Setup the csvfile

        if not os.path.exists(self.csvpath):
            with open(self.csvpath, 'w', newline='') as csvfile:
                fieldnames = ['sensor_name', 'timestamp', 'temperature', 'humidity', 'battery', 'uptime']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()


    def submit_readings(self, name, temp, hum, bat, up):
        print( "Submitting CSV: sensor: %s | temperature: %s | hummidity: %s | battery: %s | uptime %s" % ( name, temp, hum, bat, up ) )

        with open(self.csvpath, 'a', newline='') as csvfile:
            fieldnames = ['sensor_name', 'timestamp', 'temperature', 'humidity', 'battery', 'uptime']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'sensor_name': name, 
                'timestamp': datetime.now(),
                'temperature': temp, 
                'humidity': hum, 
                'battery': bat,
                'uptime': up
            })
