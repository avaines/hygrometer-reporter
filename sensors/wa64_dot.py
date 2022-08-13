#!/usr/bin/python3
from bluepy import btle

class WA64HygrometerDot:
    def __init__(self, name, id, poll_interval):
        self.sensor_name = name
        self.sensor_id = id
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
        # Transmit Handle 0x0021
        TX_CHAR_UUID = btle.UUID('0000fff5-0000-1000-8000-00805F9B34FB')

        # Read Handle 0x0024
        RX_CHAR_UUID = btle.UUID('0000fff3-0000-1000-8000-00805F9B34FB')

        def write_bytes(vals):
            write_val = bytearray.fromhex(vals)
            tx.write(write_val)
            read_val = rx.read()
            return read_val
        
        def convert_to_readings(response):
            readings = []
            for v in range(6):
                results_position = 6 + (v * 2)
                reading = int.from_bytes(response[results_position:results_position+2],byteorder='little')
                reading = reading * 0.0625
                if reading > 2048:
                    reading = -1 * (4096-reading)
                # readings.append("{:.2f}".format(reading))
                readings.append(reading)
            # print("temperatures: %s | hummidities: %s | battery: %s" % ( ", ".join(readings[0:3]), ", ".join(readings[3:6]), "?%" ) )
            return readings
            
        connected = False
        tries = 0
        
        while not connected and tries < 5:
            try:
                dev = btle.Peripheral(self.sensor_id)
                connected = True
                print ("Connected to", self.sensor_id )
            except:
                print ("Failed to connect to", self.sensor_id )
                tries += 1
        
        if connected:
            #Get handles to the transmit and receieve characteristics
            tx = dev.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            rx = dev.getCharacteristics(uuid=RX_CHAR_UUID)[0]

            #Send initial command to get the number of available data points
            response = write_bytes("0100000000")
        
            #The number of available values is stored in the second and third bytes of the response, little endian order
            available = int.from_bytes(response[1:3], byteorder='little')

            # print ("There are {} available data points from this device ({})".format(available,SENSORS[sensor]))convert_to_readings

            try:
                # Data is returned as three pairs of temperature and humidity values
                for data_point in range(int(available / 3)):
                    # index = data_point * 3
                    index = data_point
                    
                    # convert index to hex, padded with leading zeroes
                    index_hex = hex(index)[2:].zfill(4)
                    
                    # reverse the byte order of the hex values
                    index_hex_reversed = index_hex[2:] + index_hex[0:2]
                    
                    # build the request string to be sent to the device
                    hex_string = "07" + index_hex_reversed + "000003"
                    
                    # send the request and get the response
                    response = write_bytes(hex_string)

                    # export the response to temperature and humidity readings to prometheus
                    temp_1, temp_2, temp_3, hum_1, hum_2, hum_3 = convert_to_readings(response)
                    self.temp_sensor_1 = int(temp_1)
                    self.temp_sensor_2 = int(temp_2)
                    self.temp_sensor_3 = int(temp_3)

                    self.hum_sensor_1 = int(hum_1)
                    self.hum_sensor_2 = int(hum_2)
                    self.hum_sensor_3 = int(hum_3)
            
            except:
                pass
        
        print(self.status)
    