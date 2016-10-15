#clase tipo tabla de variables
#atributos nombre, tipo, scope
class tablaVar(object):
       def __init__(self,nombre,tipo,scope):
              self.nombre = nombre
              self.tipo = tipo
              self.scope = scope
       def getNombre(self):
              return self.nombre
       def getTipo(self):
              return self.tipo
       def getScope(self):
              return self.scope