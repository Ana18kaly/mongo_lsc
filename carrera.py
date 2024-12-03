import json

class Carrera:
    def __init__(self, nombre, clave, grupos=None):
        self.nombre = nombre
        self.clave = clave
        self.grupos = grupos if grupos else []

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "clave": self.clave,
            "grupos": self.grupos
        }

    @staticmethod
    def cargar_carreras():
        try:
            with open('carreras.json', 'r') as file:
                data = json.load(file)
                return [Carrera(**carrera) for carrera in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_carreras(carreras):
        with open('carreras.json', 'w') as file:
            json.dump([carrera.to_dict() for carrera in carreras], file, indent=4)

