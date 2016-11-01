class cuadruplo(object):
       def __init__(self,operador,operando1,operando2,resultado):
              self.operador = operador
              self.operando1 = operando1
              self.operando2 = operando2
              self.resultado = resultado
       def getOperador(self):
              return self.operador
       def getOperando1(self):
              return self.operando1
       def getOperando2(self):
              return self.operando2
       def getResultado(self):
              return self.resultado
       def setResultado(self,resultado):
              self.resultado = resultado
       def setOperador(self,operador):
              self.operador = operador
       def setOperando1(self,operando1):
              self.operando1 = operando1
       def setOperando2(self,operando2):
              self.operando2 = operando2