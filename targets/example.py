#!/usr/bin/env python3

class ExampleTarget:
    def __init__(self, name, option):
        self.target_name = name
        self.option = "%s" % (option)

    def submit_readings(self, sensor, temp, hum, bat):
        print( "SUBMITTING EXAMPLETARGETFOR: sensor: %s | temperature: %s | hummidity: %s | battery: %s" % ( sensor, temp, hum, bat ) )
