#clase tipo tabla de funciones
#atributos: nombre y tipo
class tablaFunciones(object):
      def __init__(self,nombre,tipo,parametros,start):
          self.nombre = nombre
          self.tipo = tipo
          self.parametros = parametros
          self.start = start

      def getNombre(self):
          return self.nombre

      def getTipo(self):
          return self.tipo

      def getParametros(self):
          return self.parametros

      def getStart(self):
          return self.start

      def setNombre(self,nombre):
          self.nombre = nombre

      def setTipo(self,tipo):
          self.tipo = tipo

      def setParametros(self,parametros):
          self.parametros = parametros

      def setStart(self,start):
          self.start = start
