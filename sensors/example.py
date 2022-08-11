#!/usr/bin/python3

class ExampleSensor:
    def __init__(self, name, poll_interval):
        self.sensor_name = name
        self.poll_interval = poll_interval

        self.next_poll_in_seconds = poll_interval

        self.bat_sensor = 0

        self.temp_sensor_1 = 0
        self.temp_sensor_2 = 0
        self.temp_sensor_3 = 0

        self.hum_sensor_1 = 0
        self.hum_sensor_2 = 0
        self.hum_sensor_3 = 0

    @property
    def hum_summary(self):
        return (self.hum_sensor_1 + self.hum_sensor_2 + self.hum_sensor_3 )/3

    @property
    def temp_summary(self):
        return (self.temp_sensor_1 + self.temp_sensor_2 + self.temp_sensor_3 )/3

    @property
    def status(self):
        return  "%s : temperature: %s | hummidity: %s | battery: %s" % ( self.sensor_name, self.temp_summary, self.hum_summary, self.bat_sensor )


    def fetch(self):
        self.next_poll_in_seconds -= 1

        if self.next_poll_in_seconds <= 0:
            self.main()
            self.next_poll_in_seconds = self.poll_interval


    def main(self):
        self.temp_sensor_1 += 1
        self.temp_sensor_2 += 1
        self.temp_sensor_3 += 1

        self.hum_sensor_1 += 1
        self.hum_sensor_2 += 1
        self.hum_sensor_3 += 1

        print(self.status)