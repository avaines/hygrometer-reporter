#!/usr/bin/python3
from bluepy.btle import Scanner, DefaultDelegate # pylint: disable=import-error
from time import strftime
import struct

class OriaThermoBeaconSensor:
    def __init__(self, name, id, poll_interval=5, DEBUG=False):
        self.sensor_name = name
        self.sensor_id = id
        self.poll_interval = poll_interval
        self.DEBUG = DEBUG

        self.next_poll_in_seconds = poll_interval
        self.retry_count = 10

        self.uptime = 0
        self.bat_sensor = 0
        self.temp_sensor = 0
        self.hum_sensor = 0

    @property
    def status(self):

        return  "%s : temperature: %sdegC | hummidity: %s% | battery: %sV | uptime: %ssec" % ( self.sensor_name, self.temp_summary, self.hum_summary, self.bat_sensor, self.uptime )

    class DecodeErrorException(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

    class ScanDelegate(DefaultDelegate):
        def __init__(self):
            DefaultDelegate.__init__(self)

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                #print ("Discovered device", dev.addr)
                pass
            elif isNewData:
                #print ("Received new data from", dev.addr)
                pass
    

    def fetch(self):
        self.next_poll_in_seconds -= 1

        if self.next_poll_in_seconds <= 0:
            self.main()
            self.next_poll_in_seconds = self.poll_interval

    def main(self):
        scanner = Scanner().withDelegate(self.ScanDelegate())
        
        try:
            while (self.retry_count > 0):
                #print ("Initiating scan...")
                devices = scanner.scan(2.0)
                self.retry_count -= 1

                if len(devices) >= 1:
                    for dev in devices:
                        if dev.addr == self.sensor_id:
                            #print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                            manufacturer_hex = next(value for _, desc, value in dev.getScanData() if desc == 'Manufacturer')
                            manufacturer_bytes = bytes.fromhex(manufacturer_hex)

                            if len(manufacturer_bytes) == 20:
                                e6, e5, e4, e3, e2, e1, voltage, temperature_raw, humidity_raw, uptime_seconds = struct.unpack('xxxxBBBBBBHHHI', manufacturer_bytes)

                                self.temp_sensor = temperature_raw / 16.
                                self.hum_sensor = humidity_raw / 16.
                                self.bat_sensor = voltage / 1000
                                self.uptime = uptime_seconds

                            else:
                                if self.DEBUG: print ("Ignoring invalid data length for {}: {}".format(self.sensor_name,len(manufacturer_bytes)))                            
                    
        except self.DecodeErrorException:
            print("Decode Exception")
            pass 


# if __name__ == "__main__":
#     import json, time

#     sensors = json.loads(
#         '''[
#             {
#                 "mac": "63:06:00:00:09:b2",
#                 "name": "1"
#             },
#         ]'''
#     )

#     sensor_instances={}
#     for sensor in sensors:
#         sensor_instances[sensor['name']] = OriaThermoBeaconSensor(
#             name = sensor['name'],
#             id = sensor['mac'],
#             poll_interval = 1
#         )

#     # while True:
#     try:
#         for sensor in sensor_instances:
#             sensor_instances[sensor].fetch()
#             print()

#         time.sleep(1)
#     except Exception as exc:
#         print(str(exc))
#         pass

        
