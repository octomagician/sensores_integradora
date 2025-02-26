from machine import UART, Pin
from sensor import Sensor
import time
import json

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
tinaco = Sensor()

while True:
    if uart.any():
        data = uart.read()
    
        if data:
            line = data.decode('utf-8').strip()
            print(line)
            
            if line.startswith("TDS"):
                id_sensor = "TDS"
            elif line.startswith("TEM"):
                id_sensor = "TEM"
            elif line.startswith("TUR"):
                id_sensor = "TUR"
            elif line.startswith("SPH"):
                id_sensor = "SPH"
            else:
                continue
            valor = float(line.split(":")[1])
            now = time.localtime()
            timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                now[0], now[1], now[2], now[3], now[4], now[5]
            )

            sensor = Sensor(id_sensor, valor, timestamp)
            tinaco.create(sensor)
            tinaco.to_json("Tinaco0")
            print("saved")    
    time.sleep(1)

