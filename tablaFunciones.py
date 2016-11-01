#clase tipo tabla de funciones
#atributos: nombre y tipo
class tablaFunciones(object):
      def __init__(self,nombre,tipo,parametros,size):
          self.nombre = nombre
          self.tipo = tipo
          self.parametros = parametros
          self.size = size
      def getNombre(self):
          return self.nombre
      def getTipo(self):
          return self.tipo
      def getSize(self):
          return self.size
      def getParametros(self):
          return self.parametros
      def setNombre(self,nombre):
          self.nombre = nombre
      def setTipo(self,tipo):
          self.tipo = tipo
      def setSize(self,size):
          self.size = size
      def setParametros(self,parametros):
          self.parametros = parametros
