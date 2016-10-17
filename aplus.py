#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Adriana Valenzuela a01195331
#Mayra Ruiz a00812918

from tablaVar import tablaVar
from tablaFunciones import tablaFunciones
from errorSintactico import errorSintactico
from errorLexico import errorLexico
from errorSemantico import errorSemantico
from cuadruplo import cuadruplo
from Queue import Queue
from Stack import Stack
import ply.lex as lex
import ply.yacc as yacc
import sys

#variables globales
bscope = 0;
iContadorDiccionarioVar = 1;
iContadorDiccionarioFuncion = 1;
iContadorInicioLocal = 0;
iAux = 0
arregloVar = [];
arregloFuncion = [];
dV = {};
dF = {};
tipoDeclaracion = ""
tmptipo = "";
op = -2
op1 = -2
op2 = -2
tipo = -2
operador = ""
operando1 = ""
operando2 = ""
resultado = []
iContadorTemporal = 0
PilaO = Stack()
POper = Stack()
arregloCuadruplos = []

cubo = [[[0 for k in range(11)] for j in range(4)] for i in range(4)]
#Cubo [OP1][OP2][OPERACION] = TIPO
# INT
cubo[0][0][0] = 0     # int + int = int
cubo[0][1][0] = 1     # int + float = float
cubo[0][2][0] = -1    # int + string = error
cubo[0][3][0] = -1    # int + bool = error

cubo[0][0][1] = 0     # int - int = int
cubo[0][1][1] = 1     # int - float = float
cubo[0][2][1] = -1    # int - string = error
cubo[0][3][1] = -1    # int - bool = error

cubo[0][0][2] = 0     # int * int = int
cubo[0][1][2] = 1     # int * float = float
cubo[0][2][2] = -1    # int * string = error
cubo[0][3][2] = -1    # int * bool = error

cubo[0][0][3] = 1     # int / int = int
cubo[0][1][3] = 1     # int / float = float
cubo[0][2][3] = -1    # int / string = error
cubo[0][3][3] = -1    # int / bool = error

cubo[0][0][4] = 3     # int < int = bool
cubo[0][1][4] = 3     # int < float = bool
cubo[0][2][4] = -1    # int < string = error
cubo[0][3][4] = -1    # int < bool = error

cubo[0][0][5] = 3     # int > int = bool
cubo[0][1][5] = 3     # int > float = bool
cubo[0][2][5] = -1    # int > string = error
cubo[0][3][5] = -1    # int > bool = error

# ERROR
cubo[0][0][6] = -1    # int = int = error
cubo[0][1][6] = -1    # int = float = error
cubo[0][2][6] = -1    # int = string = error
cubo[0][3][6] = -1    # int = bool = error

cubo[0][0][7] = 3     # int <> int = bool
cubo[0][1][7] = 3     # int <> float = bool
cubo[0][2][7] = -1    # int <> string = error
cubo[0][3][7] = -1    # int <> bool = error

cubo[0][0][8] = 3     # int == int = bool
cubo[0][1][8] = 3     # int == float = bool
cubo[0][2][8] = -1    # int == string = error
cubo[0][3][8] = -1    # int == bool = error

cubo[0][0][9] = -1    # int & int = error
cubo[0][1][9] = -1    # int & float = error
cubo[0][2][9] = -1    # int & string = error
cubo[0][3][9] = -1    # int & bool = error

cubo[0][0][10] = -1     # int | int = error
cubo[0][1][10] = -1     # int | float = error
cubo[0][2][10] = -1     # int | string = error
cubo[0][3][10] = -1     # int | bool = error

# FLOAT
cubo[1][0][0] = 1     # float + int = float
cubo[1][1][0] = 1     # float + float = float
cubo[1][2][0] = -1    # float + string = error
cubo[1][3][0] = -1    # float + bool = error

cubo[1][0][1] = 1     # float - int = float
cubo[1][1][1] = 1     # float - float = float
cubo[1][2][1] = -1    # float - string = error
cubo[1][3][1] = -1    # float - bool = error

cubo[1][0][2] = 1     # float * int = float
cubo[1][1][2] = 1     # float * float = float
cubo[1][2][2] = -1    # float * string = error
cubo[1][3][2] = -1    # float * bool = error

cubo[1][0][3] = 1     # float / int = float
cubo[1][1][3] = 1     # float / float = float
cubo[1][2][3] = -1    # float / string = error
cubo[1][3][3] = -1    # float / bool = error

cubo[1][0][4] = 3     # float < int = bool
cubo[1][1][4] = 3     # float < float = bool
cubo[1][2][4] = -1    # float < string = error
cubo[1][3][4] = -1    # float < bool = error

cubo[1][0][5] = 3     # float > int = bool
cubo[1][1][5] = 3     # float > float = bool
cubo[1][2][5] = -1    # float > string = error
cubo[1][3][5] = -1    # float > bool = error

# ERROR
cubo[1][0][6] = -1    # float = int = error
cubo[1][1][6] = -1    # float = float = error
cubo[1][2][6] = -1    # float = string = error
cubo[1][3][6] = -1    # float = bool = error

cubo[1][0][7] = 3     # float <> int = bool
cubo[1][1][7] = 3     # float <> float = bool
cubo[1][2][7] = -1    # float <> string = error
cubo[1][3][7] = -1    # float <> bool = error

cubo[1][0][8] = 3     # float == int = bool
cubo[1][1][8] = 3     # float == float = bool
cubo[1][2][8] = -1    # float == string = error
cubo[1][3][8] = -1    # float == bool = error

cubo[1][0][9] = -1    # float & int = error
cubo[1][1][9] = -1    # float & float = error
cubo[1][2][9] = -1    # float & string = error
cubo[1][3][9] = -1    # float & bool = error

cubo[1][0][10] = -1     # float | int = error
cubo[1][1][10] = -1     # float | float = error
cubo[1][2][10] = -1     # float | string = error
cubo[1][3][10] = -1     # float | bool = error

# STRING
cubo[2][0][0] = -1    # string + int = error
cubo[2][1][0] = -1    # string + float = error
cubo[2][2][0] = -1    # string + string = error
cubo[2][3][0] = -1    # string + bool = error

cubo[2][0][1] = -1    # string - int = error
cubo[2][1][1] = -1    # string - float = error
cubo[2][2][1] = -1    # string - string = error
cubo[2][3][1] = -1    # string - bool = error

cubo[2][0][2] = -1    # string * int = error
cubo[2][1][2] = -1    # string * float = error
cubo[2][2][2] = -1    # string * string = error
cubo[2][3][2] = -1    # string * bool = error

cubo[2][0][3] = -1    # string / int = error
cubo[2][1][3] = -1    # string / float = error
cubo[2][2][3] = -1    # string / string = error
cubo[2][3][3] = -1    # string / bool = error

cubo[2][0][4] = -1    # string < int = error
cubo[2][1][4] = -1    # string < float = error
cubo[2][2][4] = 3     # string < string = bool
cubo[2][3][4] = -1    # string < bool = error

cubo[2][0][5] = -1    # string > int = error
cubo[2][1][5] = -1    # string > float = error
cubo[2][2][5] = 3     # string > string = bool
cubo[2][3][5] = -1    # string > bool = error

# ERROR
cubo[2][0][6] = -1    # string = int = error
cubo[2][1][6] = -1    # string = float = error
cubo[2][2][6] = -1    # string = string = error
cubo[2][3][6] = -1    # string = bool = error

cubo[2][0][7] = -1    # string <> int = error
cubo[2][1][7] = -1    # string <> float = error
cubo[2][2][7] = 3     # string <> string = bool
cubo[2][3][7] = -1    # string <> bool = error

cubo[2][0][8] = -1    # string == int = error
cubo[2][1][8] = -1    # string == float = error
cubo[2][2][8] = 3     # string == string = bool
cubo[2][3][8] = -1    # string == bool = error

cubo[2][0][9] = -1    # string & int = error
cubo[2][1][9] = -1    # string & float = error
cubo[2][2][9] = -1    # string & string = error
cubo[2][3][9] = -1    # string & bool = error

cubo[2][0][10] = -1     # string | int = error
cubo[2][1][10] = -1     # string | float = error
cubo[2][2][10] = -1     # string | string = error
cubo[2][3][10] = -1     # string | bool = error

# BOOL
cubo[3][0][0] = -1    # bool + int = error
cubo[3][1][0] = -1    # bool + float = error
cubo[3][2][0] = -1    # bool + string = error
cubo[3][3][0] = -1    # bool + bool = error

cubo[3][0][1] = -1    # bool - int = error
cubo[3][1][1] = -1    # bool - float = error
cubo[3][2][1] = -1    # bool - string = error
cubo[3][3][1] = -1    # bool - bool = error

cubo[3][0][2] = -1    # bool * int = error
cubo[3][1][2] = -1    # bool * float = error
cubo[3][2][2] = -1    # bool * string = error
cubo[3][3][2] = -1    # bool * bool = error

cubo[3][0][3] = -1    # bool / int = error
cubo[3][1][3] = -1    # bool / float = error
cubo[3][2][3] = -1    # bool / string = error
cubo[3][3][3] = -1    # bool / bool = error

cubo[3][0][4] = -1    # bool < int = error
cubo[3][1][4] = -1    # bool < float = error
cubo[3][2][4] = -1    # bool < string = error
cubo[3][3][4] = -1    # bool < bool = error

cubo[3][0][5] = -1    # bool > int = error
cubo[3][1][5] = -1    # bool > float = error
cubo[3][2][5] = -1    # bool > string = error
cubo[3][3][5] = -1    # bool > bool = error

# ERROR
cubo[3][0][6] = -1    # bool = int = error
cubo[3][1][6] = -1    # bool = float = error
cubo[3][2][6] = -1    # bool = string = error
cubo[3][3][6] = -1    # bool = bool = error

cubo[3][0][7] = -1    # bool <> int = error
cubo[3][1][7] = -1    # bool <> float = error
cubo[3][2][7] = -1    # bool <> string = error
cubo[3][3][7] = 3     # bool <> bool = bool

cubo[3][0][8] = -1    # bool == int = error
cubo[3][1][8] = -1    # bool == float = error
cubo[3][2][8] = -1    # bool == string = error
cubo[3][3][8] = 3     # bool == bool = bool

cubo[3][0][9] = -1    # bool & int = error
cubo[3][1][9] = -1    # bool & float = error
cubo[3][2][9] = -1    # bool & string = error
cubo[3][3][9] = 3     # bool & bool = bool

cubo[3][0][10] = -1     # bool | int = error
cubo[3][1][10] = -1     # bool | float = error
cubo[3][2][10] = -1     # bool | string = error
cubo[3][3][10] = 3    # bool | bool = bool

dicOperadores = {"+" : 0, "-" : 1, "*" : 2, "/" : 3, "<" : 4, ">": 5, "=" : 6,"<>" : 7, "==" : 8, "&": 9, "|": 10}

dicTipos = {"int" : 0, "float" : 1, "string" : 2, "bool" : 3, "error" : -1}



#tipo de tokens que se retornan
tokens = (
  'INT', 
  'FLOAT',
  'STRING',
  'BOOL',
  'PARENTESIS_IZQ',
  'PARENTESIS_DER',
  'RETURN',
  'PUNTO_Y_COMA',
  'WHILE',
  'END_WHILE',
  'CHECKWALL',
  'MOVE',
  'TURN_LEFT',
  'TURN_RIGHT',
  'PICK_BEEPER',
  'PUT_BEEPER',
  'IF',
  'END_IF',
  'ELIF',
  'END_ELIF',
  'ELSE',
  'END_ELSE',
  'PRINT',
  'DEF',
  'END_DEF',
  'SUMA',
  'RESTA',
  'MULTIPLICACION',
  'DIVISION',
  'MENOR_QUE',
  'MAYOR_QUE',
  'EQUIVALE',
  'IGUAL_A',
  'DIFERENTE',
  'MENOR_IGUAL',
  'MAYOR_IGUAL',
  'DOS_PUNTOS',
  'COMA',
  'ID',
  'CTE_INT',
  'CTE_STRING',
  'CTE_FLOAT',
  'CTE_BOOL'
  )

#expresiones regulares
t_SUMA              = r'\+'
t_RESTA             = r'-'
t_MULTIPLICACION    = r'\*'
t_DIVISION          = r'/'
t_PARENTESIS_IZQ    = r'\('
t_PARENTESIS_DER    = r'\)'
t_MENOR_QUE         = r'\<'
t_MAYOR_QUE         = r'\>'
t_MENOR_IGUAL       = r'\<='
t_MAYOR_IGUAL       = r'\>='
t_DIFERENTE         = r'\<>'
t_EQUIVALE          = r'\='
t_IGUAL_A           = r'\=='
t_PUNTO_Y_COMA      = r'\;'
t_DOS_PUNTOS        = r'\:'
t_COMA              = r'\,'


#palabras reservadas del lenguaje
reserved = {
  'int'       : 'INT',
  'float'     : 'FLOAT',
  'string'    : 'STRING',
  'bool'    : 'BOOL',
  'return'    : 'RETURN',
  'while'     : 'WHILE',
  'end_while' : 'END_WHILE',
  'checkWall' : 'CHECKWALL',
  'move'      : 'MOVE',
  'turnLeft'  : 'TURN_LEFT',
  'turnRight' : 'TURN_RIGHT',
  'pickBeeper': 'PICK_BEEPER',
  'putBeeper' : 'PUT_BEEPER',
  'if'        : 'IF',
  'end_if'    : 'END_IF',
  'elif'      : 'ELIF',
  'end_elif'  : 'END_ELIF',
  'else'      : 'ELSE',
  'end_else'  : 'END_ELSE',
  'print'     : 'PRINT',
  'def'       : 'DEF',
  'end_def'   : 'END_DEF',
}

#er de float se debe poner antes de int por que luego reconoce int . int
def t_CTE_FLOAT(t):
    r'[0-9]+\.[[0-9]+]'
    t.value = float(t.value)
    return t

#er de cte int debe ser con d para que pueda funcionar
def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

#er de identidicador, deben comenzar con una letra y oyeden ser seguidos por cualquier letra guión bajo o bien un dígito
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t;

#er de string debe ser definida entre comillas y puede contener cualquier cosa
def t_CTE_STRING(t):
    r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\!]*\"'
    t.type = reserved.get(t.value,'CTE_STRING') 
    return t;

#ignora tabs y spaces
t_ignore  = ' \t'
t_ignore_comentario = '\#.*'

#pasa los endofline
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
      raise errorLexico("Error de Lexico: " + t.value[0] + " en linea : " + t.lexer.lineno)
      sys.exit()

lexer = lex.lex()

##################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################

start = "estatuto"

def p_empty(p):
    'empty :'
    pass

def p_estatuto(p):
    '''
    estatuto : declaracion estatuto_2
             | estatuto_2
    '''

def p_estatuto_2(p):
  '''
  estatuto_2 : opciones estatuto_2
            | empty
  '''

def p_opciones(p):
  '''
  opciones : asignacion
          | function destroyVars
          | condicion
          | escritura
          | ciclo
          | turnleft
          | turnright
          | move
          | checkwall
          | pickbeeper
          | putbeeper
          | funcionUsuario
  '''

def p_declaracion(p):
  '''
  declaracion : tipo ID declaracion_aux imprimePuntoYComa declaracion_3
  '''
  global bscope
  global arregloVar
  global iContadorDiccionarioVar
  global dV
  global tmptipo;
  global tipoDeclaracion

  tmptipo = tipoDeclaracion

  if(bscope == 0):
    arregloVar.append(tablaVar(p[2],tipoDeclaracion,'global'))
  else:
    arregloVar.append(tablaVar(p[2],tipoDeclaracion,'local'))

  if(iContadorDiccionarioVar == 1):
    dV = {iContadorDiccionarioVar : arregloVar[iContadorDiccionarioVar-1]}
  else:
    for x in range(0,iContadorDiccionarioVar - 1):
      if(p[2] == arregloVar[x].getNombre()):
        raise errorSemantico("Variable ya definida: " + p[2])
    dV[iContadorDiccionarioVar] = arregloVar[iContadorDiccionarioVar - 1]

  iContadorDiccionarioVar = iContadorDiccionarioVar + 1
  print(dV)

def p_declaracion_aux(p):
  '''
  declaracion_aux : declaracion_2
          | empty
  '''

def p_declaracion_2(p):
  '''
  declaracion_2 : imprimeComa ID a
  '''

  global bscope
  global arregloVar
  global iContadorDiccionarioVar
  global dV
  global tmptipo

  if(bscope == 0):
    arregloVar.append(tablaVar(p[2],tmptipo,'global'))
  else:
    arregloVar.append(tablaVar(p[2],tmptipo,'local'))

  for x in range(0,iContadorDiccionarioVar - 1):
    if(p[2] == arregloVar[x].getNombre()):
      raise errorSemantico("Variable ya definida: " + p[2])

  dV[iContadorDiccionarioVar] = arregloVar[iContadorDiccionarioVar - 1]   
  iContadorDiccionarioVar = iContadorDiccionarioVar + 1
  print(dV)

def p_a(p):
  '''
  a : declaracion_2
   | empty
  '''

def p_declaracion_3(p):
  '''
  declaracion_3 : declaracion
                | empty
  '''

def p_tipo(p):
  '''
  tipo : INT
       | FLOAT
       | STRING
  '''
  global tipoDeclaracion
  tipoDeclaracion = p[1]
  print(p[1]);

def p_asignacion(p):
  '''
  asignacion : ID  EQUIVALE asignacion_aux

  '''
  global arregloVar
  global iContadorDiccionarioVar
  global tipo
  global PilaO
  global operador
  global operando1
  global operando2
  global resultado
  global iContadorTemporal
  varAux = 0;
  auxTipoStr = ""
  auxTipo = -2
  for x in range(0,iContadorDiccionarioVar - 1):
    if(p[1] != arregloVar[x].getNombre()):
      varAux += 1
    else:
      auxTipoStr = arregloVar[x].getTipo()
      auxTipo = dicTipos[auxTipoStr]
      if(auxTipo != tipo):
        raise errorSemantico("Tipos incompatibles de variables en :" + p[1])
      else:
        operador = "="
        operando2 = PilaO.pop()
        operando1 = PilaO.pop()
        resultado.append(operando1)
        arregloCuadruplos.append(cuadruplo(operador,operando2,"nul",resultado[iContadorTemporal]))
        PilaO.push(resultado[iContadorTemporal])
        iContadorTemporal += 1


  if(varAux == iContadorDiccionarioVar - 1):
  	raise errorSemantico("Variable no declarada: " + p[1])

def p_asignacion_aux(p):
	'''
	asignacion_aux : exp imprimePuntoYComa
					       | funcionUsuario
	'''

def p_exp(p):
  '''
  exp : expresion exp_2
  '''

def p_exp_2(p):
  '''
  exp_2 : imprimeDiferente expresion
      | imprimeMayorQue expresion
      | imprimeMenorQue expresion
      | imprimeIgualA expresion
      | imprimeMayorIgual expresion
      | imprimeMenorIgual expresion
      | empty
  '''

def p_expresion(p):
  '''
  expresion : termino reglaOperadorMM expresion_2
  '''
  global op
  global tipo
  if(op != -2):
    if(tipo == -2):
      tipo = cubo[op1][op2][op]
    else:
      tipo = cubo[tipo][op2][op]
    if(tipo == -1):
      raise errorSemantico("Uso incorrecto de tipos ")

def p_reglaOperadorMM(p):
  '''
  reglaOperadorMM : empty
  '''
  global POper
  global PilaO
  global operador
  global operando1
  global operando2
  global resultado
  global iContadorTemporal
  if(POper.isEmpty() == 0):
    if(POper.top() == "+" or POper.top() == "-"):
      operador = POper.pop()
      operando2 = PilaO.pop()
      operando1 = PilaO.pop()
      resultado[iContadorTemporal] = iContadorTemporal + 1
      arregloCuadruplos.append(cuadruplo(operador,operando1,operando2,resultado[iContadorTemporal]))
      PilaO.push(resultado[iContadorTemporal])
      iContadorTemporal += 1

def p_expresion_2(p):
  '''
  expresion_2 : SUMA expresion
              | RESTA expresion
              | empty
  '''
  global op
  global POper
  if(p[1] == "+"):
    op = dicOperadores["+"]
    POper.push(p[1])
  elif(p[1] == "-"):
    op = dicOperadores["-"]
    POper.push(p[1])


def p_termino(p):
  '''
  termino : factor reglaOperadorMD termino_2
  '''
  global op
  global tipo
  if(op != -2):
    if(tipo == -2):
      tipo = cubo[op1][op2][op]
    else:
      tipo = cubo[tipo][op2][op]
    if(tipo == -1):
      raise errorSemantico("Uso incorrecto de tipos ")

def p_reglaOperadorMD(p):
  '''
  reglaOperadorMD : empty
  '''
  global POper
  global PilaO
  global operador
  global operando1
  global operando2
  global resultado
  global iContadorTemporal
  if(POper.isEmpty() == 0):
    if(POper.top() == "*" or POper.top() == "/"):
      operador = POper.pop()
      operando2 = PilaO.pop()
      operando1 = PilaO.pop()
      resultado[iContadorTemporal] = iContadorTemporal + 1
      arregloCuadruplos.append(cuadruplo(operador,operando1,operando2,resultado[iContadorTemporal]))
      PilaO.push(resultado[iContadorTemporal])
      iContadorTemporal += 1




def p_termino_2(p):
  '''
  termino_2 : MULTIPLICACION termino
            | DIVISION termino
            | empty
  '''
  global op
  global POper
  if(p[1] == '*'):
    op = dicOperadores["*"]
    POper.push(p[1])
  elif(p[1] == '/'):
    op = dicOperadores["/"]
    POper.push(p[1])

def p_factor(p):
  '''
  factor : imprimeParentesisIzq exp imprimeParentesisDer
         | var_cte
  '''

def p_var_cte(p):
  '''
  var_cte : matchID
          | matchCteInt
          | matchCteFloat
  '''

def p_matchID(p):
  '''
  matchID : ID
  '''
  global arregloVar
  global iContadorDiccionarioVar
  global op1
  global op2
  global PilaO
  varAux = 0
  auxTipo = ""
  for x in range(0,iContadorDiccionarioVar - 1):
    if(p[1] != arregloVar[x].getNombre()):
      varAux += 1
    else:
      auxTipo = arregloVar[x].getTipo()
      if(op1 != -2):
        op2 = dicTipos[auxTipo]
        print("op2 asignado")
      else:
        op1 = dicTipos[auxTipo]
        print("op1 asignado")
      PilaO.push(p[1])

  if(varAux == iContadorDiccionarioVar - 1):
    raise errorSemantico("Variable no declarada: " + p[1])

def p_matchCteInt(p):
  '''
  matchCteInt : CTE_INT
  '''
  global op1
  global op2
  global PilaO
  if(op1 != -2):
    op2 = dicTipos["int"]
  else:
    op1 = dicTipos["int"]
  PilaO.push(p[1])

def p_matchCteFloat(p):
  '''
  matchCteFloat : CTE_FLOAT
  '''
  global op1
  global op2
  global PilaO
  if(op1 != -2):
    op2 = dicTipos["float"]
  else:
    op1 = dicTipos["float"]
  PilaO.push(p[1])

def p_condicion(p):
  '''
  condicion : imprimeIf condicion_2 imprimeDosPuntos estatuto_2 imprimeEndIf condicion_3 condicion_4
  '''

def p_condicion_2(p):
  '''
  condicion_2 : exp 
            | checkwall
  '''

def p_condicion_3(p):
  '''
  condicion_3 : imprimeElif condicion_2 imprimeDosPuntos estatuto_2 imprimeEndElif condicion_3
              | empty
  '''

def p_condicion_4(p):
  '''
  condicion_4 : imprimeElse imprimeDosPuntos estatuto_2 imprimeEndElse
              | empty
  '''

def p_escritura(p):
  '''
  escritura : imprimePrint imprimeParentesisIzq escritura_2 imprimeParentesisDer imprimePuntoYComa
  '''

def p_escritura_2(p):
  '''
  escritura_2 : CTE_STRING
              | exp
  '''

def p_ciclo(p):
  '''
  ciclo : imprimeWhile exp imprimeDosPuntos estatuto_2 imprimeEndWhile
  '''

def p_function(p):
  '''
  function : imprimeDef aux ID imprimeParentesisIzq function_aux imprimeParentesisDer imprimeDosPuntos estatuto function_4 imprimeEndDef
  '''
  global bscope
  global arregloFuncion
  global iContadorDiccionarioFuncion
  global dF

  arregloFuncion.append(tablaFunciones(p[3],p[2]))

  if(iContadorDiccionarioFuncion == 1):
    dF = {iContadorDiccionarioFuncion : arregloFuncion[iContadorDiccionarioFuncion-1]}
  else:
    for x in range(0,iContadorDiccionarioFuncion - 1):
      if(p[3] == arregloFuncion[x].getNombre()):
        raise errorSemantico("Función previamente definida: " + p[3])
    dF[iContadorDiccionarioFuncion] = arregloFuncion[iContadorDiccionarioFuncion - 1]
    
  iContadorDiccionarioFuncion = iContadorDiccionarioFuncion + 1
  print(dF)
  bscope = 0

def p_aux(p):
  '''
  aux : tipo
    | empty
  '''

def p_function_aux(p):
  '''
  function_aux : function_2
               | empty
  '''

def p_function_2(p):
  '''
  function_2 : tipo ID function_3
  '''
  global arregloVar
  global iContadorDiccionarioVar
  global dV

  arregloVar.append(tablaVar(p[2],p[1],'local'))

  print(arregloVar)

  if(iContadorDiccionarioVar == 1):
    dV = {iContadorDiccionarioVar : arregloVar[iContadorDiccionarioVar-1]}
  else:
    for x in range(0,iContadorDiccionarioVar - 1):
      if(p[2] == arregloVar[x].getNombre()):
        raise errorSemantico("Variable ya definida: " + p[2])
    dV[iContadorDiccionarioVar] = arregloVar[iContadorDiccionarioVar - 1]

  iContadorDiccionarioVar = iContadorDiccionarioVar + 1

def p_function_3(p):
  '''
  function_3 : COMA function_aux
            | empty
  '''

def p_function_4(p):
  '''
  function_4 : imprimeReturn function_5 imprimePuntoYComa
              | empty
  '''

def p_function_5(p):
  '''
  function_5 : exp
            | empty
  ''' 

def p_destroyVars(p):
  '''
  destroyVars : empty
  '''
  global arregloVar
  global dV
  global iContadorInicioLocal
  global iAux
  global iContadorDiccionarioVar

  iAux = iContadorInicioLocal
  del arregloVar[iContadorInicioLocal:iContadorDiccionarioVar - 1]
  for x in range(iContadorInicioLocal + 1 , iContadorDiccionarioVar):
    del dV[x]
  iContadorDiccionarioVar = iAux + 1

  print(len(dV))

#define la sintaxixs de una función de usuario
def p_funcionUsuario(p):
  '''
  funcionUsuario : ID imprimeParentesisIzq functionUsuario_parametros imprimeParentesisDer imprimePuntoYComa
  '''
  #checa si la función que tratas de usar existe o no, en caso de no existir levanata una excepción
  global arregloFuncion
  global iContadorDiccionarioFuncion
  global tipo
  auxTipo
  varAux = 0
  for x in range(0,iContadorDiccionarioFuncion - 1):
    if(p[1] != arregloFuncion[x].getNombre()):
      varAux += 1
    else:
      auxTipo = arregloFuncion[x].getTipo()
      tipo = dicTipos[auxTipo]
  if(varAux == iContadorDiccionarioFuncion - 1):
    raise errorSemantico("Función no definida: " + p[1] + "()")

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_parametros(p):
  '''
  functionUsuario_parametros : functionUsuario_aux1
               				| empty
  '''

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_aux1(p):
  '''
  functionUsuario_aux1 : tipo ID functionUsuario_aux2
  '''

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_aux2(p):
  '''
  functionUsuario_aux2 : COMA functionUsuario_aux1
            			| empty
  '''

#función de sintaxis que revisa si se recive la función predeinida de checkWall();
def p_checkwall(p):
  '''
  checkwall : CHECKWALL imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  print("Encontré un checkwall\n")

#función de sintaxis que revisa si se recive la función predeinida de move();
def p_move(p):
  '''
  move : MOVE imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  print("Encontré un move\n")

#función de sintaxis que revisa si se recive la función predeinida de turnRight();
def p_turnright(p):
  '''
  turnright : TURN_RIGHT imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  print("Encontré un turnright\n")

#función de sintaxis que revisa si se recive la función predeinida de turnLeft();
def p_turnleft(p):
  '''
  turnleft : TURN_LEFT imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  print("Encontré un turnleft\n")

#función de sintaxis que revisa si se recive la función predeinida de pickBeeper();
def p_pickbeeper(p):
  '''
  pickbeeper : PICK_BEEPER imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  print("Encontré un pickbeeper\n")

#función de sintaxis que revisa si se recive la función predeinida de putBeeper();
def p_putbeeper(p):
  '''
  putbeeper : PUT_BEEPER imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  print("Encontré un putbeeper")

#########################################################################################################################################################################
########################################################################################################################################################################
#########################################################################################################################################################################

def p_imprimeReturn(p):
  '''
  imprimeReturn : RETURN
  '''
  print(p[1])

def p_imprimeDef(p):
  '''
  imprimeDef : DEF
  '''
  global bscope
  global iContadorInicioLocal
  bscope = 1
  iContadorInicioLocal = iContadorDiccionarioVar-1
  print(p[1])

def p_imprimeEndDef(p):
  '''
  imprimeEndDef : END_DEF
  '''
  print(p[1])

def p_imprimeWhile(p):
  '''
  imprimeWhile : WHILE
  '''
  print(p[1])

def p_imprimeEndWhile(p):
  '''
  imprimeEndWhile : END_WHILE
  '''
  print(p[1])

def p_imprimePrint(p):
  '''
  imprimePrint : PRINT
  '''
  print(p[1])

def p_imprimeParentesisIzq(p):
  '''
  imprimeParentesisIzq : PARENTESIS_IZQ
  '''
  print(p[1])

def p_imprimeParentesisDer(p):
  '''
  imprimeParentesisDer : PARENTESIS_DER
  '''
  print(p[1])

def p_imprimeElse(p):
  '''
  imprimeElse : ELSE
  '''
  print(p[1])

def p_imprimeEndElse(p):
  '''
  imprimeEndElse : END_ELSE
  '''
  print(p[1])

def p_imprimeElif(p):
  '''
  imprimeElif : ELIF
  '''
  print(p[1])

def p_imprimeEndElif(p):
  '''
  imprimeEndElif : END_ELIF
  '''
  print(p[1])

def p_imprimeIf(p):
  '''
  imprimeIf : IF
  '''
  print(p[1])

def p_imprimeDosPuntos(p):
  '''
  imprimeDosPuntos : DOS_PUNTOS
  '''
  print(p[1])

def p_imprimeEndIf(p):
  '''
  imprimeEndIf : END_IF
  '''
  print(p[1])

def p_imprimeDiferente(p):
  '''
  imprimeDiferente : DIFERENTE
  '''
  print(p[1])

def p_imprimeMayorQue(p):
  '''
  imprimeMayorQue : MAYOR_QUE
  '''
  print(p[1])

def p_imprimeMenorQue(p):
  '''
  imprimeMenorQue : MENOR_QUE
  '''
  print(p[1])

def p_imprimeIgualA(p):
  '''
  imprimeIgualA : IGUAL_A
  '''
  print(p[1])

def p_imprimeMayorIgual(p):
  '''
  imprimeMayorIgual : MAYOR_IGUAL
  '''
  print(p[1])

def p_imprimeMenorIgual(p):
  '''
  imprimeMenorIgual : MENOR_IGUAL
  '''
  print(p[1])

def p_imprimeEquivale(p):
  '''
  imprimeEquivale : EQUIVALE
  '''
  print(p[1])

def p_imprimeID(p):
    '''
    imprimeID : ID
    '''
    print("ID : {} ".format(p[1]))

def p_imprimePuntoYComa(p):
  '''
  imprimePuntoYComa : PUNTO_Y_COMA
  '''
  print(p[1])

def p_imprimeComa(p):
  '''
  imprimeComa : COMA
  '''
  print(p[1])

############################################################################################################################################################
############################################################################################################################################################
###########################################################################################################################################################

# Error rule for syntax errors
def p_error(p):
  raise errorSintactico("Error de sintaxis")

# Build the parser
parser = yacc.yacc()
data = ""
f = open('prueba.txt', 'r')
for line in f:
  if not line.strip():
    continue
  else:
    data = data + line
result = parser.parse(data)


