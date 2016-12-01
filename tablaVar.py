#clase tipo tabla de variables
#atributos nombre, tipo, scope
class tablaVar(object):
       def __init__(self,nombre,tipo,scope,direccion,size):
              self.nombre = nombre
              self.tipo = tipo
              self.scope = scope
              self.direccion = direccion
              self.size = size
       def getNombre(self):
              return self.nombre
       def getTipo(self):
              return self.tipo
       def getScope(self):
              return self.scope
       def getDireccion(self):
              return self.direccion
       def getSize(self):
              return self.size
       def setDireccion(self,direccion):
              self.direccion = direccion
       def setNombre(self,nombre):
              self.nombre = nombre
       def setTipo(self,tipo):
              self.tipo = tipo
       def setScope(self,scope):
              self.scope = scope
       def setSize(self,size):
              self.size = size