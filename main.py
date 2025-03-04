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
                sensor_id = "TDS"
            elif line.startswith("TEM"):
                sensor_id = "TEM"
            elif line.startswith("TUR"):
                sensor_id = "TUR"
            elif line.startswith("SPH"):
                sensor_id = "SPH"
            elif line.startswith("BOM"):
                sensor_id = "BOM"
            else:
                continue
            tinaco_id = int(line.split("-")[1].split("+")[0])
            valor = float(line.split(":")[1])
            now = time.localtime()
            timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                now[0], now[1], now[2], now[3], now[4], now[5]
            )

            sensor = Sensor(sensor_id, tinaco_id, valor, timestamp)
            tinaco.create(sensor)
            tinaco.to_json("Tinacos")
            print("saved")    
    time.sleep(1)