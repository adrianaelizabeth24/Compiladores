#clase tipo tabla de variables
#atributos nombre, tipo, scope
class tablaConstantes(object):
       def __init__(self,valor,direccion):
              self.valor = valor
              self.direccion = direccion
       def getDireccion(self):
              return self.direccion
       def getValor(self):
              return self.valor
       def setDireccion(self,direccion):
              self.direccion = direccion
       def setValor(self,nombre):
              self.valor = valor
