from clase import Clase

class Sensor(Clase):
    def __init__(self, sensor_id=None, tinaco_id=None, valor=None, timestamp=None):
        #if sensor_id is not None and tinaco_id is not None and valor is not None and timestamp is not None:
        if (sensor_id and tinaco_id and valor and timestamp) is not None:
            self.__sensor_id = sensor_id
            self.__tinaco_id = tinaco_id
            self.__valor = valor
            self.__timestamp = timestamp
            self.is_object = True
        else:
            super().__init__()
            self.is_object = False

    def to_dictionary(self):
        if self.is_object:
            return {
                "sensor_id": self.__sensor_id,
                "tinaco_id": self.__tinaco_id,
                "valor": self.__valor,
                "timestamp": self.__timestamp
            }
        else:
            return [obj.to_dictionary() for obj in self.collection if obj.is_object]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
    @property
    def sensor_id(self):
        return self.__sensor_id
    
    @sensor_id.setter
    def sensor_id(self, nuevo_sensor_id):
        if not nuevo_sensor_id:
            raise ValueError("sensor_id vacío")
        self.__sensor_id = nuevo_sensor_id
    
    @sensor_id.deleter
    def sensor_id(self):
        self.__sensor_id = None

# --------------------------------------------------------------------------------------------
    @property
    def tinaco_id(self):
        return self.__tinaco_id
    
    @tinaco_id.setter
    def tinaco_id(self, nuevo_tinaco_id):
        if not nuevo_tinaco_id:
            raise ValueError("tinaco_id vacío")
        self.__tinaco_id = nuevo_tinaco_id
    
    @tinaco_id.deleter
    def tinaco_id(self):
        self.__tinaco_id = None

    # --------------------------------------------------------------------------------------------
    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, nuevo_valor):
        if not nuevo_valor:
            raise ValueError("valor vacío")
        self.__valor = nuevo_valor

    @valor.deleter
    def valor(self):
        self.__valor = None

    # --------------------------------------------------------------------------------------------
    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, nuevo_timestamp):
        if not nuevo_timestamp:
            raise ValueError("timestamp vacío")
        self.__timestamp = nuevo_timestamp

    @timestamp.deleter
    def timestamp(self):
        self.__timestamp = None

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

#Por si quieres probarlo localmente :)

if __name__ == "__main__":
    Tinaco0 = Sensor()
    Sensor0 = Sensor("TEM", "1", 25, "2021-09-01 12:00:00")
    Sensor1 = Sensor("TUR", "1", 500, "2021-09-01 12:00:00")
    Tinaco0.create(Sensor0)
    Tinaco0.create(Sensor1)

    print("valors:")
    print(Tinaco0.read())

    Tinaco0.to_json("Tinacos")
    print("Tinaco0 guardado como Tinacos.json")