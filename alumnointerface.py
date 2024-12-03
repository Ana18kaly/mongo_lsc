from alumno import Alumno
from database import Database

class AlumnoInterface:
    def __init__(self):
      
        self.alumnos.cargar_alumnos()

    def guardar_cambios(self):
        """Guarda los cambios en el archivo JSON."""
        self.alumnos.guardar_alumnos()

    def agregar_alumno(self, name, pname, mname, curp, matricula):
        """Agrega un alumno y guarda los cambios en el archivo."""
        try:
            nuevo_alumno = Alumno(name, pname, mname, curp, matricula)
            self.alumnos.agregar(nuevo_alumno)
            database = Database("3clases", "alumnos")
            if database.ping:
                database.guardar(self.alumnos.to_dict())
                open_file = open('lista_alumnos.json', 'w')
                open_file.write = []
                open_file.close()
            else:
                self.alumnos.guardar_alumnos(self.alumnos.to_dict())
        except ValueError as e:
            print(f"Error al agregar alumno: {e}")

    def eliminar_alumno(self, matricula):
        """Elimina un alumno por matrícula y guarda los cambios en el archivo."""
        try:
            self.alumnos.eliminar(matricula)
            self.guardar_cambios()
            print("Alumno eliminado exitosamente.")
        except ValueError as e:
            print(f"Error al eliminar alumno: {e}")

    def cambiar_datos_alumno(self, matricula, name=None, pname=None, mname=None, curp=None, new_matricula=None):
        """Modifica los datos de un alumno específico y guarda los cambios."""
        try:
            self.alumnos.cambiar_datos_alumno(matricula, name, pname, mname, curp, new_matricula)
            self.guardar_cambios()
            print("Datos del alumno modificados exitosamente.")
        except ValueError as e:
            print(f"Error al modificar alumno: {e}")

    def buscar_alumno(self, matricula):
        """Busca un alumno por su matrícula y lo muestra."""
        alumno = self.alumnos.buscar_por_matricula(matricula)
        if alumno:
            print(f"Alumno encontrado: {alumno.nombre} {alumno.paterno} {alumno.materno} - Matrícula: {alumno.matricula_a}")
        else:
            print("No se encontró ningún alumno con esa matrícula.")

    def mostrar_alumnos(self):
        """Muestra la lista completa de alumnos desde el archivo."""
        self.alumnos.cargar_alumnos() 
        print("\nLista de alumnos:")
        print(self.alumnos.mostrar_lista())

    def interfaz_usuario(self):
        """Interfaz interactiva para gestionar alumnos."""
        while True:
            print("\nMenú de Alumno:")
            print("1. Agregar Alumno")
            print("2. Modificar Alumno")
            print("3. Eliminar Alumno")
            print("4. Buscar Alumno")
            print("5. Mostrar Alumnos")
            print("6. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                name = input("Nombre: ")
                pname = input("Apellido Paterno: ")
                mname = input("Apellido Materno: ")
                curp = input("CURP: ")
                matricula = input("Matrícula: ")
                self.agregar_alumno(name, pname, mname, curp, matricula)

            elif opcion == "2":
                matricula = input("Matrícula del alumno a modificar: ")
                name = input("Nuevo nombre (dejar vacío para no cambiar): ") or None
                pname = input("Nuevo apellido paterno (dejar vacío para no cambiar): ") or None
                mname = input("Nuevo apellido materno (dejar vacío para no cambiar): ") or None
                curp = input("Nuevo CURP (dejar vacío para no cambiar): ") or None
                new_matricula = input("Nueva matrícula (dejar vacío para no cambiar): ") or None
                self.cambiar_datos_alumno(matricula, name, pname, mname, curp, new_matricula)

            elif opcion == "3":
                matricula = input("Matrícula del alumno a eliminar: ")
                self.eliminar_alumno(matricula)

            elif opcion == "4":
                matricula = input("Matrícula del alumno a buscar: ")
                self.buscar_alumno(matricula)

            elif opcion == "5":
                self.mostrar_alumnos()

            elif opcion == "6":
                print("Saliendo del sistema.")
                break

            else:
                print("Opción no válida. Por favor, selecciona una opción del 1 al 6.")


if __name__ == "__main__":
    try:
        alumno_manager = AlumnoInterface()
        alumno_manager.interfaz_usuario()
    except Exception as e:
        print(f"Error inesperado: {e}")



