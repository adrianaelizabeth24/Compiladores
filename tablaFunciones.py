#clase tipo tabla de funciones
#atributos: nombre y tipo
class tablaFunciones(object):
      def __init__(self,nombre,tipo,parametros,direcciones,start,dirs):
          self.nombre = nombre
          self.tipo = tipo
          self.parametros = parametros
          self.direcciones = direcciones
          self.start = start
          self.dirs = dirs

      def getNombre(self):
          return self.nombre

      def getTipo(self):
          return self.tipo

      def getParametros(self):
          return self.parametros

      def getDirecciones(self):
          return self.direcciones

      def getStart(self):
          return self.start

      def getDirs(self):
          return self.dirs

      def setNombre(self,nombre):
          self.nombre = nombre

      def setTipo(self,tipo):
          self.tipo = tipo

      def setParametros(self,parametros):
          self.parametros = parametros

      def setDirecciones(self,direcciones):
          self.direcciones = direcciones

      def setStart(self,start):
          self.start = start

      def setDirs(self,dirs):
          self.dirs = dirs
