import json

class Clase:
    def __init__(self):
        self.collection = []
        self.is_object = False

    def create(self, obj):
        self.collection.append(obj)
        return f"Agregada: {obj}"

    def read(self):
        return self.to_dictionary()

    def update(self, index, new_object):
        if 0 <= index < len(self.collection):
            self.collection[index] = new_object
            return f"Modificada:\n{new_object}"
        return "Fuera de rango."

    def delete(self, index):
        if 0 <= index < len(self.collection):
            old_object = self.collection.pop(index)
            return f"Eliminada:\n{old_object}"
        return "Índice fuera de rango."

    def to_json(self, path):
        with open(path + ".json", 'w') as file:
            file.write(json.dumps(self.read()))
            #la rasp no soporta el indent, hace que truene

