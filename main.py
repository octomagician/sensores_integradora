import network
import time
import urequests
import json
from machine import UART, Pin

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
ssid = "IOT" 
password = "exameniot"
server_url = "http://192.168.80.156:8000/api/v1/data"
local_storage = "data.json"

# Función para conectar a Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Conectando a la red Wi-Fi...")
        wlan.connect(ssid, password)
        
        # Esperar a que se conecte
        max_attempts = 10
        while not wlan.isconnected() and max_attempts > 0:
            print("Intentando conectar...")
            time.sleep(1)
            max_attempts -= 1

        if not wlan.isconnected():
            print("No se pudo conectar a la red Wi-Fi.")
            return False
        else:
            print("Conexión exitosa!")
            print("Dirección IP:", wlan.ifconfig()[0])
            return True
    else:
        print("Ya está conectado a la red Wi-Fi.")
        print("Dirección IP:", wlan.ifconfig()[0])
        return True

# Función para guardar datos localmente
def save_locally(data):
    """Guarda los datos localmente en un archivo JSON."""
    with open(local_storage, "a") as file:
        file.write(json.dumps(data) + "\n")

# Función para enviar datos al servidor
def send_to_server(data):
    """Envía los datos al servidor."""
    try:
        response = urequests.post(server_url, json=data)
        print("Respuesta del servidor:", response.text)
        response.close()
        return True
    except Exception as e:
        print("Error al enviar datos al servidor:", e)
        return False

# Conectar a Wi-Fi
if not connect_wifi(ssid, password):
    print("No se pudo conectar a Wi-Fi. Los datos se guardarán solo localmente.")

# Bucle principal
while True:
    if uart.any():
        data = uart.read()
        if data:
            line = data.decode('utf-8').strip()
            print(line)

            # Procesar los datos
            if line.startswith("5"): #tds
                sensor_id = 5
            elif line.startswith("2"): #temperatura
                sensor_id = 2
            elif line.startswith("4"): #turbidez
                sensor_id = 4
            elif line.startswith("3"): #ph
                sensor_id = 3
            elif line.startswith("1"): #ultrasonico
                sensor_id = 1
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

            # Crear el JSON para enviar
            payload = {
                "sensor_id": sensor_id,
                "tinaco_id": tinaco_id,
                "valor": valor,
                "timestamp": timestamp
            }

            # Intentar enviar los datos al servidor
            if connect_wifi(ssid, password):  # Verificar conexión Wi-Fi antes de enviar
                if not send_to_server(payload):
                    # Si falla, guardar localmente
                    save_locally(payload)
                    print("Datos guardados localmente.")
           
