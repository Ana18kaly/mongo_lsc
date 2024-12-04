import json
from database import Database
from bson import ObjectId


class GrupoInterface:
    def __init__(self):
        # Conexión única a MongoDB
        self.db = Database("3clases")
        self.collection_alumnos = self.db.collection_name = self.db.db_name["alumnos"]
        self.collection_grupos = self.db.collection_name = self.db.db_name["grupos"]

        # Carga inicial de datos
        self.alumnos = self.cargar_alumnos()
        self.grupos = self.cargar_grupos()

    def cargar_alumnos(self):
        """Carga los alumnos desde MongoDB."""
        try:
            return list(self.collection_alumnos.find({}, {"_id": 0}))
        except Exception as e:
            print(f"Error al cargar alumnos: {e}")
            return []

    def cargar_grupos(self):
        """Carga los grupos desde MongoDB."""
        try:
            return list(self.collection_grupos.find({}))
        except Exception as e:
            print(f"Error al cargar grupos: {e}")
            return []

    def buscar_alumno_por_matricula(self, matricula):
        """Busca un alumno por su matrícula."""
        return next((alumno for alumno in self.alumnos if alumno["matricula_a"] == matricula.strip()), None)

    def agregar_grupo(self, nombre_grupo, grado, seccion, matriculas):
        """Agrega un grupo a MongoDB."""
        alumnos_grupo = []
        for matricula in matriculas:
            alumno = self.buscar_alumno_por_matricula(matricula)
            if alumno:
                alumnos_grupo.append(alumno)
            else:
                print(f"Alumno con matrícula {matricula.strip()} no encontrado.")
        nuevo_grupo = {
            "nombre_grupo": nombre_grupo,
            "grado": grado,
            "seccion": seccion,
            "alumnos": alumnos_grupo
        }
        try:
            self.collection_grupos.insert_one(nuevo_grupo)
            self.grupos.append(nuevo_grupo)
            print("Grupo agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar grupo: {e}")

    def eliminar_grupo(self, nombre_grupo):
        """Elimina un grupo por su nombre."""
        try:
            resultado = self.collection_grupos.delete_one({"nombre_grupo": nombre_grupo})
            if resultado.deleted_count > 0:
                self.grupos = [g for g in self.grupos if g["nombre_grupo"] != nombre_grupo]
                print(f"Grupo '{nombre_grupo}' eliminado.")
                return True
            print(f"Grupo '{nombre_grupo}' no encontrado.")
            return False
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False

    def mostrar_grupos(self):
        """Muestra la lista de grupos y sus alumnos."""
        if not self.grupos:
            print("No hay grupos registrados.")
            return
        for grupo in self.grupos:
            print(f"\nGrupo: {grupo['nombre_grupo']}, Grado: {grupo['grado']}, Sección: {grupo['seccion']}")
            print("Alumnos:")
            for alumno in grupo.get("alumnos", []):
                print(f" - {alumno['matricula_a']}")

    def interfaz_usuario(self):
        """Interfaz interactiva para manejar grupos."""
        opciones = {
            '1': self._opcion_agregar_grupo,
            '2': self._opcion_modificar_grupo,
            '3': self._opcion_eliminar_grupo,
            '4': self._opcion_mostrar_grupos
        }
        while True:
            print("\nMenú de Grupo:")
            print("1. Agregar Grupo")
            print("2. Modificar Grupo")
            print("3. Eliminar Grupo")
            print("4. Mostrar Grupos")
            print("5. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '5':
                print("Saliendo...")
                break
            accion = opciones.get(opcion)
            if accion:
                accion()
            else:
                print("Opción no válida. Intenta de nuevo.")

    def _opcion_agregar_grupo(self):
        nombre_grupo = input("Nombre del grupo: ")
        grado = input("Grado: ")
        seccion = input("Sección: ")
        matriculas = input("Matrículas de alumnos (separadas por comas): ").split(',')
        self.agregar_grupo(nombre_grupo, grado, seccion, matriculas)

    def _opcion_modificar_grupo(self):
        # Similar a agregar, pero actualiza un grupo existente
        pass

    def _opcion_eliminar_grupo(self):
        nombre_grupo = input("Nombre del grupo a eliminar: ")
        self.eliminar_grupo(nombre_grupo)

    def _opcion_mostrar_grupos(self):
        self.mostrar_grupos()


if __name__ == "__main__":
    interfaz = GrupoInterface()
    interfaz.interfaz_usuario()
