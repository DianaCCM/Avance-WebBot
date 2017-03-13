class RAM:  # Clase para organizar RAM

    def __init__(self, codigo):  # Crear el objeto
        self.codigo = codigo

    def toRAM(self):  # Se retorna en formato Json lo que será guardado en la colección
        return {"codigo": self.codigo}
