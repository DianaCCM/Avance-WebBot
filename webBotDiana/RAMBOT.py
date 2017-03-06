class RAM: #Clase para organizar RAM

    def __init__(self, codigo): #Para crear el objeto
        self.codigo = codigo

    def toMemRam (self): #Se retorna en formato Json lo que será guardado en la colección
        return { "codigo":self.codigo }
