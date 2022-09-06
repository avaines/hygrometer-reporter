#!/usr/bin/env python3

class ExampleTarget:
    def __init__(self, name, option):
        self.target_name = name
        self.option = "%s" % (option)

    def submit_readings(self, name, temp, hum, bat, up):
        print( "Submitting Example: sensor: %s | temperature: %s | hummidity: %s | battery: %s | uptime: %s" % ( name, temp, hum, bat, up ) )
