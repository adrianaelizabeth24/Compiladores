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
import ply.lex as lex
import ply.yacc as yacc
import sys

#variables globales
#boleanas
bscope = 0
bCiclo = 0
bIf = 0
bRetorna = 0
#enteros (contadores)
iContadorDiccionarioVar = 1
iContadorDiccionarioFuncion = 1
iContadorInicioLocal = 0
iContadorTemporal = 0
iContadorCuadruplos = 0
iContadorParametros = 0
iAux = 0
#enteros indicadores
op = -2
op1 = -2
op2 = -2
tipo = -2

#strings
tipoDeclaracion = ""
tipoDeclaracionFuncion = ""
tmptipo = ""
operador = ""
operando1 = ""
operando2 = ""
nombreFuncion = ""
memTipo = ""
funcionActiva = ""

#arreglos, pilas y filas
arregloVar = []
arregloFuncion = []
resultado = []
PilaO = []
POper = []
PSaltos = []
PSaltosAux = []
PTipo = []
arregloCuadruplos = []

#diccionarios
dV = {}
dF = {}

#apuntadores a memoria
vgi = 5000
vli= 5300
vgf = 6000
vlf = 6300
vgs = 7000
vls = 7300
vgb = 8000
vlb = 8300
tgi = 9000
tgf = 10000
tgs = 11000
tgb = 12000
ctei = 43000
ctef = 44000
ctes = 45000
cteb = 46000

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

cubo[0][0][3] = 1     # int / int = float
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
cubo[0][0][6] = 0    # int = int = int (por que cuando asignas int a int el temporal te debe guardar int)
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
cubo[1][1][6] = 1    # float = float = float (por que asignas)
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
cubo[2][2][6] = 2    # string = string = string (asignas!)
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
cubo[3][3][6] = 3    # bool = bool = bool (asignas!)

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
  'VOID',
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
  'MAIN',
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
  'TRUE'
  'FALSE'
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
  'void'    : 'VOID',
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
  'main'	: 'MAIN',
  'true'  : 'TRUE',
  'false' : 'FALSE'
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

def t_CTE_BOOL(t):
    r'\"[True|False]\"'
    t.type = reserved.get(t.value,'CTE_BOOL') 
    return t;

#ignora tabs y spaces
t_ignore  = ' \t'
t_ignore_comentario = '\#.*'

#pasa los endofline
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#excepción de error léxico
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
    estatuto : start declaracion declaracion_3 function_declaration matchMain DOS_PUNTOS estatuto_2
             | start function_declaration matchMain DOS_PUNTOS estatuto_2
    '''

def p_start(p):
	'''
	start : empty
	'''
	global PSaltos
	global iContadorCuadruplos
	global arregloCuadruplos
	global resultado
	PSaltos.append(iContadorCuadruplos)
	resultado.append(-2)
	arregloCuadruplos.append(cuadruplo("GotoMain",-2,"nul","nul"))
	iContadorCuadruplos+=1

def p_matchMain(p):
	'''
	matchMain : MAIN
	'''
	global PSaltos
	global arregloCuadruplos
	global iContadorCuadruplos
	global operador
	global resultado

	  #saca el tope de Psaltos , que es el apuntador al "gotof"
	res = PSaltos.pop()
	#al cuadruplo ubicado en la posición res le mete contador temporal + 1 porque apunta a la siguiente direccion
	arregloCuadruplos[res].setOperando1(iContadorCuadruplos + 1)
	print(p[1])

def p_function_declaration(p):
	'''
	function_declaration : function destroyVars function_declaration
						| empty
	'''

def p_estatuto_2(p):
  '''
  estatuto_2 : opciones estatuto_2
            | empty
  '''

def p_opciones(p):
  '''
  opciones : asignacion
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
  declaracion : tipo ID declaracion_aux imprimePuntoYComa
  '''
  global bscope
  global arregloVar
  global iContadorDiccionarioVar
  global dV
  global tipoDeclaracion
  global vgi
  global vli
  global vgf
  global vlf
  global vgs
  global vls
  global arrGI, arrLI,arrGF,arrLF,arrGS,arrLS

  if(bscope == 0):
    arregloVar.append(tablaVar(p[2],tipoDeclaracion,'global'))
  else:
    arregloVar.append(tablaVar(p[2],tipoDeclaracion,'local'))

  if(iContadorDiccionarioVar == 1):
    dV = {iContadorDiccionarioVar : arregloVar[iContadorDiccionarioVar-1]}
    if(tipoDeclaracion == "int" and bscope == 0):
    	vgi+=1
    elif(tipoDeclaracion == "int" and bscope == 1):
    	vli+=1
    elif(tipoDeclaracion == "float" and bscope == 0):
    	vgf+=1
    elif(tipoDeclaracion == "float" and bscope == 1):
    	vlf+=1
    elif(tipoDeclaracion == "string" and bscope == 0):
    	vgs+=1
    elif(tipoDeclaracion == "string" and bscope == 1):
    	vls+=1
  else:
    for x in range(0,iContadorDiccionarioVar - 1):
      if(p[2] == arregloVar[x].getNombre()):
        raise errorSemantico("Variable ya definida: " + p[2])
    dV[iContadorDiccionarioVar] = arregloVar[iContadorDiccionarioVar - 1]

  iContadorDiccionarioVar = iContadorDiccionarioVar + 1
  for x in range(0,iContadorDiccionarioVar-1):
    print(arregloVar[x].getNombre())
    print(arregloVar[x].getTipo())
    print(arregloVar[x].getScope())
    print("--------------------")
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
  global tipoDeclaracion

  if(bscope == 0):
    arregloVar.append(tablaVar(p[2],tipoDeclaracion,'global'))
  else:
    arregloVar.append(tablaVar(p[2],tipoDeclaracion,'local'))

  for x in range(0,iContadorDiccionarioVar - 1):
    if(p[2] == arregloVar[x].getNombre()):
      raise errorSemantico("Variable ya definida: " + p[2])

  dV[iContadorDiccionarioVar] = arregloVar[iContadorDiccionarioVar - 1]   
  iContadorDiccionarioVar = iContadorDiccionarioVar + 1
  if(tipoDeclaracion == "int" and bscope == 0):
  	vgi+=1
  elif(tipoDeclaracion == "int" and bscope == 1):
  	vli+=1
  elif(tipoDeclaracion == "float" and bscope == 0):
  	vgf+=1
  elif(tipoDeclaracion == "float" and bscope == 1):
   	vlf+=1
  elif(tipoDeclaracion == "string" and bscope == 0):
   	vgs+=1
  elif(tipoDeclaracion == "string" and bscope == 1):
   	vls+=1
  print(dV)

def p_a(p):
  '''
  a : declaracion_2
   | empty
  '''

def p_declaracion_3(p):
  '''
  declaracion_3 : declaracion declaracion_3
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
  asignacion : matchID EQUIVALE asignacion_aux

  '''
  global arregloVar
  global iContadorDiccionarioVar
  global tipo
  global PilaO
  global PTipo
  global op
  global op1
  global op2
  global tipo
  global operador
  global operando1
  global operando2
  global resultado
  global iContadorTemporal
  global iContadorCuadruplos
  varAux = 0;
  operador = "="
  operando2 = PilaO.pop()
  operando1 = PilaO.pop()
  op2 = PTipo.pop()
  op1 = PTipo.pop()
  op = dicOperadores["="]
  print("operador : ")
  print(op)
  print("op2 :")
  print(op2)
  print("op1 :")
  print(op1)
  tipo = cubo[op1][op2][op]

  if(tipo == -1):
  	raise errorSemantico("Uso incorrecto de tipos ")
  else:
  	PTipo.append(tipo)
  	resultado.append(operando1)
  	arregloCuadruplos.append(cuadruplo(operador,operando2,"nul",resultado[iContadorCuadruplos]))
  	PilaO.append(resultado[iContadorCuadruplos])
  	iContadorCuadruplos += 1

def p_asignacion_aux(p):
	'''
	asignacion_aux : expresion imprimePuntoYComa
					| funcionUsuario
	'''

def p_exp(p):
  '''
  exp : expresion exp_2
  '''

def p_exp_2(p):
  '''
  exp_2 : DIFERENTE expresion
      | MAYOR_QUE expresion
      | MENOR_QUE expresion
      | IGUAL_A expresion
      | MAYOR_IGUAL expresion
      | MENOR_IGUAL expresion
      | empty
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
  global iContadorCuadruplos
  global dicTipos
  global PTipo

  ## cuadruplos de condicion
  # toma el operador 1 y los operandos
  operador = p[1]
  operando2 = PilaO.pop()
  operando1 = PilaO.pop()
  iContadorTemporal += 1
  resultado.append(iContadorTemporal)
  op2 = PTipo.pop()
  op1 = PTipo.pop()
  op = dicTipos[operador]
  tipo = cubo[op1][op2][op]
  if(tipo != 3):
    raise errorSemantico("uso incorrecto de tipos ")
  else:
  	#genera el cuadruplo
  	arrTB.append(iContadorTemporal)
  	tgb+=1
  	arregloCuadruplos.append(cuadruplo(operador,operando2,operando1,resultado[iContadorCuadruplos]))
  	#el temporal lo mete a la pila
  	PilaO.append(iContadorTemporal)
  	#suma uno al contador
  	iContadorCuadruplos += 1

def p_expresion(p):
  '''
  expresion : termino expresion_2
  '''
  global POper
  global PilaO
  global PTipo
  global op
  global tipo
  global dicOperadores
  global operador
  global operando1
  global operando2
  global resultado
  global iContadorTemporal
  global iContadorCuadruplos

  if(len(POper) > 0):
    if(POper[-1] == "+" or POper[-1] == "-"):
      operador = POper.pop()
      operando2 = PilaO.pop()
      operando1 = PilaO.pop()
      iContadorTemporal += 1
      op2 = PTipo.pop()
      op1 = PTipo.pop()
      if (operador == "+"):
      	op = dicOperadores["+"]
      else:
      	op = dicOperadores["-"]
      tipo = cubo[op1][op2][op]
      if(tipo == -1):
      	raise errorSemantico("uso incorrecto de tipos ")
      else:
      	if(tipo == 1):
      		tgi+=1
      	elif(tipo == 2):
      		tgf+=2
      	PTipo.append(tipo)
      	resultado.append(iContadorTemporal)
      	arregloCuadruplos.append(cuadruplo(operador,operando1,operando2,resultado[iContadorCuadruplos]))
      	PilaO.append(iContadorTemporal)
      	iContadorCuadruplos += 1

def p_expresion_2(p):
  '''
  expresion_2 : SUMA expresion
              | RESTA expresion
              | empty
  '''
  global POper
  if(p[1] == "+"):
    POper.append(p[1])
  elif(p[1] == "-"):
    POper.append(p[1])

def p_termino(p):
  '''
  termino : factor termino_2
  '''
  ##generacion de cuadruplos
  global op
  global tipo
  global op1
  global op2
  global POper
  global PilaO
  global PTipo
  global operador
  global operando1
  global operando2
  global resultado
  global dicOperadores
  global iContadorTemporal
  global iContadorCuadruplos
  #entra si ya entro una multiplicacion o division a la pila o suma o resta
  if(len(POper) > 0):
  	#pregunta si el tope es multiplicacion o division en caso de serlo prosigue
    if(POper[-1] == "*" or POper[-1] == "/"):
      #saca el operador y ambos operandos
      operador = POper.pop()
      operando2 = PilaO.pop()
      operando1 = PilaO.pop()
      iContadorTemporal += 1
      op2 = PTipo.pop()
      op1 = PTipo.pop()
      if (operador == "*"):
      	op = dicOperadores["*"]
      else:
      	op = dicOperadores["/"]
      tipo = cubo[op1][op2][op]
      if(tipo == -1):
      	raise errorSemantico("uso incorrecto de tipos ")
      else:
      	if(tipo == 1):
      		tgi+=1
      	elif(tipo == 2):
      		tgf+=2
      	PTipo.append(tipo)
      	#al arreglo de resultados mete el numero de temporal
      	resultado.append(iContadorTemporal)
      	#genera un nuevo cuadruplo
      	arregloCuadruplos.append(cuadruplo(operador,operando1,operando2,resultado[iContadorCuadruplos]))
      	#mete el temporal
      	PilaO.append(iContadorTemporal)
      	iContadorCuadruplos += 1

def p_termino_2(p):
  '''
  termino_2 : MatchMultiplicacion
            | MatchDivision
            | empty
  '''

def p_MatchMultiplicacion(p):
  '''
  MatchMultiplicacion : MULTIPLICACION termino
  '''
  #si llega una multiplicacion la mete dentro de la pila de operadores
  global POper
  POper.append(p[1])

def p_MatchDivision(p):
  '''
  MatchDivision : DIVISION termino
  '''
  #si llega una division la mete en la pila de operadores
  global POper
  POper.append(p[1])

def p_factor(p):
  '''
  factor : imprimeParentesisIzq expresion imprimeParentesisDer
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
  global PTipo
  global dicTipos
  varAux = 0
  tipo = ""
  auxTipo = -2
  #Checa si variable esta o no declarada
  for x in range(0,iContadorDiccionarioVar - 1):
    if(p[1] != arregloVar[x].getNombre()):
      varAux += 1
    else:
      #cubo semantico tipo de dato correcto
      tipo = arregloVar[x].getTipo()
      auxTipo = dicTipos[tipo]
      PTipo.append(auxTipo)
      #Meter a pila operadores paso 1 del algoritmo
      PilaO.append(p[1])
  #No esta declarada
  if(varAux == iContadorDiccionarioVar - 1):
    raise errorSemantico("Variable no declarada: " + p[1])

def p_matchCteInt(p):
  '''
  matchCteInt : CTE_INT
  '''
  global PilaO
  global PTipo
  global dicTipos
  global arrCI
  global ctei
  auxTipo = -2

  auxTipo = dicTipos["int"]
  PTipo.append(auxTipo)

  #meter a pila de operadores
  PilaO.append(p[1])
  ctei+=1

def p_matchCteFloat(p):
  '''
  matchCteFloat : CTE_FLOAT
  '''
  global PilaO
  global PTipo
  global dicTipos
  global arrCF
  global ctef
  auxTipo = -2
  #cubo semantico toma el valor float directamente y lo guarda en op2 si op1 está ocupado

  auxTipo = dicTipos["float"]
  PTipo.append(auxTipo)
  #mete la constante a la pila de operandos
  PilaO.append(p[1])
  ctef+=1

def p_condicion(p):
  '''
  condicion : imprimeIf imprimeParentesisIzq condicion_2 imprimeParentesisDer imprimeDosPuntos cuacondicion1 estatuto_2 imprimeEndIf condicion_3 condicion_4
  '''

def p_cuacondicion1(p):
  '''
  cuacondicion1 : empty
  '''
  global operador
  global operando1
  global operando2
  global resultado
  global iContadorCuadruplos
  global PSaltos
  global PilaO
  global arregloCuadruplos
  global PSaltos
  #genera de operador gotof
  operador = "GotoFIf"
  #el operando 1 es el temporal o ultima variable localizada en pila o
  operando1 = PilaO.pop()
  #agrega la posición actual a la pila de saltos
  PSaltos.append(iContadorCuadruplos)
  #el resultado le asigna -2 para estandarizar que está vacio
  resultado.append(-2)
  #genera el cuadruplo
  arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
  #suma uno al contador
  iContadorCuadruplos += 1

def p_condicion_2(p):
  '''
  condicion_2 : exp 
            | checkwall
  '''

def p_condicion_3(p):
  '''
  condicion_3 : ELIF imprimeParentesisIzq condicion_2 imprimeParentesisDer imprimeDosPuntos cuacondicion1 estatuto_2 imprimeEndElif condicion_3
              | empty
  '''

def p_condicion_4(p):
  '''
  condicion_4 : ELSE imprimeDosPuntos estatuto_2 imprimeEndElse
              | empty
  '''
  global PSaltosAux
  global iContadorCuadruplos
  global arregloCuadruplos
  if(p[1] != "else"):
    while(len(PSaltosAux)>0):
      res = PSaltosAux.pop()
      arregloCuadruplos[res].setResultado(iContadorCuadruplos + 1)

def p_escritura(p):
  '''
  escritura : imprimePrint imprimeParentesisIzq escritura_2 imprimeParentesisDer imprimePuntoYComa
  '''
  global operador
  global operando1
  global resultado
  global PilaO
  global arregloCuadruplos
  global iContadorCuadruplos

  operador = "print"
  operando1 = PilaO.pop()
  resultado.append("nul")
  arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos += 1

def p_escritura_2(p):
  '''
  escritura_2 : matchCteString
              | expresion
  '''

def p_matchCteString(p):
	'''
	matchCteString : CTE_STRING
	'''
	global arrCS
	global ctes
	ctes+=1

#funcion de sintaxis del ciclo --> estructura "while ( expresion ) : codigo end_while"
def p_ciclo(p):
  '''
  ciclo : imprimeWhile imprimeParentesisIzq exp imprimeParentesisDer imprimeDosPuntos cuaciclo1 estatuto_2 imprimeEndWhile
  '''

#funcion auxiliar para ayudar a generar el cuadruplo gotof
def p_cuaciclo1(p):
  '''
  cuaciclo1 : empty
  '''
  global operador
  global operando1
  global operando2
  global resultado
  global iContadorCuadruplos
  global PSaltos
  global PilaO
  global arregloCuadruplos
  global PSaltos
  #genera de operador gotof
  operador = "GotoFC"
  #el operando 1 es el temporal o ultima variable localizada en pila o
  operando1 = PilaO.pop()
  #agrega la posición actual a la pila de saltos
  PSaltos.append(iContadorCuadruplos)
  #el resultado le asigna -2 para estandarizar que está vacio
  resultado.append(-2)
  #genera el cuadruplo
  arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
  #suma uno al contador
  iContadorCuadruplos += 1

def p_function(p):
  '''
  function : imprimeDef tipoFunction ID imprimeParentesisIzq function_aux imprimeParentesisDer imprimeDosPuntos estatuto_2 function_4 imprimeEndDef
  '''
  global bscope
  global arregloFuncion
  global iContadorDiccionarioFuncion
  global dF
  global tipoDeclaracionFuncion

  arregloFuncion.append(tablaFunciones(p[3],tipoDeclaracionFuncion))

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

def p_tipoFunction(p):
  '''
  tipoFunction : INT
       		   | FLOAT
       		   | STRING
       		   | VOID
  '''
  global tipoDeclaracionFuncion
  global bRetorna
  tipoDeclaracionFuncion = p[1]
  if(p[1] != "void"):
  	bRetorna = 1
  print(p[1]);

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
  function_4 : RETURN expresion PUNTO_Y_COMA
              | empty
  '''
  global PilaO, PTipo
  global arregloCuadruplos
  global iContadorCuadruplos
  global operando1, operador, resultado, operando2, op1,op2, op
  global tipoDeclaracionFuncion
  global dicOperadores,dicTipos
  global bRetorna
  if((bRetorna == 1) and (p[1] != 'return')):
    raise errorSemantico("Definiste una funcion que debe retornar un valor y no lo retorna ")
  if(p[1] == 'return'):
  	op1 = PTipo.pop()
  	op2 = dicTipos[tipoDeclaracionFuncion]
  	op = dicOperadores["="]
  	tipo = cubo[op1][op2][op]
  	if(tipo == -1):
  		raise errorSemantico("uso incorrecto de tipos ")
  	else:
  		operando1 = PilaO.pop()
  		operador = "Return"
  		resultado.append(-2)
  		arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
  		iContadorCuadruplos+=1

def p_destroyVars(p):
  '''
  destroyVars : empty
  '''
  global arregloVar
  global dV
  global iContadorInicioLocal
  global iAux
  global iContadorDiccionarioVar
  global resultado
  global arregloCuadruplos
  global iContadorTemporal
  global vli,vlf,vls,vlb,tgi,tgf,tgs,tgb

  iAux = iContadorInicioLocal
  del arregloVar[iContadorInicioLocal:iContadorDiccionarioVar - 1]
  for x in range(iContadorInicioLocal + 1 , iContadorDiccionarioVar):
    del dV[x]
  iContadorDiccionarioVar = iAux + 1
  iContadorTemporal = iContadorDiccionarioVar - iContadorInicioLocal
  vli= 5300
  vlf = 6300
  vls = 7300
  vlb = 8300
  tgi -= iContadorInicioLocal
  tgf -= iContadorInicioLocal
  tgs -= iContadorInicioLocal
  tgb -= iContadorInicioLocal

  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("ret","nul","nul",resultado[iContadorCuadruplos]))

  print(len(dV))

#define la sintaxixs de una función de usuario
def p_funcionUsuario(p):
  '''
  funcionUsuario : matchFunction imprimeParentesisIzq era_func functionUsuario_parametros imprimeParentesisDer imprimePuntoYComa go_sub
  '''

def p_matchFunction(p):
	'''
	matchFunction : ID
	'''
	#checa si la función que tratas de usar existe o no, en caso de no existir levanata una excepción
	global arregloFuncion
	global iContadorDiccionarioFuncion
	global funcionActiva
	varAux = 0
	auxTipo = ""
	for x in range(0,iContadorDiccionarioFuncion - 1):
		if(p[1] != arregloFuncion[x].getNombre()):
			varAux += 1
		if(varAux == iContadorDiccionarioFuncion - 1):
			raise errorSemantico("Funcion no definida: " + p[1])
		else:
			funcionActiva = p[1]
			auxTipo = arregloFuncion[x].getTipo()
			if(auxTipo != "void"):
				tipo = dicTipos[auxTipo]

def p_era_func(p):
	'''
	era_func : empty
	'''
	global PilaO
	global iContadorTemporal
	global arregloCuadruplos
	global resultado
	global nombreFuncion
	global iContadorCuadruplos
	global funcionActiva

	resultado.append(-2)
	arregloCuadruplos.append(cuadruplo("era",funcionActiva,"nul",-2))
	iContadorCuadruplos+=1

def p_go_sub(p):
	'''
	go_sub : empty
	'''
	global iContadorTemporal
	global arregloCuadruplos, arregloFuncion
	global resultado
	global iContadorCuadruplos
	global iContadorDiccionarioFuncion
	global funcionActiva
	global PTipo
	global dicTipos
	tipo = ""
	tipoDic = -2
	resultado.append(-2)
	arregloCuadruplos.append(cuadruplo("gosub",funcionActiva,"nul",-2))
	iContadorCuadruplos+=1
	for x in range(0,iContadorDiccionarioFuncion - 1):
		if(arregloFuncion[x].getNombre() == funcionActiva):
			tipo = arregloFuncion[x].getTipo();
	if(tipo != "void"):
		print("mi tipo es ")
		print(tipo)
		tipoDic = dicTipos[tipo]
		PTipo.append(tipoDic)
		resultado.append(iContadorTemporal)
		arregloCuadruplos.append(cuadruplo("=",funcionActiva,"nul",iContadorTemporal))
		iContadorTemporal += 1
		iContadorCuadruplos += 1

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_parametros(p):
  '''
  functionUsuario_parametros : functionUsuario_aux1 functionUsuario_aux2
               				| empty
  '''

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_aux1(p):
  '''
  functionUsuario_aux1 : expresion
  '''
  global iContadorCuadruplos
  global arregloCuadruplos
  global PilaO
  global resultado
  global iContadorParametros
  operando1 = PilaO.pop()
  resultado.append(iContadorParametros + 1)
  arregloCuadruplos.append(cuadruplo("param",operando1,"nul",iContadorParametros + 1))
  iContadorCuadruplos+=1
  iContadorParametros+=1

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
  global iContadorCuadruplos
  global arregloCuadruplos
  global resultado
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("era","checkwall","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","checkwall","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  print("Encontré un checkwall\n")

#función de sintaxis que revisa si se recive la función predeinida de move();
def p_move(p):
  '''
  move : MOVE imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  global iContadorCuadruplos
  global arregloCuadruplos
  global resultado
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("era","move","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","move","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  print("Encontré un move\n")

#función de sintaxis que revisa si se recive la función predeinida de turnRight();
def p_turnright(p):
  '''
  turnright : TURN_RIGHT imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  global iContadorCuadruplos
  global arregloCuadruplos
  global resultado
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("era","turnRight","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","turnRight","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  print("Encontré un turnright\n")

#función de sintaxis que revisa si se recive la función predeinida de turnLeft();
def p_turnleft(p):
  '''
  turnleft : TURN_LEFT imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  global iContadorCuadruplos
  global arregloCuadruplos
  global resultado
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("era","turnLeft","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","turnLeft","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  print("Encontré un turnleft\n")

#función de sintaxis que revisa si se recive la función predeinida de pickBeeper();
def p_pickbeeper(p):
  '''
  pickbeeper : PICK_BEEPER imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''

  global iContadorCuadruplos
  global arregloCuadruplos
  global resultado
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("era","pickBeeper","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","pickBeeper","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  print("Encontré un pickbeeper\n")

#función de sintaxis que revisa si se recive la función predeinida de putBeeper();
def p_putbeeper(p):
  '''
  putbeeper : PUT_BEEPER imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  global iContadorCuadruplos
  global arregloCuadruplos
  global resultado
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("era","putBeeper","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","putBeeper","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
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
  #prende el contador de locales e inicia el de locales
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
  #cuando entra al while prende el boleano de ciclo
  global bCiclo
  global PSaltos
  global iContadorCuadruplos
  bCiclo = 1
  PSaltos.append(iContadorCuadruplos)
  print(p[1])

def p_imprimeEndWhile(p):
  '''
  imprimeEndWhile : END_WHILE
  '''
  global PSaltos
  global arregloCuadruplos
  global iContadorCuadruplos
  global bCiclo
  global operador
  global resultado
  
  #saca el tope de Psaltos , que es el apuntador al "gotof"
  res = PSaltos.pop()
  #al cuadruplo ubicado en la posición res le mete contador temporal + 1 porque apunta a la siguiente direccion
  arregloCuadruplos[res].setResultado(iContadorCuadruplos + 1)
  #saca el apuntador al inicio del while 
  auxresultado = PSaltos.pop()
  operador = "Goto"
  #almacena el resultado en el arreglo de resultados para no perder la cuenta
  resultado.append(auxresultado)
  #genera el cuadruplo
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul",auxresultado))
  #sigye la cuenta del contador y resetea la variable boleana
  bCiclo = 0
  iContadorCuadruplos += 1
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

def p_imprimeEndElse(p):
  '''
  imprimeEndElse : END_ELSE
  '''
  global PSaltosAux
  global iContadorCuadruplos
  global arregloCuadruplos
  if(p[1] != "else"):
    while(len(PSaltosAux)>0):
      res = PSaltosAux.pop()
      arregloCuadruplos[res].setResultado(iContadorCuadruplos + 1)
  print(p[1])

def p_imprimeEndElif(p):
  '''
  imprimeEndElif : END_ELIF
  '''
  global PSaltos
  global PSaltosAux
  global arregloCuadruplos
  global iContadorCuadruplos
  global operador
  global resultado
  global bIf

  #saca el tope de Psaltos , que es el apuntador al "gotof"
  res = PSaltos.pop()
  #al cuadruplo ubicado en la posición res le mete contador temporal + 1 porque apunta a la siguiente direccion
  arregloCuadruplos[res].setResultado(iContadorCuadruplos + 1)
  
  PSaltosAux.append(iContadorCuadruplos)
  operador = "Goto"
  #almacena el resultado en el arreglo de resultados para no perder la cuenta
  resultado.append(-2)
  #genera el cuadruplo
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul",resultado[iContadorCuadruplos]))
  #sigye la cuenta del contador y resetea la variable boleana
  iContadorCuadruplos+=1
  bIf = 0
  print(p[1])

def p_imprimeIf(p):
  '''
  imprimeIf : IF
  '''
  global bIf
  bIf = 1
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
  global PSaltos
  global PSaltosAux
  global arregloCuadruplos
  global iContadorCuadruplos
  global operador
  global resultado
  global bIf

  #saca el tope de Psaltos , que es el apuntador al "gotof"
  res = PSaltos.pop()
  #al cuadruplo ubicado en la posición res le mete contador temporal + 1 porque apunta a la siguiente direccion
  arregloCuadruplos[res].setResultado(iContadorCuadruplos + 1)
  
  PSaltosAux.append(iContadorCuadruplos)
  operador = "Goto"
  #almacena el resultado en el arreglo de resultados para no perder la cuenta
  resultado.append(-2)
  #genera el cuadruplo
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul",resultado[iContadorCuadruplos]))
  #sigye la cuenta del contador y resetea la variable boleana
  iContadorCuadruplos+=1
  bIf = 0
  print(p[1])

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
for x in range(0,iContadorCuadruplos + 1):
	print("Cuadruplo num " + str(x))
	print(arregloCuadruplos[x].getOperador())
	print(arregloCuadruplos[x].getOperando1())
	print(arregloCuadruplos[x].getOperando2())
	print(arregloCuadruplos[x].getResultado())