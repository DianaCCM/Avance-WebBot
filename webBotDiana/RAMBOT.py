class RAM:

    def __init__(self, codigo):
        self.codigo = codigo

    def toMemRam (self):
        return { "codigo":self.codigo }

    def __str__(self):
        return "codigo: " %(self.codigo)