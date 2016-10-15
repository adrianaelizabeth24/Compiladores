#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Adriana Valenzuela a01195331
#Mayra Ruiz a00812918


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
tmptipo = "";

from tablaVar import tablaVar
from tablaFunciones import tablaFunciones
from errorSintactico import errorSintactico
from errorLexico import errorLexico
from errorSemantico import errorSemantico
import ply.lex as lex
import ply.yacc as yacc
import sys

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

  tmptipo = p[1]

  if(bscope == 0):
    arregloVar.append(tablaVar(p[2],p[1],'global'))
  else:
    arregloVar.append(tablaVar(p[2],p[1],'local'))

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
       | BOOL
  '''
  print(p[1]);

def p_asignacion(p):
  '''
  asignacion : ID imprimeEquivale asignacion_aux

  '''
  global arregloVar
  global iContadorDiccionarioVar
  varAux = 0;
  for x in range(0,iContadorDiccionarioVar - 1):
  	if(p[1] != arregloVar[x].getNombre()):
  		varAux += 1
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
  expresion : termino expresion_2
  '''

def p_expresion_2(p):
  '''
  expresion_2 : imprimeSuma expresion
              | imprimeResta expresion
              | empty
  '''

def p_termino(p):
  '''
  termino : factor termino_2
  '''

def p_termino_2(p):
  '''
  termino_2 : imprimeMultiplicacion termino
            | imprimeDivision termino
            | empty
  '''

def p_factor(p):
  '''
  factor : imprimeParentesisIzq exp imprimeParentesisDer
          | imprimeSuma var_cte
          | imprimeResta var_cte
          | var_cte
  '''

def p_var_cte(p):
  '''
  var_cte : matchID
          | CTE_INT
          | CTE_FLOAT
  '''
  print(p[1])

def p_matchID(p):
	'''
	matchID : ID
	'''
	global arregloVar
	global iContadorDiccionarioVar
	varAux = 0
	for x in range(0,iContadorDiccionarioVar - 1):
		if(p[1] != arregloVar[x].getNombre()):
			varAux += 1
	if(varAux == iContadorDiccionarioVar - 1):
		raise errorSemantico("Variable no declarada: " + p[1])


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
	varAux = 0
	for x in range(0,iContadorDiccionarioFuncion - 1):
		if(p[1] != arregloFuncion[x].getNombre()):
			varAux += 1
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

def p_imprimeMultiplicacion(p):
  '''
  imprimeMultiplicacion : MULTIPLICACION
  '''
  print(p[1])

def p_imprimeDivision(p):
  '''
  imprimeDivision : DIVISION
  '''
  print(p[1])

def p_imprimeSuma(p):
  '''
  imprimeSuma : SUMA
  '''
  print(p[1])

def p_imprimeResta(p):
  '''
  imprimeResta : RESTA
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
print(dV)
print(result)

