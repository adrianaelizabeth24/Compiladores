#clase tipo tabla de funciones
#atributos: nombre y tipo
class tablaFunciones(object):
      def __init__(self,nombre,tipo):
          self.nombre = nombre
          self.tipo = tipo
      def getNombre(self):
          return self.nombre
      def getTipo(self):
          return self.tipo