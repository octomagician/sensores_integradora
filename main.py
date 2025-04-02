import network
import time
import urequests
import json
from machine import UART, Pin
import os

# Configuración UART ---------------------------------------------
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), timeout=100)
# Configuración Wi-Fi --------------------------------------------
#ssid = "IOT" 
#password = "exameniot"
#ssid = "iPhone de Ana"
#password = "toto0306"
#server_url = "https://conejosaltando.fun/api/v1/data"
#ssid = "AF"
#password = "Chitoto0306@"
#server_url = "http://192.168.0.63:8000/api/v1/data"
ssid = "Tics Enero 25"
password = "W@c@nd@Forever"
server_url = "http://192.168.252.196:8000/api/v1/data"
# Otros ----------------------------------------------------------
local_storage = "data.json"
buffer = ""

# Función para conectar a Wi-Fi (igual que antes)
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        current_ssid = wlan.config('essid')
        if current_ssid != ssid:
            wlan.disconnect()
            time.sleep(1)
    
    if not wlan.isconnected():
        print("Conectando a Wi-Fi...")
        wlan.connect(ssid, password)
        
        max_attempts = 10
        while not wlan.isconnected() and max_attempts > 0:
            print("Intentando conectar...")
            time.sleep(1)
            max_attempts -= 1

        if not wlan.isconnected():
            print("No se pudo conectar a Wi-Fi")
            return False
        else:
            print("Conexión exitosa!")
            print("IP:", wlan.ifconfig()[0])
            return True
    else:
        print("Ya conectado a Wi-Fi")
        print("IP:", wlan.ifconfig()[0])
        return True

# Función para guardar datos localmente
def save_locally(data):
    try:
        existing_data = []
        try:
            with open(local_storage, "r") as file:
                for line in file:
                    if line.strip():
                        existing_data.append(json.loads(line))
        except OSError:
            pass
        
        existing_data.append(data)
        
        with open(local_storage, "w") as file:
            for item in existing_data:
                file.write(json.dumps(item) + "\n")
        print("Dato guardado en data.json")
    except Exception as e:
        print("Error al guardar:", e)

# Función para leer y enviar datos acumulados
def send_accumulated_data():
    if not connect_wifi(ssid, password):
        return False
    
    try:
        with open(local_storage, "r") as file:
            accumulated = [json.loads(line) for line in file if line.strip()]
    except OSError:
        return True  # No hay datos para enviar
    
    if not accumulated:
        return True
    
    try:
        print(f"Intentando enviar {len(accumulated)} datos...")
        response = urequests.post(server_url, json={"batch": accumulated})
        
        if response.status_code in (200, 201):
            print("Envío exitoso! Borrando data.json")
            with open(local_storage, "w") as file:
                file.write("")
            return True
        else:
            print(f"Error del servidor: {response.text}")
            return False
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False
    finally:
        if 'response' in locals():
            response.close()

#---------------------------------------------------------------------
# Bucle principal ----------------------------------------------------
last_send_time = time.time()
SEND_INTERVAL = 30  #seg

while True:
    try:
        # Intentar enviar cada minuto
        current_time = time.time()
        if current_time - last_send_time >= SEND_INTERVAL:
            if send_accumulated_data():
                last_send_time = current_time
            else:
                print("Fallo en envío. Reintentando en 1 minuto.")
        
        # Procesar datos UART
        data = uart.read()
        if data:
            try:
                buffer += data.decode('utf-8')
            except UnicodeError:
                buffer = ""
                continue
                
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()
                
                if not line or ':' not in line:
                    continue
                
                print("Dato recibido:", line)
                
                try:
                    if line.startswith("5"): sensor_id = 5 		#TDS
                    elif line.startswith("2"): sensor_id = 2	#TEM
                    elif line.startswith("4"): sensor_id = 4	#TUR
                    elif line.startswith("3"): sensor_id = 3	#PH
                    elif line.startswith("1"): sensor_id = 1	#SON
                    elif line.startswith("BOM"): sensor_id = "BOM"
                    else: continue

                    tinaco_id = int(line.split('-')[1].split('+')[0])
                    valor = float(line.split(':')[1].strip())
                    
                    payload = {
                        "sensor_id": sensor_id,
                        "tinaco_id": tinaco_id,
                        "valor": valor,
                        "timestamp": "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*time.localtime())
                    }
                    
                    save_locally(payload)
                    
                except Exception as e:
                    print(f"Error procesando dato: {e}")
        
        time.sleep(0.1)
        
    except Exception as e:
        print(f"Error en bucle principal: {e}")
        time.sleep(1)
