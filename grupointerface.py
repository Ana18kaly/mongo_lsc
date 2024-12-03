from database import Database  # Clase para manejar la conexión con MongoDB
from bson import ObjectId  # Para manejar IDs en MongoDB


class GrupoInterface:
    def __init__(self):
        self.database_alumnos = Database("3clases", "alumnos")
        self.database_grupos = Database("3clases", "grupos")
        self.grupos = self.cargar_grupos()  # Cargar grupos desde MongoDB
        self.alumnos = self.cargar_alumnos()  # Cargar alumnos desde MongoDB

    def cargar_alumnos(self):
        """Carga los alumnos desde la colección MongoDB."""
        if self.database_alumnos.ping():
            return list(self.database_alumnos.collection_name.find({}, {"_id": 0}))
        else:
            print("Error: No se pudo conectar a la colección 'alumnos'.")
            return []

    def cargar_grupos(self):
        """Carga los grupos desde la colección MongoDB."""
        if self.database_grupos.ping():
            return list(self.database_grupos.collection_name.find({}))
        else:
            print("Error: No se pudo conectar a la colección 'grupos'.")
            return []

    def buscar_alumno_por_matricula(self, matricula):
        """Busca un alumno en la lista de alumnos por matrícula."""
        for alumno in self.alumnos:
            if alumno["matricula_a"] == matricula.strip():
                return alumno
        return None

    def manejar_opciones_grupo(self, opcion):
        acciones = {
            '1': self._opcion_agregar_grupo,
            '2': self._opcion_modificar_grupo,
            '3': self._opcion_eliminar_grupo,
            '4': self._opcion_eliminar_alumno_de_grupo,
            '5': self._opcion_mostrar_grupos,
            '6': self._opcion_agregar_alumno_a_grupo,
        }
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida.")

    def _opcion_agregar_grupo(self):
        nombre_grupo = input("Nombre del grupo: ")
        grado = input("Grado: ")
        seccion = input("Sección: ")
        matriculas = input("Lista de matrículas de alumnos (separadas por comas): ").split(',')
        self.agregar_grupo(nombre_grupo, grado, seccion, matriculas)
        print("Grupo agregado y almacenado en MongoDB.")

    def _opcion_modificar_grupo(self):
        nombre_grupo = input("Nombre del grupo a modificar: ")
        nuevo_nombre = input("Nuevo nombre del grupo (deja en blanco para no cambiar): ")
        nuevo_grado = input("Nuevo grado (deja en blanco para no cambiar): ")
        nueva_seccion = input("Nueva sección (deja en blanco para no cambiar): ")
        nuevas_matriculas = input("Nueva lista de matrículas (separadas por comas, deja en blanco para no cambiar): ").split(',')
        if nuevas_matriculas == ['']:
            nuevas_matriculas = None
        self.cambiar_datos_grupo(nombre_grupo, nuevo_nombre=nuevo_nombre, nuevo_grado=nuevo_grado, nueva_seccion=nueva_seccion, nuevas_matriculas=nuevas_matriculas)

    def _opcion_eliminar_grupo(self):
        nombre_grupo = input("Nombre del grupo a eliminar: ")
        if self.eliminar_grupo(nombre_grupo):
            print("Grupo eliminado de MongoDB.")
        else:
            print("Grupo no encontrado.")

    def _opcion_eliminar_alumno_de_grupo(self):
        nombre_grupo = input("Nombre del grupo: ")
        matricula_alumno = input("Matrícula del alumno a eliminar: ")
        self.eliminar_alumno_de_grupo(nombre_grupo, matricula_alumno)

    def _opcion_mostrar_grupos(self):
        print("\nLista de grupos:")
        self.mostrar_grupos()

    def _opcion_agregar_alumno_a_grupo(self):
        nombre_grupo = input("Nombre del grupo: ")
        matricula_alumno = input("Matrícula del alumno a agregar: ")
        self.agregar_alumno_a_grupo(nombre_grupo, matricula_alumno)

    def agregar_grupo(self, nombre_grupo, grado, seccion, matriculas):
        """Agrega un grupo directamente a la base de datos MongoDB."""
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
        self.database_grupos.collection_name.insert_one(nuevo_grupo)
        self.grupos.append(nuevo_grupo)

    def eliminar_grupo(self, nombre_grupo):
        """Elimina un grupo de la colección MongoDB."""
        resultado = self.database_grupos.collection_name.delete_one({"nombre_grupo": nombre_grupo})
        if resultado.deleted_count > 0:
            self.grupos = [g for g in self.grupos if g["nombre_grupo"] != nombre_grupo]
            return True
        return False

    def cambiar_datos_grupo(self, nombre_grupo, nuevo_nombre=None, nuevo_grado=None, nueva_seccion=None, nuevas_matriculas=None):
        """Modifica un grupo en la colección MongoDB."""
        grupo = next((g for g in self.grupos if g["nombre_grupo"] == nombre_grupo), None)
        if not grupo:
            print(f"Grupo '{nombre_grupo}' no encontrado.")
            return False

        nuevos_datos = {}
        if nuevo_nombre:
            nuevos_datos["nombre_grupo"] = nuevo_nombre
        if nuevo_grado:
            nuevos_datos["grado"] = nuevo_grado
        if nueva_seccion:
            nuevos_datos["seccion"] = nueva_seccion
        if nuevas_matriculas:
            nuevos_alumnos = []
            for matricula in nuevas_matriculas:
                alumno = self.buscar_alumno_por_matricula(matricula)
                if alumno:
                    nuevos_alumnos.append(alumno)
                else:
                    print(f"Alumno con matrícula {matricula.strip()} no encontrado.")
            nuevos_datos["alumnos"] = nuevos_alumnos

        if nuevos_datos:
            self.database_grupos.collection_name.update_one({"nombre_grupo": nombre_grupo}, {"$set": nuevos_datos})
            grupo.update(nuevos_datos)
            return True
        return False

    def mostrar_grupos(self):
        for grupo in self.grupos:
            print(f"Grupo: {grupo['nombre_grupo']}, Grado: {grupo['grado']}, Sección: {grupo['seccion']}")
            print("Alumnos:")
            for alumno in grupo.get("alumnos", []):
                print(f" - {alumno['matricula_a']}")

    def interfaz_usuario(self):
        while True:
            print("\nMenú de Grupo:")
            print("1. Agregar Grupo")
            print("2. Modificar Grupo")
            print("3. Eliminar Grupo")
            print("4. Eliminar Alumno de Grupo")
            print("5. Mostrar Grupos")
            print("6. Agregar Alumno a Grupo")
            print("7. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion in ['1', '2', '3', '4', '5', '6']:
                self.manejar_opciones_grupo(opcion)
            elif opcion == '7':
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")


# Ejecutar la interfaz
if __name__ == "__main__":
    interfaz = GrupoInterface()
    interfaz.interfaz_usuario()



