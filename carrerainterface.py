from database import Database
from bson import ObjectId


class CarreraInterface:
    def __init__(self):
        self.database_carreras = Database("3clases", "carreras")
        self.database_grupos = Database("3clases", "grupos")
        self.carreras = self.cargar_carreras()
        self.grupos = self.cargar_grupos()

    def cargar_carreras(self):
        """Carga las carreras desde la colección MongoDB."""
        if self.database_carreras.ping():
            return list(self.database_carreras.collection_name.find({}))
        else:
            print("Error: No se pudo conectar a la colección 'carreras'.")
            return []

    def cargar_grupos(self):
        """Carga los grupos desde la colección MongoDB."""
        if self.database_grupos.ping():
            return list(self.database_grupos.collection_name.find({}, {"_id": 0}))
        else:
            print("Error: No se pudo conectar a la colección 'grupos'.")
            return []

    def manejar_opciones_carrera(self, opcion):
        acciones = {
            '1': self._opcion_crear_carrera,
            '2': self._opcion_modificar_carrera,
            '3': self._opcion_eliminar_carrera,
            '4': self._opcion_agregar_grupo_a_carrera,
            '5': self._opcion_eliminar_grupo_de_carrera,
            '6': self._opcion_mostrar_numero_carreras,
        }
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida.")

    def _opcion_crear_carrera(self):
        nombre_carrera = input("Nombre de la carrera: ")
        clave_carrera = input("Clave de la carrera: ")
        nombre_grupo = input("Nombre del grupo a asociar: ")
        self.crear_carrera(nombre_carrera, clave_carrera, nombre_grupo)

    def _opcion_modificar_carrera(self):
        id_carrera = input("ID de la carrera a modificar: ")
        nuevo_nombre = input("Nuevo nombre de la carrera (deja en blanco para no cambiar): ")
        nueva_clave = input("Nueva clave de la carrera (deja en blanco para no cambiar): ")
        self.modificar_carrera(id_carrera, nuevo_nombre, nueva_clave)

    def _opcion_eliminar_carrera(self):
        id_carrera = input("ID de la carrera a eliminar: ")
        self.eliminar_carrera(id_carrera)

    def _opcion_agregar_grupo_a_carrera(self):
        id_carrera = input("ID de la carrera: ")
        nombre_grupo = input("Nombre del grupo a agregar: ")
        self.agregar_grupo_a_carrera(id_carrera, nombre_grupo)

    def _opcion_eliminar_grupo_de_carrera(self):
        id_carrera = input("ID de la carrera: ")
        nombre_grupo = input("Nombre del grupo a eliminar: ")
        self.eliminar_grupo_de_carrera(id_carrera, nombre_grupo)

    def _opcion_mostrar_numero_carreras(self):
        self.mostrar_numero_carreras()

    def crear_carrera(self, nombre_carrera, clave_carrera, nombre_grupo):
        grupo_seleccionado = next((grupo for grupo in self.grupos if grupo['nombre_grupo'] == nombre_grupo), None)
        if grupo_seleccionado:
            nueva_carrera = {
                "nombre": nombre_carrera,
                "clave": clave_carrera,
                "grupos": [grupo_seleccionado]
            }
            self.database_carreras.collection_name.insert_one(nueva_carrera)
            self.carreras.append(nueva_carrera)
            print(f"Carrera '{nombre_carrera}' agregada exitosamente con el grupo '{nombre_grupo}'.")
        else:
            print(f"El grupo '{nombre_grupo}' no fue encontrado.")

    def modificar_carrera(self, id_carrera, nuevo_nombre=None, nueva_clave=None):
        carrera = next((c for c in self.carreras if str(c["_id"]) == id_carrera), None)
        if carrera:
            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nueva_clave:
                cambios["clave"] = nueva_clave

            if cambios:
                self.database_carreras.collection_name.update_one({"_id": ObjectId(id_carrera)}, {"$set": cambios})
                carrera.update(cambios)
                print(f"Carrera '{id_carrera}' modificada exitosamente.")
        else:
            print(f"Carrera con ID '{id_carrera}' no encontrada.")

    def eliminar_carrera(self, id_carrera):
        resultado = self.database_carreras.collection_name.delete_one({"_id": ObjectId(id_carrera)})
        if resultado.deleted_count > 0:
            self.carreras = [carrera for carrera in self.carreras if str(carrera["_id"]) != id_carrera]
            print(f"Carrera con ID '{id_carrera}' eliminada exitosamente.")
        else:
            print(f"Carrera con ID '{id_carrera}' no encontrada.")

    def agregar_grupo_a_carrera(self, id_carrera, nombre_grupo):
        grupo_seleccionado = next((grupo for grupo in self.grupos if grupo['nombre_grupo'] == nombre_grupo), None)
        if grupo_seleccionado:
            carrera = next((c for c in self.carreras if str(c["_id"]) == id_carrera), None)
            if carrera:
                self.database_carreras.collection_name.update_one(
                    {"_id": ObjectId(id_carrera)},
                    {"$push": {"grupos": grupo_seleccionado}}
                )
                carrera["grupos"].append(grupo_seleccionado)
                print(f"Grupo '{nombre_grupo}' agregado a la carrera con ID '{id_carrera}'.")
            else:
                print(f"Carrera con ID '{id_carrera}' no encontrada.")
        else:
            print(f"Grupo '{nombre_grupo}' no encontrado.")

    def eliminar_grupo_de_carrera(self, id_carrera, nombre_grupo):
        carrera = next((c for c in self.carreras if str(c["_id"]) == id_carrera), None)
        if carrera:
            self.database_carreras.collection_name.update_one(
                {"_id": ObjectId(id_carrera)},
                {"$pull": {"grupos": {"nombre_grupo": nombre_grupo}}}
            )
            carrera["grupos"] = [g for g in carrera["grupos"] if g["nombre_grupo"] != nombre_grupo]
            print(f"Grupo '{nombre_grupo}' eliminado de la carrera con ID '{id_carrera}'.")
        else:
            print(f"Carrera con ID '{id_carrera}' no encontrada.")

    def mostrar_numero_carreras(self):
        print(f"Número total de carreras creadas: {len(self.carreras)}")

    def interfaz_usuario(self):
        while True:
            print("\nMenú de Carrera:")
            print("1. Crear Carrera")
            print("2. Modificar Carrera")
            print("3. Eliminar Carrera")
            print("4. Agregar Grupo a Carrera")
            print("5. Eliminar Grupo de Carrera")
            print("6. Mostrar Número de Carreras")
            print("7. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion in ['1', '2', '3', '4', '5', '6']:
                self.manejar_opciones_carrera(opcion)
            elif opcion == '7':
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")


# Ejecutar la interfaz
if __name__ == "__main__":
    carrera_manager = CarreraInterface()
    carrera_manager.interfaz_usuario()






