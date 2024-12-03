import json
from lista import Lista
class Alumno(Lista):
    def __init__(self, nombre=None, paterno=None, materno=None, curp=None, matricula=None):
        self.isLista = False
        if nombre is None and paterno is None:
            super().__init__()
            self.isLista = True  # Actúa como lista de alumnos
        else:
            self.nombre = nombre
            self.paterno = paterno
            self.materno = materno
            self.curp_a = curp
            self.matricula_a = matricula

    # Métodos para la gestión de alumnos
    # def agregar(self, alumno):
    #     """Agrega un alumno a la lista, evitando duplicados."""
    #     if not self.buscar_por_matricula(alumno.matricula_a):
    #         self.elementos.append(alumno)
    #         self.guardar_alumnos()
    #     else:
    #         raise ValueError(f"Ya existe un alumno con la matrícula {alumno.matricula_a}.")

    def eliminar(self, matricula):
        """Elimina un alumno por matrícula."""
        eliminado = [alumno for alumno in self.elementos if alumno.matricula_a == matricula]
        if eliminado:
            self.elementos = [alumno for alumno in self.elementos if alumno.matricula_a != matricula]
            self.guardar_alumnos()
        else:
            raise ValueError(f"No se encontró ningún alumno con la matrícula {matricula}.")

    def cambiar_datos_alumno(self, matricula, name=None, pname=None, mname=None, curp=None, new_matricula=None):
        """Modifica los datos de un alumno específico por su matrícula."""
        for alumno in self.elementos:
            if alumno.matricula_a == matricula:
                if name:
                    alumno.nombre = name
                if pname:
                    alumno.paterno = pname
                if mname:
                    alumno.materno = mname
                if curp:
                    alumno.curp_a = curp
                if new_matricula:
                    if not self.buscar_por_matricula(new_matricula):
                        alumno.matricula_a = new_matricula
                    else:
                        raise ValueError(f"Ya existe un alumno con la matrícula {new_matricula}.")
                self.guardar_alumnos()
                return
        raise ValueError(f"No se encontró ningún alumno con la matrícula {matricula}.")

    def buscar_por_matricula(self, matricula):
        """Busca un alumno por su matrícula."""
        for alumno in self.elementos:
            if alumno.matricula_a == matricula:
                return alumno
        return None

    def buscar_por_nombre(self, nombre):
        """Busca alumnos por nombre."""
        return [alumno for alumno in self.elementos if alumno.nombre.lower() == nombre.lower()]

    def cargar_alumnos(self):
        """Carga los alumnos desde un archivo JSON."""
        try:
            with open('lista_alumnos.json', 'r') as file:
                datos = json.load(file)
                self.elementos = [Alumno.from_dict(alumno) for alumno in datos]
        except (FileNotFoundError, json.JSONDecodeError):
            self.elementos = []

    def guardar_alumnos(self):
        """Guarda la lista de alumnos en un archivo JSON."""
        with open('lista_alumnos.json', 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    # Métodos auxiliares
    def to_dict(self):
        """Convierte la lista de alumnos a un diccionario."""
        if self.isLista:
            return [alumno.to_dict() for alumno in self.elementos]
        return {
            "nombre": self.nombre,
            "paterno": self.paterno,
            "materno": self.materno,
            "curp_a": self.curp_a,
            "matricula_a": self.matricula_a
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Alumno desde un diccionario."""
        return Alumno(
            nombre=data.get("nombre"),
            paterno=data.get("paterno"),
            materno=data.get("materno"),
            curp=data.get("curp_a"),
            matricula=data.get("matricula_a")
        )

    def mostrar_lista(self):
        """Muestra la lista de alumnos."""
        if self.isLista:
            return "\n".join([f"{i + 1}. {alumno.nombre} {alumno.paterno} {alumno.materno} - Matrícula: {alumno.matricula_a}" 
                              for i, alumno in enumerate(self.elementos)])
        return "Este objeto no es una lista de alumnos."

    def __str__(self):
        """Representación en cadena."""
        return self.mostrar_lista()
