class Lista:
    def __init__(self):
        self.elementos = []

    def agregar(self, elemento):
        """Agrega un nuevo elemento a la lista."""
        self.elementos.append(elemento)
        print(f"Elemento agregado: {elemento}")

    def editar(self, index, nuevo_elemento):
        """Edita un elemento en la lista según su índice."""
        if 0 <= index < len(self.elementos):
            self.elementos[index] = nuevo_elemento
            print(f"Elemento en el índice {index} editado a: {nuevo_elemento}")
        else:
            print(f"Índice {index} fuera de rango.")

    def eliminar(self, index):
        """Elimina un elemento de la lista según su índice."""
        if 0 <= index < len(self.elementos):
            eliminado = self.elementos.pop(index)
            print(f"Elemento eliminado: {eliminado}")
        else:
          print(f"Índice {index} fuera de rango.")

    def __str__(self):
        """Retorna una representación de la lista."""
        if not self.elementos:
            return "La lista está vacía."
        return "\n".join([f"{idx}: {elem}" for idx, elem in enumerate(self.elementos)])