#!/usr/bin/python3

from unicodedata import name
import yaml
import time

target_instances = {}
sensor_instances = {}
sensor_targets = {}

with open("sensor_config.yml", "r") as stream:
    config = yaml.safe_load(stream)
    DEBUG = config["debug"] if 'debug' in config else False
    if DEBUG: print("Debugging enabled")

def initalise():
    with open("sensor_config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)

            #  Set up the Targets
            for target in config['targets']:

                if target['target'] == 'example':
                    print("Initialising Example target")

                    from targets.example import ExampleTarget
                    target_instances[target['target']] = ExampleTarget(
                        name = target['target'],
                        option = target['options']['option'],
                    )

                elif target['target'].startswith('csv'):
                    print("Initialising CSV target: ", target['options']['path'])

                    from targets.csv import CSVTarget
                    target_instances[target['target']] = CSVTarget(
                        name = target['target'],
                        path = target['options']['path'],
                    )

                elif target['target'] == "prometheus-push":
                    print("Initialising Prometheus (Push To Gatway)")

                elif target['target'] == "innodb":
                    print("Initialising Innodb")

                else:
                    print("Error: %s is an unknown target" % (target['target']))

            #  Set up the Sensors
            for sensor in config['sensors']:
                if sensor['type'] == 'example':
                    print("Sensor %s is an example, starting collection" % (sensor['name']))

                    from sensors.example import ExampleSensor
                    sensor_targets[sensor['name']] = sensor['targets']
                    sensor_instances[sensor['name']] = ExampleSensor(
                        name = sensor['name'],
                        poll_interval = sensor['poll_interval']
                    )

                elif sensor['type'] == 'oria-thermobeacon':
                    print("Sensor %s is a oria-thermobeacon, starting collection" % (sensor['name']))

                    from sensors.oria_thermobeacon_dot import OriaThermoBeaconSensor
                    sensor_targets[sensor['name']] = sensor['targets']
                    sensor_instances[sensor['name']] = OriaThermoBeaconSensor(
                        name = sensor['name'],
                        id = sensor['options']['id'],
                        poll_interval = sensor['poll_interval']
                    )

                elif sensor['type'] == 'hive':
                    print("Sensor %s is a Hive device, starting collection" % (sensor['name']))

                else:
                    print("%s is a unknown sensor type" % (sensor['name']))

            print()

        except yaml.YAMLError as exc:
            if DEBUG: print("sensor_config.yml could not be loaded")
            print(exc)

def main():
    while True:
        for si in sensor_instances:
            this_sensor_instance = sensor_instances[si]
            this_sensor_instance.fetch()

            # If the poll_interval and the next_poll_in_seconds are the same, it means its either the very first one or the latest tick
            if this_sensor_instance.next_poll_in_seconds == this_sensor_instance.poll_interval:
                
                if DEBUG: print (" Submitting tmp:%i hum:%i bat:%i up:%i" % (this_sensor_instance.temp_sensor, this_sensor_instance.hum_sensor, this_sensor_instance.bat_sensor, this_sensor_instance.uptime))
                
                for st in sensor_targets[si]:
                    # For each of the targets for this sensor, submit the readings
                    target_instances[st].submit_readings(
                        name = this_sensor_instance.sensor_name,
                        temp = this_sensor_instance.temp_sensor,
                        hum = this_sensor_instance.hum_sensor,
                        bat = this_sensor_instance.bat_sensor,
                        up = this_sensor_instance.uptime,
                    )

            # How long till the next tick for this sensor?
            else:
                if DEBUG: print(" Time remaining for next %s tick: %i seconds" % (this_sensor_instance.sensor_name, this_sensor_instance.next_poll_in_seconds) )

        time.sleep(1)

if __name__ == "__main__":
    initalise()
    main()