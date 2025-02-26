from clase import Clase

class Sensor(Clase):
    def __init__(self, id=None, valor=None, timestamp=None):
        if id is not None and valor is not None and timestamp is not None:
            self.__id = id
            self.__valor = valor
            self.__timestamp = timestamp
            self.is_object = True
        else:
            super().__init__()
            self.is_object = False

    def to_dictionary(self):
        if self.is_object:
            return {
                "id": self.__id,
                "valor": self.__valor,
                "timestamp": self.__timestamp
            }
        else:
            return [obj.to_dictionary() for obj in self.collection if obj.is_object]

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, nuevo_id):
        if not nuevo_id:
            raise ValueError("id vacío")
        self.__id = nuevo_id
    
    @id.deleter
    def id(self):
        self.__id = None

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
"""
if __name__ == "__main__":
    Tinaco0 = Sensor()
    Sensor0 = Sensor("TEM", 25, "2021-09-01 12:00:00")
    Sensor1 = Sensor("TUR", 500, "2021-09-01 12:00:00")
    Tinaco0.create(Sensor0)
    Tinaco0.create(Sensor1)

    print("valors:")
    print(Tinaco0.read())

    Tinaco0.to_json("Tinaco0")
    print("Tinaco0 guardado como Tinaco0.json")
"""
