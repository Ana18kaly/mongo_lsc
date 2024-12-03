import json

class Grupo:
    def __init__(self, nombre_grupo, grado, seccion, alumnos):
        self.nombre_grupo = nombre_grupo
        self.grado = grado
        self.seccion = seccion
        self.alumnos = alumnos  # Lista de diccionarios de alumnos

    def to_dict(self):
        # Convierte el grupo a un diccionario que se puede guardar en JSON
        return {
            'nombre_grupo': self.nombre_grupo,
            'grado': self.grado,
            'seccion': self.seccion,
            'alumnos': [alumno['matricula_a'] for alumno in self.alumnos]  # Asumimos que los alumnos son representados por su matrícula
        }

    @staticmethod
    def cargar_grupos():
        try:
            with open('grupos.json', 'r') as file:
                grupos_data = json.load(file)
                # Crea una lista de objetos Grupo a partir de los datos cargados
                grupos = []
                for grupo_data in grupos_data:
                    grupos.append(Grupo(grupo_data['nombre_grupo'], grupo_data['grado'], grupo_data['seccion'], grupo_data['alumnos']))
                return grupos
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Si no hay grupos guardados, devuelve una lista vacía

















