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
iContadorDiccionarioVar = 0
iContadorDiccionarioFuncion = 0
iContadorInicioLocal = 0
iContadorTemporal = 0
iContadorCuadruplos = 0
iContadorParametros = 0
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
resultado = []
PilaO = []
POper = []
PSaltos = []
PSaltosAux = []
PTipo = []
arregloCuadruplos = []
listaParamFuncion = []
listaAuxParamFuncion = []

#diccionarios
dV = {}
dF = {}

#apuntadores a memoria
vgi = 5000
vgf = 6000
vgs = 7000
vgb = 8000
vli= 10000
vlf = 11000
vlb = 12000
vls = 13000
tgi = 20000
tgf = 21000
tgs = 22000
tgb = 23000
ctei = 30000
ctef = 31000
ctes = 32000
cteb = 33000

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

dicOperadores = {"+" : 0, "-" : 1, "*" : 2, "/" : 3, "<" : 4, ">": 5, "=" : 6,"<>" : 7, "==" : 8, "&": 9, "|": 10, "print" : 11}

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
  'CTE_BOOL',
  'TRUE',
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

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################



#seccion 1 del codigo
#######################################################################################################

start = "estatuto"

def p_empty(p):
    'empty :'
    pass

#estructura general de a+
#puede comenzar o no comenzar por la declaración de variables globales
#es seguido por la declaración opcional de funciones de usuario
#en la tercera parte es el programa principal que es identificado por la palabra MAIN y es seguido de una serie de estatutos
def p_estatuto(p):
    '''
    estatuto : start declaracion_3 function_declaration matchMain DOS_PUNTOS estatuto_2
    '''

#funcion auxiliar de estatuto
#sirve para generar el cuadruplo goto : main
def p_start(p):
	'''
	start : empty
	'''
	global PSaltos
	global iContadorCuadruplos
	global arregloCuadruplos , resultado
	#mete a la pila de saltos el cuadruplo inicial para poder llenar despúes el cuadruplo donde se encuentre main
	PSaltos.append(iContadorCuadruplos)
	#agrega -2 a resultados para no perder la cuenta
	resultado.append(-2)
	#genera el cuadruplo y lo agrega al arreglo de cuádruplos
	arregloCuadruplos.append(cuadruplo("GotoMain",-2,"nul","nul"))
	#contador de cuadruplos
	iContadorCuadruplos+=1

#funcion auxiliar de estatuto
#encuentra main
#llena el cuadruplo gotomain
def p_matchMain(p):
	'''
	matchMain : MAIN
	'''
	global PSaltos
	global arregloCuadruplos
	global iContadorCuadruplos

	#saca el tope de Psaltos , que es el apuntador al "gotof"
	res = PSaltos.pop()
	#al cuadruplo ubicado en la posición res le mete contador temporal + 1 porque apunta a la siguiente direccion
	arregloCuadruplos[res].setOperando1(iContadorCuadruplos)

#funcion auxiliar de estatuto sirve para la declaracion de 0 a n funciones
def p_function_declaration(p):
	'''
	function_declaration : function destroyVars function_declaration
						| empty
	'''

#estatuto se compone de 0 a n opciones
def p_estatuto_2(p):
  '''
  estatuto_2 : opciones estatuto_2
            | empty
  '''

#toda la serie de posibles estatutos
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

###################################################################################################

#seccion 2 de codigo
###################################################################################################

#funcion para declarar de 0 a n veces variables
def p_declaracion_3(p):
  '''
  declaracion_3 : declaracion declaracion_3
                | empty
  '''

#funcion para declarar variables
def p_declaracion(p):
  '''
  declaracion : tipo ID declaracion_aux imprimePuntoYComa
  '''
  global bscope
  global iContadorDiccionarioVar
  global dV
  global tipoDeclaracion
  global vgi, vli, vgf, vlf, vgs, vls
  #vars locales
  obj = ""
  objAux = ""
  var = 0

  #si no es la primera variable a guardar checa si no se repite el nombre
  if(iContadorDiccionarioVar != 0):
    for x in range(0,iContadorDiccionarioVar):
      objAux = dV[x]
      #compara los nombres
      if(p[2] == objAux.getNombre()):
        raise errorSemantico("Variable ya definida: " + p[2])


  #checa el tipo de variable y su scope y guarda esa direccion de memoria en var
  if(tipoDeclaracion == "int" and bscope == 0):
    var = vgi
    vgi += 1
  elif(tipoDeclaracion == "int" and bscope == 1):
    var = vli
    vli+=1
  elif(tipoDeclaracion == "float" and bscope == 0):
    var = vgf
    vgf+=1
  elif(tipoDeclaracion == "float" and bscope == 1):
    var = vgf
    vlf+=1
  elif(tipoDeclaracion == "string" and bscope == 0):
    var = vgs
    vgs+=1
  elif(tipoDeclaracion == "string" and bscope == 1):
    var = vls
    vls+=1

  #crea el objeto tablaVar con : nombre, tipo, scope, direccion
  if(bscope == 0):
    obj = tablaVar(p[2],tipoDeclaracion,'global',var)
  else:
    obj = tablaVar(p[2],tipoDeclaracion,'local',var)

  #en caso de agregarla la guarda en el diccionario
  if(iContadorDiccionarioVar == 0):
  	dV = {iContadorDiccionarioVar : obj}
  else:
  	dV[iContadorDiccionarioVar] = obj

  #incrementa contador
  iContadorDiccionarioVar = iContadorDiccionarioVar + 1

#esta funcion ayuda en caso de que se quieran declarar variables variables del mismo tipo en el mismo renglon
def p_declaracion_aux(p):
  '''
  declaracion_aux : declaracion_2
          | empty
  '''

#coma id <<a>>
def p_declaracion_2(p):
  '''
  declaracion_2 : imprimeComa ID a
  '''
  global bscope
  global iContadorDiccionarioVar
  global dV
  global tipoDeclaracion
  global vgi, vli, vgf, vlf, vgs, vls
  #vars locales
  obj = ""
  objAux = ""
  var = 0

  #checa que no exista
  for x in range(0,iContadorDiccionarioVar):
    objAux = dV[x]
    #compara los nombres
    if(p[2] == objAux.getNombre()):
      raise errorSemantico("Variable ya definida: " + p[2])

  #checa el tipo de variable y su scope y guarda esa direccion de memoria en var
  if(tipoDeclaracion == "int" and bscope == 0):
    var = vgi
    vgi += 1
  elif(tipoDeclaracion == "int" and bscope == 1):
    var = vli
    vli+=1
  elif(tipoDeclaracion == "float" and bscope == 0):
    var = vgf
    vgf+=1
  elif(tipoDeclaracion == "float" and bscope == 1):
    var = vgf
    vlf+=1
  elif(tipoDeclaracion == "string" and bscope == 0):
    var = vgs
    vgs+=1
  elif(tipoDeclaracion == "string" and bscope == 1):
    var = vls
    vls+=1

  #crea el objeto tablaVar con : nombre, tipo, scope, direccion
  if(bscope == 0):
    obj = tablaVar(p[2],tipoDeclaracion,'global',var)
  else:
    obj = tablaVar(p[2],tipoDeclaracion,'local',var)

   #lo agrega al diccionario
  dV[iContadorDiccionarioVar] = obj
  #incrementa el contador
  iContadorDiccionarioVar = iContadorDiccionarioVar + 1

#funcion auxiliar recursiva que ayuda a seguir declrando variables dentro del mismo renglon
def p_a(p):
  '''
  a : declaracion_2
   | empty
  '''

#define los distintos tipos de variables pueden ser int, float, string y bool
def p_tipo(p):
  '''
  tipo : INT
       | FLOAT
       | STRING
       | BOOL
  '''
  global tipoDeclaracion
  #guarda el tipo en tipo de declaracion
  #ayuda a que no se revuelva el tipo de dato por el lalr de las funciones
  tipoDeclaracion = p[1]

###################################################################################################

#seccion 3 de codigo
###################################################################################################

#funcion que asigna a un id algo
def p_asignacion(p):
  '''
  asignacion : matchID EQUIVALE asignacion_aux
  '''
  global arregloCuadruplos
  global PilaO, PTipo
  global resultado
  global iContadorTemporal, iContadorCuadruplos, iContadorDiccionarioVar
  varAux = 0;

  #saca el tipo de datos de los operandos que esten en la pila de tipos
  op2 = PTipo.pop()
  op1 = PTipo.pop()
  #convierte = a numero
  op = dicOperadores["="]
  #calcula el tipo con el cubo de datos
  tipo = cubo[op1][op2][op]
  #si el tipo es -1 (error)--> erros semantico
  if(tipo == -1):
  	raise errorSemantico("Uso incorrecto de tipos ")
  else:
    #saca operador y operandos de la pila para hacer el cuadruplo
    operador = "="
    operando2 = PilaO.pop()
    operando1 = PilaO.pop()
    #mete el nuevo tipo a la pila de tipos
    PTipo.append(tipo)
    resultado.append(operando1)
    arregloCuadruplos.append(cuadruplo(operador,operando2,"nul",resultado[iContadorCuadruplos]))
    PilaO.append(resultado[iContadorCuadruplos])
    iContadorCuadruplos += 1

#funcion auxiliar que decide si asignar una expresion aritmetica o bien una fincion de usuario 
def p_asignacion_aux(p):
	'''
	asignacion_aux : expresion imprimePuntoYComa
					| funcionUsuario
	'''

#funcion para hacer expresiones booleanas 
def p_exp(p):
  '''
  exp : expresion exp_2
  '''

#expresion boleana 
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
  global arregloCuadruplos
  global tipo
  global resultado
  global iContadorTemporal, iContadorDiccionarioVar, iContadorCuadruplos
  global dicOperadores
  global PTipo,PilaO
  global tgb
  
  #checa el tipo de dato
  op2 = PTipo.pop()
  op1 = PTipo.pop()
  op = dicOperadores[p[1]]
  tipo = cubo[op1][op2][op]
  if(tipo != 3):
    raise errorSemantico("uso incorrecto de tipos ")
  else:
  	## cuadruplos de condicion
  	# toma el operador 1 y los operandos
  	operador = p[1]
  	operando2 = PilaO.pop()
  	operando1 = PilaO.pop()
  	#incrementa el contador y lo agrega al arreglo de resultados
  	iContadorTemporal += 1
  	resultado.append(iContadorTemporal)
  	#genera el cuadruplo
  	tgb+=1
  	arregloCuadruplos.append(cuadruplo(operador,operando2,operando1,resultado[iContadorCuadruplos]))
  	#el temporal lo mete a la pila
  	PilaO.append(iContadorTemporal)
  	#suma uno al contador
  	iContadorCuadruplos += 1

#para hacer sumas
def p_expresion(p):
  '''
  expresion : termino cuaTermino expresion_2
  '''

#funcion que hace las operaciones de cuadruplos desúes del "termino"
def p_cuaTermino(p):
  '''
  cuaTermino : empty
  '''
  global POper, PilaO, PTipo
  global tgi, tgf
  global dicOperadores
  global resultado
  global iContadorTemporal, iContadorCuadruplos

  #si la lisra tiene más de 1 elemento
  if(len(POper) > 0):
    # y su top es + o - 
    if(POper[-1] == "+" or POper[-1] == "-"):
      #checa que los tipos sean validos con la operacion
      op2 = PTipo.pop()
      op1 = PTipo.pop()
      if (POper[-1] == "+"):
      	op = dicOperadores["+"]
      else:
      	op = dicOperadores["-"]
      #checa el tipo
      tipo = cubo[op1][op2][op]
      #si es invalido erroe semantico
      if(tipo == -1):
      	raise errorSemantico("uso incorrecto de tipos ")
      else:
      	#hace cuadruplo
      	#saca d epila
      	operador = POper.pop()
      	operando2 = PilaO.pop()
      	operando1 = PilaO.pop()
      	iContadorTemporal += 1
      	if(tipo == 0):
      		tgi+=1
      	elif(tipo == 1):
      		tgf+=2
      	#agrega a la pila
      	PTipo.append(tipo)
      	resultado.append(iContadorTemporal)
      	#agrega al cuadruplo
      	arregloCuadruplos.append(cuadruplo(operador,operando1,operando2,iContadorTemporal))
      	PilaO.append(iContadorTemporal)
      	#incrementa el contador de cuadruplos
      	iContadorCuadruplos += 1

#funcion que reconoce suma o resta
def p_expresion_2(p):
  '''
  expresion_2 : matchSuma expresion
              | matchResta expresion
              | empty
  '''

#funcion que mete el "+" adentro de la pila de operadores
def p_matchSuma(p):
  '''
  matchSuma : SUMA
  '''
  global POper
  POper.append(p[1])

#función que mete el "-" adentro de la pila de operadores
def p_matchResta(p):
  '''
  matchResta : RESTA
  '''
  global POper
  POper.append(p[1])

#expresion que me deja multiplicar y dividir
def p_termino(p):
  '''
  termino : factor cuaFactor termino_2
  '''

#funcion para cuadruplo de factor
def p_cuaFactor(p):
  '''
  cuaFactor : empty
  '''
  #generacion de cuadruplos
  global POper, PilaO, PTipo
  global tgi, tgf
  global resultado
  global dicOperadores
  global iContadorTemporal, iContadorCuadruplos
  #entra si ya entro una multiplicacion o division a la pila o suma o resta
  if(len(POper) > 0):
  	#pregunta si el tope es multiplicacion o division en caso de serlo prosigue
    if(POper[-1] == "*" or POper[-1] == "/"):
      op2 = PTipo.pop()
      op1 = PTipo.pop()

      if(POper[-1] == "*"):
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
      	#saca el operador y ambos operandos
      	operador = POper.pop()
      	operando2 = PilaO.pop()
      	operando1 = PilaO.pop()
      	iContadorTemporal += 1
      	PTipo.append(tipo)
      	#al arreglo de resultados mete el numero de temporal
      	resultado.append(iContadorTemporal)
      	#genera un nuevo cuadruplo
      	arregloCuadruplos.append(cuadruplo(operador,operando1,operando2,resultado[iContadorCuadruplos]))
      	#mete el temporal
      	PilaO.append(iContadorTemporal)
      	iContadorCuadruplos += 1

#hace match de multiplicacion o division
def p_termino_2(p):
  '''
  termino_2 : MatchMultiplicacion termino
            | MatchDivision termino
            | empty
  '''

#mete la multiplicacion a la pila
def p_MatchMultiplicacion(p):
  '''
  MatchMultiplicacion : MULTIPLICACION
  '''
  #si llega una multiplicacion la mete dentro de la pila de operadores
  global POper
  POper.append(p[1])

#mete la division a la pila
def p_MatchDivision(p):
  '''
  MatchDivision : DIVISION
  '''
  #si llega una division la mete en la pila de operadores
  global POper
  POper.append(p[1])

#deja meter un id o una expresion en parentesis
def p_factor(p):
  '''
  factor : cuaFondoFalsoPI expresion cuaFondoFalsoPD
         | var_cte
  '''

#funcion que crea fondo falso cuando llega el parentesis
def p_cuaFondoFalsoPI(p):
  '''
  cuaFondoFalsoPI : PARENTESIS_IZQ
  '''
  global POper
  POper.append(p[1])

#funcion que saca el fondo flaso cuando se cierra el parentesis
def p_cuaFondoFalsoPD(p):
  '''
  cuaFondoFalsoPD : PARENTESIS_DER
  '''
  global POper
  POper.pop()

#match de id , enteros o flotantes
def p_var_cte(p):
  '''
  var_cte : matchID
          | matchCteInt
          | matchCteFloat
          | matchCteBool
  '''

#match de id checa que exista y guarda el tipo en la pila de tipo
def p_matchID(p):
  '''
  matchID : ID
  '''
  global dV, dicTipos
  global iContadorDiccionarioVar
  global PilaO, PTipo
  varAux = 0
  tipo = ""
  auxTipo = -2
  #Checa si variable esta o no declarada
  for x in range(0,iContadorDiccionarioVar):
  	if(p[1] != dV[x].getNombre()):
  		varAux += 1
  	else:
  		#cubo semantico tipo de dato correcto
  		tipo = dV[x].getTipo()
  		auxTipo = dicTipos[tipo]
  		PTipo.append(auxTipo)
  		#Meter a pila operadores paso 1 del algoritmo
  		PilaO.append(p[1])
  #No esta declarada
  if(varAux == iContadorDiccionarioVar):
    raise errorSemantico("Variable no declarada: " + p[1])

  print(p[1])

#match una constante numerica entera
def p_matchCteInt(p):
  '''
  matchCteInt : CTE_INT
  '''
  global PilaO, PTipo
  global dicTipos
  global ctei
  auxTipo = -2

  auxTipo = dicTipos["int"]
  PTipo.append(auxTipo)

  #meter a pila de operadores
  PilaO.append(p[1])
  ctei+=1

#match una constante numerica flotante
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

#hace matech a una constante boleana con true o false
def p_matchCteBool(p):
  '''
  matchCteBool : TRUE
  				| FALSE
  '''
  global cteb
  global dicTipos,PTipo,PilaO
  auxTipo = dicTipos["bool"]
  PTipo.append(auxTipo)
  #mete la constante a la pila de operandos
  PilaO.append(p[1])
  cteb+=1

###################################################################################################

#seccion 4 de codigo
###################################################################################################

#funcion para aceptar condiciones s
def p_condicion(p):
  '''
  condicion : imprimeIf imprimeParentesisIzq condicion_2 imprimeParentesisDer imprimeDosPuntos cuacondicion1 estatuto_2 imprimeEndIf condicion_3 condicion_4
  '''

#genera el cuadruplo de condicion
def p_cuacondicion1(p):
  '''
  cuacondicion1 : empty
  '''
  global operador, operando1, operando2, resultado
  global iContadorCuadruplos
  global PSaltos, PilaO
  global arregloCuadruplos
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

#la condicion puede checar una expresion o un checkwall
def p_condicion_2(p):
  '''
  condicion_2 : exp 
            | checkwall
  '''

#condicion permite un elif
def p_condicion_3(p):
  '''
  condicion_3 : ELIF imprimeParentesisIzq condicion_2 imprimeParentesisDer imprimeDosPuntos cuacondicion1 estatuto_2 imprimeEndElif condicion_3
              | empty
  '''

#permite un else
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

###################################################################################################

#seccion 5 de codigo
###################################################################################################

#genera el cuadruplo para imprimir
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

#hace match de un string o bien de una expresion
def p_escritura_2(p):
  '''
  escritura_2 : matchCteString
              | expresion
  '''

#imprime string
def p_matchCteString(p):
	'''
	matchCteString : CTE_STRING
	'''
	global ctes
	global dicTipos,PTipo,PilaO
	auxTipo = dicTipos["string"]
	PTipo.append(auxTipo)
	#mete la constante a la pila de operandos
	PilaO.append(p[1])
	ctes+=1

###################################################################################################

#seccion 6 de codigo
###################################################################################################

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


###################################################################################################

#seccion 7 de codigo
###################################################################################################
#funciones
def p_function(p):
  '''
  function : imprimeDef tipoFunction matchIDFunction imprimeParentesisIzq function_aux imprimeParentesisDer imprimeDosPuntos estatuto_2 function_4 imprimeEndDef
  '''
  global bscope
  global listaParamFuncion
  global iContadorDiccionarioFuncion, iContadorDiccionarioVar
  global dF,dV
  global tipoDeclaracionFuncion
  global vgi, vli, vgf, vlf, vgs, vls

  for x in range(0,iContadorDiccionarioFuncion):
    varFunc = dF[x]
    if(p[1] == varFunc.getNombre()):
      raise errorSemantico("Función previamente definida: " + p[1])

  listaAux = []
  listaAux.extend(listaParamFuncion)
  varAux = tablaFunciones(p[1],tipoDeclaracionFuncion,listaAux, -2)

  if(iContadorDiccionarioFuncion == 0):
    dF = {iContadorDiccionarioFuncion : varAux}
  else:
    dF[iContadorDiccionarioFuncion] = varAux
    
  iContadorDiccionarioFuncion = iContadorDiccionarioFuncion + 1
  print(dF)
  bscope = 0


def p_matchIDFunction(p):
  '''
  matchIDFunction : ID
  '''
  global bscope
  global listaParamFuncion
  global iContadorDiccionarioFuncion, iContadorDiccionarioVar
  global dF,dV
  global tipoDeclaracionFuncion
  global vgi, vli, vgf, vlf, vgs, vls

  for x in range(0,iContadorDiccionarioFuncion):
    varFunc = dF[x]
    if(p[1] == varFunc.getNombre()):
      raise errorSemantico("Función previamente definida: " + p[1])

  listaAux = []
  listaAux.extend(listaParamFuncion)
  varAux = tablaFunciones(p[1],tipoDeclaracionFuncion,listaAux, -2)

  if(iContadorDiccionarioFuncion == 0):
    dF = {iContadorDiccionarioFuncion : varAux}
  else:
    dF[iContadorDiccionarioFuncion] = varAux
    
  iContadorDiccionarioFuncion = iContadorDiccionarioFuncion + 1
  print(dF)
  bscope = 0
  #si no es void crea una variable global coon el mismo nombre
  if(tipoDeclaracionFuncion != "void"): 
    #vars locales
    obj = ""
    objAux = ""
    var = 0
    #checa que no exista
    for x in range(0,iContadorDiccionarioVar):
      #compara los nombre
      if(p[1] == dV[x].getNombre()):
        raise errorSemantico("Variable ya definida: " + p[1])

    #checa el tipo de variable y su scope y guarda esa direccion de memoria en var
    if(tipoDeclaracionFuncion == "int"):
      var = vgi
      vgi += 1
    elif(tipoDeclaracionFuncion == "float"):
      var = vgf
      vgf+=1
    elif(tipoDeclaracionFuncion == "string"):
      var = vgs
      vgs+=1

    #crea el objeto tablaVar con : nombre, tipo, scope, direccion
    obj = tablaVar(p[1],tipoDeclaracionFuncion,"global",var)
     #lo agrega al diccionario
    dV[iContadorDiccionarioVar] = obj
    #incrementa el contador
    iContadorDiccionarioVar = iContadorDiccionarioVar + 1

def p_tipoFunction(p):
  '''
  tipoFunction : INT
       		   | FLOAT
       		   | STRING
       		   | BOOL
       		   | VOID
  '''
  global tipoDeclaracionFuncion
  global bRetorna
  tipoDeclaracionFuncion = p[1]
  if(p[1] != "void"):
  	bRetorna = 1

def p_function_aux(p):
  '''
  function_aux : function_2
               | empty
  '''

def p_function_2(p):
  '''
  function_2 : tipo ID function_3
  '''
  global bscope
  global iContadorDiccionarioVar
  global dV
  global tipoDeclaracion
  global vli, vlf, vls
  #vars locales
  obj = ""
  objAux = ""
  var = 0

  #si no es la primera variable a guardar checa si no se repite el nombre
  if(iContadorDiccionarioVar != 0):
    for x in range(0,iContadorDiccionarioVar):
      objAux = dV[x]
      #compara los nombres
      if(p[2] == objAux.getNombre()):
        raise errorSemantico("Variable ya definida: " + p[2])


  #checa el tipo de variable y su scope y guarda esa direccion de memoria en var
  if(tipoDeclaracion == "int"):
    var = vli
    vli+=1
  elif(tipoDeclaracion == "float"):
    var = vgf
    vlf+=1
  elif(tipoDeclaracion == "string"):
    var = vls
    vls+=1

  obj = tablaVar(p[2],tipoDeclaracion,'local',var)
  aux = dicTipos[tipoDeclaracion]
  listaParamFuncion.append(aux)

  #en caso de agregarla la guarda en el diccionario
  if(iContadorDiccionarioVar == 0):
  	dV = {iContadorDiccionarioVar : obj}
  else:
  	dV[iContadorDiccionarioVar] = obj

  #incrementa contador
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
  global arregloCuadruplos, listaParamFuncion
  global dV
  global iContadorInicioLocal, iContadorDiccionarioVar, iContadorTemporal, iContadorCuadruplos
  global resultado
  global vli,vlf,vls,vlb,tgi,tgf,tgs,tgb
  global bRetorna

  iAux = 0
  iAux = iContadorInicioLocal
  for x in range(iContadorInicioLocal , iContadorDiccionarioVar):
    if(dV[x].getScope() == "local"):
      del dV[x]

  if(bRetorna == 1):
    iContadorDiccionarioVar = iAux + 1
  else:
    iContadorDiccionarioVar = iAux

  iContadorTemporal = iContadorDiccionarioVar - iContadorInicioLocal
  del listaParamFuncion[:]

  vli= 10000
  vlf = 11000
  vlb = 12000
  vls = 13000
  tgi -= iContadorTemporal
  tgf -= iContadorTemporal
  tgs -= iContadorInicioLocal
  tgb -= iContadorInicioLocal
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("ret","nul","nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  bRetorna = 0

###################################################################################################

#seccion 8 de codigo
###################################################################################################

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
	global dF
	global iContadorDiccionarioFuncion
	global funcionActiva
	varAux = 0
	auxTipo = ""
	for x in range(0,iContadorDiccionarioFuncion):
		if(p[1] != dF[x].getNombre()):
			varAux += 1
		if(varAux == iContadorDiccionarioFuncion):
			raise errorSemantico("Funcion no definida: " + p[1])
		else:
			funcionActiva = p[1]
			auxTipo = dF[x].getTipo()
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
	global arregloCuadruplos, dF
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
	for x in range(0,iContadorDiccionarioFuncion):
		if(dF[x].getNombre() == funcionActiva):
			tipo = dF[x].getTipo();
	if(tipo != "void"):
		tipoDic = dicTipos[tipo]
		PTipo.append(tipoDic)
		resultado.append(iContadorTemporal)
		arregloCuadruplos.append(cuadruplo("=",funcionActiva,"nul",resultado[iContadorCuadruplos]))
		iContadorTemporal += 1
		iContadorCuadruplos += 1

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_parametros(p):
  '''
  functionUsuario_parametros : functionUsuario_aux1 functionValidaParams
               				| empty
  '''

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_aux1(p):
  '''
  functionUsuario_aux1 : expresion functionUsuario_aux2
  '''
  global iContadorCuadruplos
  global arregloCuadruplos
  global PilaO, PTipo
  global resultado
  global iContadorParametros
  global funcionActiva
  global tipo

  tipo = PTipo.pop()
  listaAuxParamFuncion.append(tipo)
  operando1 = PilaO.pop()
  resultado.append(iContadorParametros + 1)
  arregloCuadruplos.append(cuadruplo("param",operando1,"nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  iContadorParametros+=1

#funcion auxiliar de p_funcionUsuario
def p_functionUsuario_aux2(p):
  '''
  functionUsuario_aux2 : COMA functionUsuario_aux1
            			| empty
  '''

def p_functionValidaParams(p):
	'''
	functionValidaParams : empty
	'''
	global dF,listaAuxParamFuncion
	global funcionActiva, iContadorDiccionarioFuncion
	listaAux = []
	for x in range(0,iContadorDiccionarioFuncion):
		objAux = dF[x]
		if(objAux.getNombre() == funcionActiva):
			listaAux.extend(objAux.getParametros())

	if(len(listaAuxParamFuncion) == len(listaAux)):
		for x in range (0, len(listaAux)):
			if(listaAuxParamFuncion[x] != listaAux[x]):
				raise errorSemantico("Tipo de Parametros no concuerda con los parametros de la funcion")
	else:
		raise errorSemantico("La cantidad de parametros no concuerda con los parametros de la funcion")

###################################################################################################

#seccion 9 de codigo
###################################################################################################
#función de sintaxis que revisa si se recive la función predeinida de checkWall();
def p_checkwall(p):
  '''
  checkwall : CHECKWALL imprimeParentesisIzq imprimeParentesisDer imprimePuntoYComa
  '''
  global iContadorCuadruplos
  global arregloCuadruplos
  global resultado
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("era","checkwall","nul",-2))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","checkwall","nul",-2))
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
  arregloCuadruplos.append(cuadruplo("era","move","nul",-2))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","move","nul",-2))
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
  arregloCuadruplos.append(cuadruplo("era","turnRight","nul",-2))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","turnRight","nul",-2))
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
  arregloCuadruplos.append(cuadruplo("era","turnLeft","nul",-2))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","turnLeft","nul",-2))
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
  arregloCuadruplos.append(cuadruplo("era","pickBeeper","nul",-2))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","pickBeeper","nul",-2))
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
  arregloCuadruplos.append(cuadruplo("era","putBeeper","nul",-2))
  iContadorCuadruplos+=1
  resultado.append(-2)
  arregloCuadruplos.append(cuadruplo("gosub","putBeeper","nul",-2))
  iContadorCuadruplos+=1
  print("Encontré un putbeeper")

#########################################################################################################################################################################
########################################################################################################################################################################
#########################################################################################################################################################################

def p_imprimeReturn(p):
  '''
  imprimeReturn : RETURN
  '''

def p_imprimeDef(p):
  '''
  imprimeDef : DEF
  '''
  global bscope
  global iContadorInicioLocal
  #prende el contador de locales e inicia el de locales
  bscope = 1
  iContadorInicioLocal = iContadorDiccionarioVar

def p_imprimeEndDef(p):
  '''
  imprimeEndDef : END_DEF
  '''

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
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul",resultado[iContadorCuadruplos]))
  #sigye la cuenta del contador y resetea la variable boleana
  bCiclo = 0
  iContadorCuadruplos += 1

def p_imprimePrint(p):
  '''
  imprimePrint : PRINT
  '''

def p_imprimeParentesisIzq(p):
  '''
  imprimeParentesisIzq : PARENTESIS_IZQ
  '''

def p_imprimeParentesisDer(p):
  '''
  imprimeParentesisDer : PARENTESIS_DER
  '''

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
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul",-2))
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

def p_imprimeDosPuntos(p):
  '''
  imprimeDosPuntos : DOS_PUNTOS
  '''

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
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul",-2))
  #sigye la cuenta del contador y resetea la variable boleana
  iContadorCuadruplos+=1
  bIf = 0


def p_imprimePuntoYComa(p):
  '''
  imprimePuntoYComa : PUNTO_Y_COMA
  '''

def p_imprimeComa(p):
  '''
  imprimeComa : COMA
  '''

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

print("\n")

for x in range(0,iContadorDiccionarioVar):
  print("variable numero " + str(x))
  print(dV[x].getNombre())
  print(dV[x].getTipo())
  print(dV[x].getDireccion())
  print("--------------------")

print("\n")

for x in range(0,iContadorCuadruplos):
	print("Cuadruplo num " + str(x))
	print(arregloCuadruplos[x].getOperador())
	print(arregloCuadruplos[x].getOperando1())
	print(arregloCuadruplos[x].getOperando2())
	print(arregloCuadruplos[x].getResultado())