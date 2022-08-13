#!/usr/bin/env python3
import csv
from datetime import datetime
import os

class CSVTarget:
    def __init__(self, name, path):
        self.target_name = name
        self.csvpath = "%s" % (path)

        # Setup the csvfile

        if not os.path.exists(self.csvpath):
            with open(self.csvpath, 'w', newline='') as csvfile:
                fieldnames = ['sensor_name', 'timestamp', 'temperature', 'humidity', 'battery']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()


    def submit_readings(self, name, temp, hum, bat):
        print( "Submitting CSV: sensor: %s | temperature: %s | hummidity: %s | battery: %s" % ( name, temp, hum, bat ) )

        with open(self.csvpath, 'a', newline='') as csvfile:
            fieldnames = ['sensor_name', 'timestamp', 'temperature', 'humidity', 'battery']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'sensor_name': name, 
                'timestamp': datetime.now(),
                'temperature': temp, 
                'humidity': hum, 
                'battery': bat
            })
