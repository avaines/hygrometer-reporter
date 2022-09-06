#!/usr/bin/python3

class ExampleSensor:
    def __init__(self, name, poll_interval=10):
        self.sensor_name = name
        self.poll_interval = poll_interval

        self.next_poll_in_seconds = poll_interval

        self.bat_sensor = 0
        self.temp_sensor = 0
        self.hum_sensor = 0

    @property
    def status(self):
        return  "%s : temperature: %s | hummidity: %s | battery: %s" % ( self.sensor_name, self.temp_summary, self.hum_summary, self.bat_sensor )


    def fetch(self):
        self.next_poll_in_seconds -= 1

        if self.next_poll_in_seconds <= 0:
            self.main()
            self.next_poll_in_seconds = self.poll_interval

    def main(self):
        self.temp_sensor += 1
        self.hum_sensor += 1
        print(self.status)