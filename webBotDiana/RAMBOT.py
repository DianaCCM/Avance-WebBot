class RAM: #Clase para organizar RAM

    def __init__(self, codigo):
        self.codigo = codigo

    def toMemRam (self): #Se retorna en formato Json lo que será guardado en la colección
        return { "codigo":self.codigo }
