#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Adriana Valenzuela a01195331
#Mayra Ruiz a00812918

from tablaVar import tablaVar
from tablaFunciones import tablaFunciones
from tablaConstantes import tablaConstantes
from errorSintactico import errorSintactico
from errorLexico import errorLexico
from errorSemantico import errorSemantico
from cuadruplo import cuadruplo
import ply.lex as lex
import ply.yacc as yacc
import sys
from sys import argv

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
numConstantes = 0
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
nombreIDArr = ""
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
arregloConstantes = []

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

cubo = [[[0 for k in range(13)] for j in range(4)] for i in range(4)]
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

cubo[0][0][11] = 3     # int <= int = bool
cubo[0][1][11] = 3     # int <= float = bool
cubo[0][2][11] = -1    # int <= string = error
cubo[0][3][11] = -1    # int <= bool = error

cubo[0][0][12] = 3     # int >= int = bool
cubo[0][1][12] = 3     # int >= float = bool
cubo[0][2][12] = -1    # int >= string = error
cubo[0][3][12] = -1    # int >= bool = error

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

cubo[1][0][11] = 3     # float <= int = bool
cubo[1][1][11] = 3     # float <= float = bool
cubo[1][2][11] = -1    # float <= string = error
cubo[1][3][11] = -1    # float <= bool = error

cubo[1][0][12] = 3     # float >= int = bool
cubo[1][1][12] = 3     # float >= float = bool
cubo[1][2][12] = -1    # float >= string = error
cubo[1][3][12] = -1    # float >= bool = error

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
cubo[2][2][4] = -1     # string < string = bool
cubo[2][3][4] = -1    # string < bool = error

cubo[2][0][5] = -1    # string > int = error
cubo[2][1][5] = -1    # string > float = error
cubo[2][2][5] = -1     # string > string = bool
cubo[2][3][5] = -1    # string > bool = error

# ERROR
cubo[2][0][6] = -1    # string = int = error
cubo[2][1][6] = -1    # string = float = error
cubo[2][2][6] = 2    # string = string = string (asignas!)
cubo[2][3][6] = -1    # string = bool = error

cubo[2][0][7] = -1    # string <> int = error
cubo[2][1][7] = -1    # string <> float = error
cubo[2][2][7] = -1     # string <> string = bool
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

cubo[2][0][11] = -1     # string <= int = bool
cubo[2][1][11] = -1    # string <= float = bool
cubo[2][2][11] = -1    # string <= string = error
cubo[2][3][11] = -1    # string <= bool = error

cubo[2][0][12] = -1     # string >= int = bool
cubo[2][1][12] = -1     # string >= float = bool
cubo[2][2][12] = -1    # string >= string = error
cubo[2][3][12] = -1    # string >= bool = error

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
cubo[3][3][7] = -1     # bool <> bool = bool

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
cubo[3][3][10] = 3    	# bool | bool = bool

cubo[3][0][11] = -1     # bool <= int = bool
cubo[3][1][11] = -1    # bool <= float = bool
cubo[3][2][11] = -1    # bool <= string = error
cubo[3][3][11] = -1    # bool <= bool = error

cubo[3][0][12] = -1     # bool >= int = bool
cubo[3][1][12] = -1     # bool >= float = bool
cubo[3][2][12] = -1    # bool >= string = error
cubo[3][3][12] = -1    # bool >= bool = error

dicOperadores = {"+" : 0, "-" : 1, "*" : 2, "/" : 3, "<" : 4, ">": 5, "=" : 6,"<>" : 7, "==" : 8, "&": 9, "|": 10, "<=": 11, ">=": 12, "print" : 13 , "read": 14, "end": 15, "Goto": 16, "GotoF": 17, "Era":18, "Gosub":19, "Param":20, "Ver":21, "Ret":22, "Return":23, "move":24 , "checkwall":25, "turnRight":26, "turnLeft":27, "pickBeeper":28, "putBeeper":29}

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
  'CORCHETE_IZQ',
  'CORCHETE_DER',
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
  'ELSE',
  'END_ELSE',
  'PRINT',
  'READ',
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
t_CORCHETE_IZQ 			= r'\['
t_CORCHETE_DER			= r'\]'


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
  'else'      : 'ELSE',
  'end_else'  : 'END_ELSE',
  'print'     : 'PRINT',
  'read'			: 'READ',
  'def'       : 'DEF',
  'end_def'   : 'END_DEF',
  'main'	: 'MAIN',
  'true'  : 'TRUE',
  'false' : 'FALSE'
}

#er de float se debe poner antes de int por que luego reconoce int . int
def t_CTE_FLOAT(t):
    r'[0-9]+\.[0-9]+'
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
    r'\"([a-zA-Z]|[0-9]|[ \*\[\]\\\^\-\.\?\+\|\(\)\$\/\{\}\%\<\>=&;,_:\[\]\'!$#@])*\"'
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
      raise errorLexico("Error de Lexico: " + t.value[0])
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
    estatuto : start declaracion_3 function_declaration matchMain DOS_PUNTOS estatuto_2 cua_end
    '''

#funcion auxiliar de estatuto
#sirve para generar el cuadruplo goto : main
def p_start(p):
	'''
	start : empty
	'''
	global PSaltos,dicOperadores
	global iContadorCuadruplos
	global arregloCuadruplos , resultado
	#mete a la pila de saltos el cuadruplo inicial para poder llenar despúes el cuadruplo donde se encuentre main
	PSaltos.append(iContadorCuadruplos)
	#agrega -2 a resultados para no perder la cuenta
	resultado.append("nul")
	op = dicOperadores["Goto"]
	#genera el cuadruplo y lo agrega al arreglo de cuádruplos
	arregloCuadruplos.append(cuadruplo(op,-2,"nul","nul"))
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
          | read
          | ciclo
          | turnleft
          | turnright
          | move
          | checkwall
          | pickbeeper
          | putbeeper
          | funcionUsuario
          | returnFunc
  '''

def p_cua_end(p):
  '''
  cua_end : empty
  '''
  global iContadorCuadruplos
  global arregloCuadruplos , resultado, dicOperadores
  #agrega -2 a resultados para no perder la cuenta
  resultado.append("nul")
  op = dicOperadores["end"]
  #genera el cuadruplo y lo agrega al arreglo de cuádruplos
  arregloCuadruplos.append(cuadruplo(op,"nul","nul","nul"))
  #contador de cuadruplos
  iContadorCuadruplos+=1

###################################################################################################

#seccion 2 de codigo
###################################################################################################

#funcion para declarar de 0 a n veces variables
def p_declaracion_3(p):
  '''
  declaracion_3 : declaracion declaracion_3
  							| declaracionArreglo declaracion_3
                | empty
  '''

#funcion para declarar variables
def p_declaracion(p):
  '''
  declaracion : tipo ID declaracion_aux PUNTO_Y_COMA
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
    obj = tablaVar(p[2],tipoDeclaracion,'global',var,1)
  else:
    obj = tablaVar(p[2],tipoDeclaracion,'local',var,1)

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
  declaracion_2 : COMA ID a
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
    obj = tablaVar(p[2],tipoDeclaracion,'global',var,1)
  else:
    obj = tablaVar(p[2],tipoDeclaracion,'local',var,1)

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

def p_declaracionArreglo(p):
	'''
	declaracionArreglo : tipo ID CORCHETE_IZQ CTE_INT CORCHETE_DER PUNTO_Y_COMA
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
		vgi += p[4]
	elif(tipoDeclaracion == "int" and bscope == 1):
		var = vli
		vli+= p[4]
	elif(tipoDeclaracion == "float" and bscope == 0):
		var = vgf
		vgf+= p[4]
	elif(tipoDeclaracion == "float" and bscope == 1):
		var = vgf
		vlf+=p[4]
	elif(tipoDeclaracion == "string" and bscope == 0):
		var = vgs
		vgs+=p[4]
	elif(tipoDeclaracion == "string" and bscope == 1):
		var = vls
		vls+=p[4]

  #crea el objeto tablaVar con : nombre, tipo, scope, direccion
	if(bscope == 0):
		obj = tablaVar(p[2],tipoDeclaracion,'global',var,p[4])
	else:
		obj = tablaVar(p[2],tipoDeclaracion,'local',var,p[4])

  #en caso de agregarla la guarda en el diccionario
	if(iContadorDiccionarioVar == 0):
		dV = {iContadorDiccionarioVar : obj}
	else:
		dV[iContadorDiccionarioVar] = obj

  #incrementa contador
	iContadorDiccionarioVar = iContadorDiccionarioVar + 1

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
  asignacion : matchID arreglo EQUIVALE asignacion_aux
  '''
  global arregloCuadruplos
  global PilaO, PTipo
  global resultado
  global iContadorTemporal, iContadorCuadruplos, iContadorDiccionarioVar
  global tgi,tgf,tgs,tgb
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
    arregloCuadruplos.append(cuadruplo(op,operando2,"nul",resultado[iContadorCuadruplos]))
    PilaO.append(resultado[iContadorCuadruplos])
    iContadorCuadruplos += 1

#funcion auxiliar que decide si asignar una expresion aritmetica o bien una fincion de usuario 
def p_asignacion_aux(p):
	'''
	asignacion_aux : expresion PUNTO_Y_COMA
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
  	resultado.append(tgb)
  	#genera el cuadruplo
  	arregloCuadruplos.append(cuadruplo(op,operando1,operando2,resultado[iContadorCuadruplos]))
  	#el temporal lo mete a la pila
  	PilaO.append(tgb)
  	#suma uno al contador
  	iContadorCuadruplos += 1
  	tgb+=1

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
  var = 0

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
      	operadorAux = dicOperadores[operador]
      	operando2 = PilaO.pop()
      	operando1 = PilaO.pop()
      	iContadorTemporal += 1
      	if(tipo == 0):
      		var = tgi
      		tgi+=1
      	elif(tipo == 1):
      		var = tgf
      		tgf+=2
      	#agrega a la pila
      	PTipo.append(tipo)
      	resultado.append(var)
      	#agrega al cuadruplo
      	arregloCuadruplos.append(cuadruplo(operadorAux,operando1,operando2,var))
      	PilaO.append(var)
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
  var = 0
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
      	if(tipo == 0):
      		var = tgi
      		tgi+=1
      	elif(tipo == 1):
      		var = tgf
      		tgf+=2
      	#saca el operador y ambos operandos
      	operador = POper.pop()
      	operadorAux = dicOperadores[operador]
      	operando2 = PilaO.pop()
      	operando1 = PilaO.pop()
      	iContadorTemporal += 1
      	PTipo.append(tipo)
      	#al arreglo de resultados mete el numero de temporal
      	resultado.append(var)
      	#genera un nuevo cuadruplo
      	arregloCuadruplos.append(cuadruplo(operadorAux,operando1,operando2,resultado[iContadorCuadruplos]))
      	#mete el temporal
      	PilaO.append(var)
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

#match de id , enteros o flotantes, boleanos o strings
def p_var_cte(p):
  '''
  var_cte : matchID arreglo
          | matchCteInt
          | matchCteFloat
          | matchCteBool
          | matchCteString
  '''

#match de id checa que exista y guarda el tipo en la pila de tipo
def p_matchID(p):
  '''
  matchID : ID 
  '''
  global dV, dicTipos
  global iContadorDiccionarioVar
  global PilaO, PTipo
  global nombreIDArr
  varAux = 0
  tipo = ""
  auxTipo = -2
  #Checa si variable esta o no declarada
  for x in range(0,iContadorDiccionarioVar):
    if(p[1] != dV[x].getNombre()):
      varAux += 1
    else:
      #cubo semantico tipo de dato correcto
      nombreIDArr = p[1]
      tipo = dV[x].getTipo()
      auxTipo = dicTipos[tipo]
      PTipo.append(auxTipo)
      #Meter a pila operadores paso 1 del algoritmo
      dir = dV[x].getDireccion()
      PilaO.append(dir)
  #No esta declarada
  if(varAux == iContadorDiccionarioVar):
    raise errorSemantico("Variable no declarada: " + p[1])

#match una constante numerica entera
def p_matchCteInt(p):
  '''
  matchCteInt : CTE_INT
  '''
  global PilaO, PTipo, arregloConstantes
  global dicTipos
  global ctei,numConstantes
  auxTipo = -2
  var = 0
  varAux = 0
  #calcula el numero de diccionario
  auxTipo = dicTipos["int"]
  PTipo.append(auxTipo)
  #guardar en tabla de Constantes
  #checa que no exista
  for x in range(0,numConstantes):
    #si existe prende la variable var
    if(p[1] == arregloConstantes[x].getValor()):
      var = 1
      varAux = arregloConstantes[x].getDireccion()
  #en caso de no existir suma la cte i y la agrega a la tabla de constantes
  if(var == 0):
    obj = tablaConstantes(p[1],ctei)
    varAux = ctei
    arregloConstantes.append(obj)
    ctei+=1
    numConstantes+=1
  #meter a pila de operadores
  PilaO.append(varAux)

#match una constante numerica flotante
def p_matchCteFloat(p):
  '''
  matchCteFloat : CTE_FLOAT
  '''
  global PilaO,PTipo,arregloConstantes
  global dicTipos
  global ctef, numConstantes
  auxTipo = -2
  var = 0
  varAux = 0
  #cubo semantico toma el valor float directamente y lo guarda en op2 si op1 está ocupado

  auxTipo = dicTipos["float"]
  PTipo.append(auxTipo)
  #mete la constante a la pila de operandos
  PilaO.append(ctef)
  for x in range(0,numConstantes):
    #si existe prende la variable var
    if(p[1] == arregloConstantes[x].getValor()):
      var = 1
      varAux = arregloConstantes[x].getDireccion()
  #en caso de no existir suma la cte i y la agrega a la tabla de constantes
  if(var == 0):
    obj = tablaConstantes(p[1],ctef)
    varAux = ctef
    arregloConstantes.append(obj)
    ctef+=1
    numConstantes+=1
  #meter a pila de operadores
  PilaO.append(varAux)
  
#hace matech a una constante boleana con true o false
def p_matchCteBool(p):
  '''
  matchCteBool : TRUE
  				| FALSE
  '''
  global cteb, numConstantes
  global dicTipos,PTipo,PilaO,arregloConstantes
  var = 0
  varAux = 0
  #calcula diccionario
  auxTipo = dicTipos["bool"]
  PTipo.append(auxTipo)
  #checa que no exista
  for x in range(0,numConstantes):
    #si existe prende la variable var
    if(p[1] == arregloConstantes[x].getValor()):
      var = 1
      varAux = arregloConstantes[x].getDireccion()
  #en caso de no existir suma la cte i y la agrega a la tabla de constantes
  if(var == 0):
    obj = tablaConstantes(p[1],cteb)
    varAux = cteb
    arregloConstantes.append(obj)
    cteb+=1
    numConstantes+=1
  #meter a pila de operadores
  PilaO.append(varAux)

#sintaxis para permitir operaciones con arreglos
def p_arreglo(p):
	'''
	arreglo : validaDimensiones CORCHETE_IZQ expresion CORCHETE_DER
					| empty
	'''

#funcion auxiliar para generar cuadruplos de arreglos
def p_validaDimesiones(p):
	'''
	validaDimensiones : empty
	'''
	global PilaO, PTipo, resultado, dicOperadores
	global arregloCuadruplos
	global nombreIDArr
	global iContadorDiccionarioVar,iContadorCuadruplos
	global tgi
	tam = 0
	direccion = 0
	#obtiene el tipo de dato de la expresion del arreglo
	tipo = PTipo.pop();
	#si no es int no se puede
	if(tipo != 0):
		raise errorSemantico("Dentro del arreglo solo debes tener expresiones enteras")
	#saca el operando1 que contiene la expresion
	operando1 = PilaO.pop()
	#busca la variable que se llame igual
	for x in range(0,iContadorDiccionarioVar):
		if(nombreIDArr == dV[x].getNombre()):
			#saca el tamaño y la direccion
			tam = dV[x].getSize()
			direccion = dV[x].getDireccion()
	#cuadruplo verifica
	op = "ver"
	#para no perder la cuenta
	resultado.append("nul")
	#cuadruplo verifica simplificado
	#como solo recibe un numero 
	#ver exp 0 tam-1
	operador = dicOperadores["Ver"]
	arregloCuadruplos.append(cuadruplo(operador,operando1,0,tam-1))
	#suma al contador de cuadruplos
	iContadorCuadruplos+=1
	#segundo cuadruplo donde suma direccion base
	op = dicOperadores["+"]
	#es int la operacion por que es una direccion + una expresion "int"
	PTipo.append(0)
	#agregas el temporal que es una direccion de mememoria temporal int
	PilaO.append(tgi)
	#para no perder la cuenta
	resultado.append(tgi)
	#genera cuadruplo direccion base mas offset
	arregloCuadruplos.append(cuadruplo(op,operando1,op,tgi))
	#suma contadores
	tgi+=1
	iContadorCuadruplos+=1



###################################################################################################

#seccion 4 de codigo
###################################################################################################

#funcion para aceptar condiciones s
def p_condicion(p):
  '''
  condicion : imprimeIf PARENTESIS_IZQ condicion_2 PARENTESIS_DER DOS_PUNTOS cuacondicion1 estatuto_2 imprimeEndIf condicion_4
  '''

#genera el cuadruplo de condicion
def p_cuacondicion1(p):
  '''
  cuacondicion1 : empty
  '''
  global operador, operando1, operando2, resultado
  global iContadorCuadruplos
  global PSaltos, PilaO, dicOperadores
  global arregloCuadruplos
  #genera de operador gotof
  operador = dicOperadores["GotoF"]
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

#permite un else
def p_condicion_4(p):
  '''
  condicion_4 : matchElse DOS_PUNTOS estatuto_2 imprimeEndElse
              | empty
  '''

#para el cuadruplo "goto" solo debe aparecer cuando llega else if o else
def p_matchElse(p):
	'''
	matchElse : ELSE
	'''
	global PSaltos, PSaltosAux, dicOperadores
	global arregloCuadruplos
	global iContadorCuadruplos
	global operador, resultado
	global bIf

	PSaltos.append(iContadorCuadruplos)
	operador = dicOperadores["Goto"]
  #almacena el resultado en el arreglo de resultados para no perder la cuenta
	resultado.append("nul")
  #genera el cuadruplo
	arregloCuadruplos.append(cuadruplo(operador,-2,"nul","nul"))
  #sigye la cuenta del contador y resetea la variable boleana
	iContadorCuadruplos+=1
	bIf = 0

def p_imprimeEndElse(p):
  '''
  imprimeEndElse : END_ELSE
  '''
  global PSaltosAux
  global iContadorCuadruplos
  global arregloCuadruplos
  #llenas en donde se regresa cuando acabe el else
  res = PSaltos.pop()
  arregloCuadruplos[res].setOperando1(iContadorCuadruplos)
  print(p[1])

def p_imprimeIf(p):
  '''
  imprimeIf : IF
  '''
  global bIf
  #enciende if
  bIf = 1

def p_imprimeEndIf(p):
  '''
  imprimeEndIf : END_IF
  '''
  global PSaltos
  global arregloCuadruplos
  global iContadorCuadruplos

  #saca el tope de Psaltos , que es el apuntador al "gotof"
  res = PSaltos.pop()
  #al cuadruplo ubicado en la posición res le mete contador temporal + 1 porque apunta a la siguiente direccion
  arregloCuadruplos[res].setResultado(iContadorCuadruplos + 1)

###################################################################################################

#seccion 5 de codigo ----- escritura y lectura de código
###################################################################################################

#genera el cuadruplo para imprimir
def p_escritura(p):
  '''
  escritura : PRINT PARENTESIS_IZQ escritura_2 PARENTESIS_DER PUNTO_Y_COMA
  '''
  global operador
  global operando1
  global resultado
  global PilaO, dicOperadores
  global arregloCuadruplos
  global iContadorCuadruplos
  #genera cuadriplo print
  operador = dicOperadores["print"]
  operando1 = PilaO.pop()
  resultado.append("nul")
  arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos += 1

#hace match de un string o bien de una expresion
def p_escritura_2(p):
  '''
  escritura_2 : expresion
  '''

#imprime string
def p_matchCteString(p):
  '''
  matchCteString : CTE_STRING
  '''
  global ctes,numConstantes
  global dicTipos,PTipo,PilaO,arregloConstantes
  var = 0
  varAux = 0
  auxTipo = dicTipos["string"]
  PTipo.append(auxTipo)
  #mete la constante a la pila de operandos
  #checa que no exista
  for x in range(0,numConstantes):
    #si existe prende la variable var
    if(p[1] == arregloConstantes[x].getValor()):
      var = 1
      varAux = arregloConstantes[x].getDireccion()
  #en caso de no existir suma la cte i y la agrega a la tabla de constantes
  if(var == 0):
    obj = tablaConstantes(p[1],ctes)
    varAux = ctes
    arregloConstantes.append(obj)
    ctes+=1
    numConstantes+=1
  #meter a pila de operadores
  PilaO.append(varAux)

#genera cuadruplo de read
def p_read(p):
	'''
	read : READ PARENTESIS_IZQ matchID PARENTESIS_DER PUNTO_Y_COMA
	'''
	global operador
	global operando1
	global resultado
	global PilaO, arregloCuadruplos, dicOperadores
	global iContadorCuadruplos
	#genera cuadriplo print
	operador = dicOperadores["read"]
	operando1 = PilaO.pop()
	resultado.append("nul")
	arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
	iContadorCuadruplos += 1

###################################################################################################

#seccion 6 de codigo
###################################################################################################

#funcion de sintaxis del ciclo --> estructura "while ( expresion ) : codigo end_while"
def p_ciclo(p):
  '''
  ciclo : imprimeWhile PARENTESIS_IZQ exp PARENTESIS_DER DOS_PUNTOS cuaciclo1 estatuto_2 imprimeEndWhile
  '''

#funcion auxiliar para ayudar a generar el cuadruplo gotof
def p_cuaciclo1(p):
  '''
  cuaciclo1 : empty
  '''
  global operador, operando1, operando2, resultado
  global iContadorCuadruplos
  global PSaltos, PilaO, PSaltos
  global arregloCuadruplos, dicOperadores

  #genera de operador gotof
  operador = dicOperadores["GotoF"]
  #el operando 1 es el temporal o ultima variable localizada en pila o
  operando1 = PilaO.pop()
  #agrega la posición actual a la pila de saltos
  PSaltos.append(iContadorCuadruplos)
  #el resultado le asigna -2 para estandarizar que está vacio
  resultado.append("nul")
  #genera el cuadruplo
  arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
  #suma uno al contador
  iContadorCuadruplos += 1

def p_imprimeWhile(p):
  '''
  imprimeWhile : WHILE
  '''
  #cuando entra al while prende el boleano de ciclo
  global bCiclo
  global PSaltos
  global iContadorCuadruplos
  bCiclo = 1
  #para saber donde regresar cuando se haga el ciclo
  PSaltos.append(iContadorCuadruplos)

def p_imprimeEndWhile(p):
  '''
  imprimeEndWhile : END_WHILE
  '''
  global PSaltos,dicOperadores
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
  operador = dicOperadores["Goto"]
  #almacena el resultado en el arreglo de resultados para no perder la cuenta
  resultado.append(auxresultado)
  #genera el cuadruplo
  arregloCuadruplos.append(cuadruplo(operador,resultado[iContadorCuadruplos],"nul","nul",))
  #sigye la cuenta del contador y resetea la variable boleana
  bCiclo = 0
  iContadorCuadruplos += 1

###################################################################################################

#seccion 7 de codigo
###################################################################################################
#funciones

#para definir funciones
#recibe un tipo --> int float string void
#puede o no tener parametros
#en caso de retornar un tipo esta obligada a tner return
def p_function(p):
  '''
  function : imprimeDef tipoFunction matchNomFunction PARENTESIS_IZQ function_aux PARENTESIS_DER agregaFunc DOS_PUNTOS declaracion_3 estatuto_2 END_DEF
  '''

#funcion auxiliar que agrega la funcion a la tabla de funciones
def p_agregaFunc(p):
	'''
	agregaFunc : empty
	'''
	global bscope
	global listaParamFuncion
	global iContadorDiccionarioFuncion, iContadorDiccionarioVar,iContadorCuadruplos
	global dF,dV
	global tipoDeclaracionFuncion
	global vgi, vli, vgf, vlf, vgs, vls
	global nombreFuncion

	#checa que no exista una funcion que se llame igual
	for x in range(0,iContadorDiccionarioFuncion):
		varFunc = dF[x]
		if(nombreFuncion == varFunc.getNombre()):
			raise errorSemantico("Función previamente definida: " + p[1])

	#agrega los parametros de la funcion
	listaAux = []
	listaAux.extend(listaParamFuncion)
	varAux = tablaFunciones(nombreFuncion,tipoDeclaracionFuncion,listaAux, iContadorCuadruplos)

	#la agrega al diccionario
	if(iContadorDiccionarioFuncion == 0):
		dF = {iContadorDiccionarioFuncion : varAux}
	else:
		dF[iContadorDiccionarioFuncion] = varAux

	#incrementa el contadoe
	iContadorDiccionarioFuncion = iContadorDiccionarioFuncion + 1
	print(dF)
	bscope = 0
	#si no es void crea una variable global coon el mismo nombre

#funcion auxiliar que en caso de que la funcion retorne valor la guarda como var global
#sirve para el parche ^
def p_matchNomFunction(p):
	'''
	matchNomFunction : ID
	'''
	global nombreFuncion
	global bscope
	global listaParamFuncion
	global iContadorDiccionarioFuncion, iContadorDiccionarioVar
	global dF,dV
	global tipoDeclaracionFuncion
	global vgi, vli, vgf, vlf, vgs, vls

	nombreFuncion = p[1]
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
		obj = tablaVar(nombreFuncion,tipoDeclaracionFuncion,"global",var,1)
		#lo agrega al diccionario
		dV[iContadorDiccionarioVar] = obj
		#incrementa el contador
		iContadorDiccionarioVar = iContadorDiccionarioVar + 1

#tipo de funcion
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
  #lo guarda en tipo declaracion
  tipoDeclaracionFuncion = p[1]
  #boleano de retorna ayuda a funcion_4
  if(p[1] != "void"):
  	bRetorna = 1

#auxiliar para declaracion de parametros
def p_function_aux(p):
  '''
  function_aux : function_2
               | empty
  '''

#declara parametros
def p_function_2(p):
  '''
  function_2 : tipo ID function_3
  '''
  global bscope
  global iContadorDiccionarioVar
  global dV
  global tipoDeclaracion
  global vli, vlf, vls
  global listaParamFuncion
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
  
  #se genera el objeto y se agrega a la listaParam
  obj = tablaVar(p[2],tipoDeclaracion,'local',var,1)
  aux = dicTipos[tipoDeclaracion]
  listaParamFuncion.append(aux)

  #en caso de agregarla la guarda en el diccionario
  if(iContadorDiccionarioVar == 0):
  	dV = {iContadorDiccionarioVar : obj}
  else:
  	dV[iContadorDiccionarioVar] = obj

  #incrementa contador
  iContadorDiccionarioVar = iContadorDiccionarioVar + 1

#para declaar más parametros
def p_function_3(p):
  '''
  function_3 : COMA function_2
            | empty
  '''

#return expresion;
def p_returnFunc(p):
  '''
  returnFunc : RETURN expresion PUNTO_Y_COMA
              | empty
  '''
  global PilaO, PTipo
  global arregloCuadruplos
  global iContadorCuadruplos
  global operando1, operador, resultado, operando2, op1,op2, op
  global tipoDeclaracionFuncion
  global dicOperadores,dicTipos
  global bRetorna
  #verifica que si está boleana haya un return si no termina
  if((bRetorna == 1) and (p[1] != 'return')):
    raise errorSemantico("Definiste una funcion que debe retornar un valor y no lo retorna ")
  #hace el return cuadruplo
  if(p[1] == 'return'):
  	#checa que regrese el mismo tipo de dato que la exp
  	op1 = PTipo.pop()
  	op2 = dicTipos[tipoDeclaracionFuncion]
  	op = dicOperadores["="]
  	tipo = cubo[op1][op2][op]
  	#error si no
  	if(tipo == -1):
  		raise errorSemantico("uso incorrecto de tipos ")
  	#si esta bien hace el cuadruplo
  	else:
  		operando1 = PilaO.pop()
  		operador = dicOperadores["Return"]
  		resultado.append("nul")
  		arregloCuadruplos.append(cuadruplo(operador,operando1,"nul","nul"))
  		iContadorCuadruplos+=1

#destruye variables de lista paramfuncion y del Dic.de vars
def p_destroyVars(p):
  '''
  destroyVars : empty
  '''
  global arregloCuadruplos
  global dV,dicOperadores
  global iContadorInicioLocal, iContadorDiccionarioVar, iContadorTemporal, iContadorCuadruplos
  global resultado
  global vli,vlf,vls,vlb,tgi,tgf,tgs,tgb
  global bRetorna
  global listaParamFuncion

  iAux = 0
  iAux = iContadorInicioLocal
  #borra todas las declaradas desde inicio local-->actual si son locales
  for x in range(iContadorInicioLocal , iContadorDiccionarioVar):
    if(dV[x].getScope() == "local"):
      del dV[x]
  del listaParamFuncion[:]
 
  #para que se resetee bien el diccionario en caso de que haya una var/funcion
  if(bRetorna == 1):
    iContadorDiccionarioVar = iAux + 1
  else:
    iContadorDiccionarioVar = iAux

  #resetea temporal
  iContadorTemporal = 1
  #resetea memoria
  vli= 10000
  vlf = 11000
  vlb = 12000
  vls = 13000
  tgi = 20000
  tgf = 21000
  tgs = 22000
  tgb = 23000
  #genera cuadruplo ret
  resultado.append("nul")
  operador = dicOperadores["Ret"]
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul","nul"))
  iContadorCuadruplos+=1
  #elimina bRetorna
  bRetorna = 0

def p_imprimeDef(p):
  '''
  imprimeDef : DEF
  '''
  global bscope
  global iContadorInicioLocal
  #prende el contador de locales e inicia el de locales
  bscope = 1
  #guarda pos donde inicia el diccionario local
  iContadorInicioLocal = iContadorDiccionarioVar


###################################################################################################

#seccion 8 de codigo
###################################################################################################

#define la sintaxixs de una función de usuario
def p_funcionUsuario(p):
  '''
  funcionUsuario : matchFunction PARENTESIS_IZQ era_func functionUsuario_parametros PARENTESIS_DER PUNTO_Y_COMA go_sub
  '''

#hace match con el nombre de la funcion y verifica si existe
def p_matchFunction(p):
	'''
	matchFunction : ID
	'''
	#checa si la función que tratas de usar existe o no, en caso de no existir levanata una excepción
	global dF
	global iContadorDiccionarioFuncion
	global funcionActiva
	varAux = 0
	for x in range(0,iContadorDiccionarioFuncion):
		if(p[1] != dF[x].getNombre()):
			varAux += 1
		if(varAux == iContadorDiccionarioFuncion):
			raise errorSemantico("Funcion no definida: " + p[1])
		else:
			#si no la almacena en funcionActiva
			funcionActiva = p[1]

#cuadruplo era
def p_era_func(p):
	'''
	era_func : empty
	'''
	global PilaO
	global iContadorTemporal, iContadorCuadruplos
	global arregloCuadruplos,resultado
	global dicOperadores
	global funcionActiva
	#era de funcionActiva
	resultado.append("nul")
	operador = dicOperadores("Era")
	arregloCuadruplos.append(cuadruplo(operador,funcionActiva,"nul","nul"))
	iContadorCuadruplos+=1

#cuadruplo gosub + parche guadalupano
def p_go_sub(p):
	'''
	go_sub : empty
	'''
	global arregloCuadruplos, dF,resultado, dicTipos, dicOperadores
	global iContadorCuadruplos, iContadorDiccionarioFuncion, iContadorTemporal
	global funcionActiva
	global PTipo
	global tgi,tgf,tgs,tgb
	tipo = ""
	tipoDic = -2
	var = 0
	#cuadruplo gosub
	resultado.append("nul")
	operador = dicOperadores["Gosub"]
	arregloCuadruplos.append(cuadruplo(operador,funcionActiva,"nul","nul"))
	iContadorCuadruplos+=1
	#parche guadalupano
	#checa el tipo
	for x in range(0,iContadorDiccionarioFuncion):
		if(dF[x].getNombre() == funcionActiva):
			tipo = dF[x].getTipo();
	#si no es void DEBE haber parche
	if(tipo != "void"):
		#agrega el tipo de funcion a la pila de tipos
		tipoDic = dicTipos[tipo]
		PTipo.append(tipoDic)
		#direccion del temporal
		if(tipoDic == 0):
			var = tgi
			tgi+=1
		elif(tipoDic == 1):
			var = tgf
			tgf+=1
		elif(tipoDic == 2):
			var = tgs
			tgs+=1
		else:
			var = tgb
			tgb+=1
		#agrega la funcion a la pila de operadores
		PilaO.append(var)
		resultado.append(var)
		#genera parche guadalupano
		arregloCuadruplos.append(cuadruplo("=",funcionActiva,"nul",resultado[iContadorCuadruplos]))
		iContadorTemporal += 1
		iContadorCuadruplos += 1

#funcion auxiliar que checa parametros en caso de recibirlos
def p_functionUsuario_parametros(p):
  '''
  functionUsuario_parametros : functionUsuario_aux1 functionValidaParams
               				| empty
  '''

#funcion auxiliar de p_funcionUsuario (recibes parametros)
#cuadruplo de parametros
def p_functionUsuario_aux1(p):
  '''
  functionUsuario_aux1 : expresion functionUsuario_aux2
  '''
  global iContadorCuadruplos, iContadorParametros
  global arregloCuadruplos,resultado, dicOperadores
  global PilaO, PTipo
  global funcionActiva
  global tipo
  #checa tipo de parametro de la funcion y los agrgea a auxiliar de parametros
  tipo = PTipo.pop()
  listaAuxParamFuncion.append(tipo)
  #genera cuadruplo de param
  operando1 = PilaO.pop()
  resultado.append(iContadorParametros + 1)
  operador = dicOperadores["Param"]
  arregloCuadruplos.append(cuadruplo(operador,operando1,"nul",resultado[iContadorCuadruplos]))
  iContadorCuadruplos+=1
  iContadorParametros+=1

#funcion auxiliar de p_funcionUsuario (, mas parametros)
def p_functionUsuario_aux2(p):
  '''
  functionUsuario_aux2 : COMA functionUsuario_aux1
            			| empty
  '''

#valida que numero y tipo de params sean correctos(igual que como se definió)
def p_functionValidaParams(p):
	'''
	functionValidaParams : empty
	'''
	global dF,listaAuxParamFuncion
	global funcionActiva, iContadorDiccionarioFuncion
	listaAux = []
	#guarda los parametros de la funcion qe se declaró
	for x in range(0,iContadorDiccionarioFuncion):
		objAux = dF[x]
		if(objAux.getNombre() == funcionActiva):
			listaAux.extend(objAux.getParametros())
	#compara tamaños de listas
	if(len(listaAuxParamFuncion) == len(listaAux)):
		#compara tipos de parametrso sean iguales(está asi por que usé directamente el tipo del diccionario de tipos)
		for x in range (0, len(listaAux)):
			if(listaAuxParamFuncion[x] != listaAux[x]):
				raise errorSemantico("Tipo de Parametros no concuerda con los parametros de la funcion")
	#tamaño no igual --> error
	else:
		raise errorSemantico("La cantidad de parametros no concuerda con los parametros de la funcion")

###################################################################################################

#seccion 9 de codigo
###################################################################################################

#función de sintaxis que revisa si se recive la función predeinida de checkWall();
def p_checkwall(p):
  '''
  checkwall : CHECKWALL PARENTESIS_IZQ PARENTESIS_DER PUNTO_Y_COMA
  '''
  global iContadorCuadruplos
  global arregloCuadruplos, resultado, dicOperadores
  #cuadruplo checkwall, este no recibe un era ni gosub por que es una funcion que yo defino en la interfaz gráfica
  resultado.append("nul")
  operador = dicOperadores["checkwall"]
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul","nul"))
  iContadorCuadruplos+=1
  print("Encontré un checkwall\n")

#función de sintaxis que revisa si se recive la función predeinida de move();
def p_move(p):
  '''
  move : MOVE PARENTESIS_IZQ PARENTESIS_DER PUNTO_Y_COMA
  '''
  global iContadorCuadruplos
  global arregloCuadruplos, resultado, dicOperadores
  #cuadruplo move
  resultado.append("nul")
  operador = dicOperadores["move"]
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul","nul"))
  iContadorCuadruplos+=1

#función de sintaxis que revisa si se recive la función predeinida de turnRight();
def p_turnright(p):
  '''
  turnright : TURN_RIGHT PARENTESIS_IZQ PARENTESIS_DER PUNTO_Y_COMA
  '''
  global iContadorCuadruplos
  global arregloCuadruplos,resultado, dicOperadores
  #cuadruplo turnRight, no llama a era ni a gosub por que es una funcion diferente
  resultado.append("nul")
  operador = dicOperadores["turnRight"]
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul","nul"))
  iContadorCuadruplos+=1

#función de sintaxis que revisa si se recive la función predeinida de turnLeft();
#cuadruplo turnleft
def p_turnleft(p):
  '''
  turnleft : TURN_LEFT PARENTESIS_IZQ PARENTESIS_DER PUNTO_Y_COMA
  '''
  global iContadorCuadruplos
  global arregloCuadruplos,resultado, dicOperadores
  resultado.append("nul")
  operador = dicOperadores["turnLeft"]
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul","nul"))
  iContadorCuadruplos+=1

#función de sintaxis que revisa si se recive la función predeinida de pickBeeper();
#genera cuadruplo pickbeeper
def p_pickbeeper(p):
  '''
  pickbeeper : PICK_BEEPER PARENTESIS_IZQ PARENTESIS_DER PUNTO_Y_COMA
  '''
  global iContadorCuadruplos
  global arregloCuadruplos,resultado, dicOperadores
  #genera cuasdruplo pickBeeper
  resultado.append("nul")
  operador = dicOperadores["pickBeeper"]
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul","nul"))
  iContadorCuadruplos+=1

#función de sintaxis que revisa si se recive la función predeinida de putBeeper();
#genera cuadruplo putbeeper
def p_putbeeper(p):
  '''
  putbeeper : PUT_BEEPER PARENTESIS_IZQ PARENTESIS_DER PUNTO_Y_COMA
  '''
  #genera el cuadrupli putBeeper, solo se ocupa saber este comando
  #el resto de la info para procesarlo se genera dentro de la interfaz
  global iContadorCuadruplos
  global arregloCuadruplos,resultado, dicOperadores
  resultado.append("nul")
  operador = dicOperadores["putBeeper"]
  arregloCuadruplos.append(cuadruplo(operador,"nul","nul","nul"))
  iContadorCuadruplos+=1

#########################################################################################################################################################################
########################################################################################################################################################################
#########################################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
###########################################################################################################################################################

# Error rule for syntax errors
def p_error(p):
  raise errorSintactico("Error de sintaxis")

#funcion que genera los obj del compilador
def writeObjectFile():
	#genera obj de constantes
	#toma el valor de la constante y su dirección virtual
	filename = argv
	filename = "aplusOBJConstantes.txt"
	target = open(filename, 'w')
	target.truncate()
	for x in range(0,numConstantes):
		target.write(str(arregloConstantes[x].getDireccion()))
		target.write("\t")
		target.write(str(arregloConstantes[x].getValor()))
		target.write("\n")
	target.close()

	#genera el obj de cuadruplos
	#toma cada uno de los cuadruplos ya referenciando al tipo de operador (con numero)
	#y con direcciones virtuales
	filename = argv
	filename = "aplusOBJCuadruplos.txt"
	target = open(filename, 'w')
	target.truncate()
	for x in range(0,iContadorCuadruplos):
		target.write(str(arregloCuadruplos[x].getOperador()))
		target.write("\t")
		target.write(str(arregloCuadruplos[x].getOperando1()))
		target.write("\t")
		target.write(str(arregloCuadruplos[x].getOperando2()))
		target.write("\t")
		target.write(str(arregloCuadruplos[x].getResultado()))
		target.write("\n")
	target.close()

	#genera el obj de funciones
	#toma el toda la información de la tabla de procedimientos la cual incluye nombre, tipo de retorno, parametros,e inicio de Cuadruplo
	filename = argv
	filename = "aplusOBJFunciones.txt"
	target = open(filename, 'w')
	target.truncate()
	for x in range(0,iContadorDiccionarioFuncion):
		target.write(str(dF[x].getNombre()))
		target.write("\t")
		target.write(str(dF[x].getTipo()))
		target.write("\t")
		target.write(str(dF[x].getParametros()))
		target.write("\t")
		target.write(str(dF[x].getStart()))
		target.write("\n")
	target.close()

# Build the parser
#main 
parser = yacc.yacc()
data = ""
f = open('prueba.txt', 'r')
for line in f:
  if not line.strip():
    continue
  else:
    data = data + line
result = parser.parse(data)
writeObjectFile()

print("\n")
#prints para debugear archivo
for x in range(0,iContadorDiccionarioVar):
  print("variable numero " + str(x))
  print(dV[x].getNombre())
  print(dV[x].getTipo())
  print(dV[x].getDireccion())
  print("--------------------")

print("\n")

for x in range(0,iContadorDiccionarioFuncion):
	print("funcion numero" + str(x))
	print(dF[x].getNombre())
	print(dF[x].getTipo())
	print(dF[x].getParametros())
	print(dF[x].getStart())
	print("-----------------")

print("\n")

for x in range(0,iContadorCuadruplos):
	print("Cuadruplo num " + str(x))
	print(arregloCuadruplos[x].getOperador())
	print(arregloCuadruplos[x].getOperando1())
	print(arregloCuadruplos[x].getOperando2())
	print(arregloCuadruplos[x].getResultado())