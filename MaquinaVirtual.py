#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Adriana Valenzuela a01195331
#Mayra Ruiz a00812918

from tablaFunciones import tablaFunciones
from errorEjecucion import errorEjecucion
import sys
from sys import argv

#variables globales
#memoria
diccionarioMemGlobal = {}
diccionarioMemTemporalGl = {}
diccionarioMemConstante = {}
diccionarioMemLocal = [{}]
diccionarioMemTemporalLl = [{}]
#cuadruplos
arregloCuadruplos = []
#funciones
arregloFunciones = []
iSaveInstruccionActual = []
arregloGraphics = []

InstruccionActual = 0
FuncionActiva = 0
iPosArray = -2
numParametros = 0
iContadorParametros = 0
bFuncion = False


i = True

'''
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
'''

#dicOperadores = {"+" : 0, "-" : 1, "*" : 2, "/" : 3,
# "<" : 4, ">": 5, "=" : 6,"<>" : 7, "==" : 8, "&": 9, "|": 10, "<=": 11, ">=": 12, 
#"print" : 13 , "read": 14, "end": 15, "Goto": 16, "GotoF": 17,
# "Era":18, "Gosub":19, "Param":20, "Ver":21, "Ret":22, "Return":23,
# "move":24 , "checkwall":25, "turnRight":26, "turnLeft":27, "pickBeeper":28, "putBeeper":29}

#funcion que lee los archivos de código intermedio
def leeObj():
	leeFunciones()
	leeConstantes()
	leeCuadruplos()

#funcion que lee el archivo de tablas de procedimientos
#dicho archivo contiene:
#nombre de la funcion, tipo de funcion, lista de direcciones de parametros, inicio de cuadruplo, dirección virtual de la funcion
#lo almacena en arregloFunciones
def leeFunciones():
	global arregloFunciones
	nombre = ""
	tipoFunc = ""
	listaParam = []
	inicioCuadruplo = 0
	dvm = 0
	#abre obj
	f = open('aplusOBJFunciones.txt','r')
	for line in f:
		iContadorAux = 0
		for word in line.split():
			#guarda nombe de función
			if(iContadorAux == 0):
				nombre = word
			#guarda típo de funcion
			elif(iContadorAux == 1):
				tipoFunc = word
			#guarda parametros de funcion
			elif(iContadorAux == 2):
				#guarda donde se inicia el cuadruplo
				inicioCuadruplo = int(word)
			elif(iContadorAux == 3):
				dvm = int(word)
			else:
				#elimina corchetes y comas
				word = word[1:]
				word = word[:-1]
				if(word != ""):
					listaParam.append(int(word))
				else:
					listaParam.append(-2)
			iContadorAux += 1
		#agrega la función al arreglo de funciones
		arregloFunciones.append(tablaFunciones(nombre,tipoFunc,-2,listaParam,inicioCuadruplo,dvm))

#funcion que lee el archvio de constantes
#archivo contiene direccion virtual y valor de constante
#lo almacena directamente en memoria
def leeConstantes():
	global diccionarioMemConstante
	key = 0
	value = 0
	#abre el obj
	f = open('aplusOBJConstantes.txt', 'r')
	for line in f:
		iContadorAux = 0
		for word in line.split():
			#guarda la direccion virtual
			if(iContadorAux == 0):
				key = int(word)
			else:
				#guarda el valor
				#si es menor que 31000 la dirección significa int
				if(key < 31000):
					value = int(word)
				#float
				elif(key > 30999 and key < 32000):
					value = float(word)
				#string
				else:
					#maneja que no se borren partes de la palabra si vienen espacios
					if(iContadorAux == 1):
						value = word
					else:
						value = str(value) + " " + word
			iContadorAux+=1
		#agrega a memoria
		diccionarioMemConstante[key] = value

#funcion que lee el archivo de cuadruplos
#lo almacena en arregloCuadruplos
def leeCuadruplos():
	global arregloCuadruplos
	op = 0
	op1 = 0
	op2 = 0
	res = 0
	#abre el obj
	f = open('aplusOBJCuadruplos.txt', 'r')
	for line in f:
		iContadorAux = 0
		bWord = False
		for word in line.split():
			#soiempre lo convierte a int
			if(iContadorAux == 0):
				op = int(word)
				#si es era o gosub la siguiente vas a usar palabra y enciende la palabra
				if((op == 18) or (op == 19)):
					bWord = True
			elif(iContadorAux == 1):
				#si es nul convierte a -2 --> vacio
				if(word == "nul"):
					op1 = -2
				#si está encendido lee palabra y lo apaga
				elif(bWord == 1):
					op1 = word
					bWord = False
				#si no convierte a numero
				else:
					op1 = int(word)
			#lee op2 lo convierte a num
			elif(iContadorAux == 2):
				if(word == "nul"):
					op2 = -2
				else:
					op2 = int(word)
			#lee resultado
			else:
				if(word == "nul"):
					res = -2
				else:
					res = int(word)
			iContadorAux+=1
		#lo agrega al arreglo de memoria
		arregloCuadruplos.append([op,op1,op2,res])

#funcion para sumar dos operandos
#en caso de recibir un operando negativo
#esta tratando con un temporal indirecto
#es el temporal que almacena una dirección (la base + offset)
#debe acceder al valor de la dirección que almacena
def Suma(op1, op2, result):
	#si ambos son positivos
	if(op1 > 0 and op2 > 0):
		#obtiene valor 1
		valor1 = getValor(op1)
		#obtiene valor 2
		valor2 = getValor(op2)
		#suma
		res = valor1 + valor2
		#asigna a memoria
		setValor(result, res)
	#op1 es temporal indirecto
	elif(op1 < 0 and op2 > 0):
		#dirección nueva
		dirNueva1 = getValor(op1)
		#encuentra valor 1
		valor1 = getValor(dirNueva1)
		#encuentra valor 2
		valor2 = getValor(op2)
		#operacion
		res = valor1 + valor2
		#asigna a memoria
		setValor(result,res)
	#op2 es temporal indirecto
	elif(op1 > 0 and op2 < 0):
		#valor
		valor1 = getValor(op1)
		#nueva dirección
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#resultado
		res = valor1 + valor2
		#asignación
		setValor(result,res)
	#ambos son temporales indirectos
	else:
		#dirección nueva1
		dirNueva1 = getValor(op1)
		#valor
		valor1 = getValor(dirNueva1)
		#dirección nueva2
		dirNueva2 = getValor(op2)
		#valor2
		valor2 = getValor(dirNueva2)
		#resultado
		res = valor1 + valor2
		#asignación
		setValor(result,res)

#funcion para restar dos operandos
#en caso de recibir un operando negativo
#esta tratando con un temporal indirecto
#es el temporal que almacena una dirección (la base + offset)
#debe acceder al valor de la dirección que almacena
def Resta(op1, op2, result):
	#ningun temporal indirecto
	if(op1 > 0 and op2 > 0):
		#valor1
		valor1 = getValor(op1)
		#valor 2
		valor2 = getValor(op2)
		#resta
		res = valor1 - valor2
		#asigna resultado a memoria
		setValor(result, res)
	#temporal indirecto
	elif(op1 < 0 and op2 > 0):
		#obtiene nueva dirección
		dirNueva1 = getValor(op1)
		#obtiene valor de la dirección
		valor1 = getValor(dirNueva1)
		#obtiene valor2
		valor2 = getValor(op2)
		#resta
		res = valor1 - valor2
		#asigna valor a memoria
		setValor(result,res)
	#temporal indirecto
	elif(op1 > 0 and op2 < 0):
		#valor1
		valor1 = getValor(op1)
		#nueva dirección
		dirNueva2 = getValor(op2)
		#valor de dirNueva2
		valor2 = getValor(dirNueva2)
		#resta
		res = valor1 - valor2
		#asigna valor a memoria
		setValor(result,res)
	#dos temporales indirectos
	else:
		#dirección nueva
		dirNueva1 = getValor(op1)
		#valor
		valor1 = getValor(dirNueva1)
		#dirección nueva
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#resta
		res = valor1 - valor2
		#asigna valor
		setValor(result,res)

#funcion para multiplicar dos operandos
#en caso de recibir un operando negativo
#esta tratando con un temporal indirecto
#es el temporal que almacena una dirección (la base + offset)
#debe acceder al valor de la dirección que almacena
def Multiplicacion(op1, op2, result):
	if(op1 > 0 and op2 > 0):
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		res = valor1 * valor2
		setValor(result, res)
	elif(op1 < 0 and op2 > 0):
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		res = valor1 * valor2
		setValor(result,res)
	elif(op1 > 0 and op2 < 0):
		valor1 = getValor(op1)
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		res = valor1 * valor2
		setValor(result,res)
	else:
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		res = valor1 * valor2
		setValor(result,res)

#funcion para dividir dos operandos
#en caso de recibir un operando negativo
#esta tratando con un temporal indirecto
#es el temporal que almacena una dirección (la base + offset)
#debe acceder al valor de la dirección que almacena
def Division(op1, op2, result):
	if(op1 > 0 and op2 > 0):
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		res = valor1 / valor2
		setValor(result, res)
	elif(op1 < 0 and op2 > 0):
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		res = valor1 / valor2
		setValor(result,res)
	elif(op1 > 0 and op2 < 0):
		valor1 = getValor(op1)
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		res = valor1 / valor2
		setValor(result,res)
	else:
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		res = valor1 / valor2
		setValor(result,res)

#compara dos valores con < y retorna verdadero o falso
#de acuerdo a los operadores
#en caso de recibir un operando negativo
#esta tratando con un temporal indirecto
#es el temporal que almacena una dirección (la base + offset)
#debe acceder al valor de la dirección que almacena
def MenorQue(op1, op2, result):
	#no hay temporales indirectos
	if(op1 > 0 and op2 > 0):
		#valor
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		#compara y resuelve
		if(valor1 < valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op1 es indirecto
	elif(op1 < 0 and op2 > 0):
		#nueva direccion
		dirNueva1 = getValor(op1)
		#valores
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		#compara
		if(valor1 < valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op2 es indirecto
	elif(op1 > 0 and op2 < 0):
		#valor
		valor1 = getValor(op1)
		#direccion
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 < valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#ambos son indirectos
	else:
		#direccion y valor
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		#direccion y valor
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 < valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")

#compara dos valores con > y retorna verdadero o falso
#verifica temporales indirectos
def MayorQue(op1, op2, result):
	#no hay temporales indirectos
	if(op1 > 0 and op2 > 0):
		#valor
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		#compara y resuelve
		if(valor1 > valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op1 es indirecto
	elif(op1 < 0 and op2 > 0):
		#nueva direccion
		dirNueva1 = getValor(op1)
		#valores
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		#compara
		if(valor1 > valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op2 es indirecto
	elif(op1 > 0 and op2 < 0):
		#valor
		valor1 = getValor(op1)
		#direccion
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 > valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#ambos son indirectos
	else:
		#direccion y valor
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		#direccion y valor
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 > valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")

#asigna el valor de una dirección a otro
#verifica temporales indirectos
def Asignacion(op1,result):
	#no indirectos
	if(op1 > 0 and result > 0):
		#valor de op1
		valor = getValor(op1)
		#se asigna a direcion de result
		setValor(result,valor)
	#un indirecto
	elif(op1 < 0 and result > 0):
		#dirección nueva de op1
		dirNueva = getValor(op1)
		#valor de dirNueva
		valor = getValor(dirNueva)
		#asigna valor
		setValor(result,valor)
	#un indirecto
	elif(op1 > 0 and result < 0):
		#dirección nueva
		dirNueva = getValor(result)
		#valor
		valor = getValor(op1)
		#asignar valor a dirección nueva
		setValor(dirNueva,valor)
	#dos indirectos
	else:
		#direccion nueva de op1
		dirNueva1 = getValor(op1)
		#dirección nueva result
		dirNueva2 = getValor(result)
		valor = getValor(dirNueva1)
		#asigna valor de dirección nueva1 a dirección nueva 2
		setValor(dirNueva2,valor)

#compara dos valores con <> y retorna verdadero o falso
#verifica temporales indirectos
def Diferente(op1, op2, result):
	#no hay temporales indirectos
	if(op1 > 0 and op2 > 0):
		#valor
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		#compara y resuelve
		if(valor1 != valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op1 es indirecto
	elif(op1 < 0 and op2 > 0):
		#nueva direccion
		dirNueva1 = getValor(op1)
		#valores
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		#compara
		if(valor1 != valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op2 es indirecto
	elif(op1 > 0 and op2 < 0):
		#valor
		valor1 = getValor(op1)
		#direccion
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 != valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#ambos son indirectos
	else:
		#direccion y valor
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		#direccion y valor
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 != valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")

#compara dos valores con == y retorna verdadero o falso
#verifica temporales indirectos
def IgualQue(op1, op2, result):
	#no hay temporales indirectos
	if(op1 > 0 and op2 > 0):
		#valor
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		#compara y resuelve
		if(valor1 == valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op1 es indirecto
	elif(op1 < 0 and op2 > 0):
		#nueva direccion
		dirNueva1 = getValor(op1)
		#valores
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		#compara
		if(valor1 == valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op2 es indirecto
	elif(op1 > 0 and op2 < 0):
		#valor
		valor1 = getValor(op1)
		#direccion
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 == valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#ambos son indirectos
	else:
		#direccion y valor
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		#direccion y valor
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 == valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")

#operador and
def And(op1,op2,result):
	if(op1 > 0 and op2 > 0):
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		if(valor1 == "true" and valor2 == "true"):
			setValor(result,"true")
		else:
			setValor(result,"false")
	elif(op1 < 0 and op2 > 0):
		dirNueva = getValor(op1)
		valor1 = getValor(dirNueva)
		valor2 = getValor(op2)
		if(valor1 == "true" and valor2 == "true"):
			setValor(result,"true")
		else:
			setValor(result,"false")
	elif(op1 > 0 and op2 < 0):
		dirNueva = getValor(op2)
		valor2 = getValor(dirNueva)
		valor1 = getValor(op1)
		if(valor1 == "true" and valor2 == "true"):
			setValor(result,"true")
		else:
			setValor(result,"false")
	else:
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		if(valor1 == "true" and valor2 == "true"):
			setValor(result,"true")
		else:
			setValor(result,"false")

#operador or
def Or(op1,op2,result):
	if(op1 > 0 and op2 > 0):
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		if(valor1 == "false" and valor2 == "false"):
			setValor(result,"false")
		else:
			setValor(result,"true")
	elif(op1 < 0 and op2 > 0):
		dirNueva = getValor(op1)
		valor1 = getValor(dirNueva)
		valor2 = getValor(op2)
		if(valor1 == "false" and valor2 == "false"):
			setValor(result,"false")
		else:
			setValor(result,"true")
	elif(op1 > 0 and op2 < 0):
		dirNueva = getValor(op2)
		valor2 = getValor(dirNueva)
		valor1 = getValor(op1)
		if(valor1 == "false" and valor2 == "false"):
			setValor(result,"false")
		else:
			setValor(result,"true")
	else:
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		if(valor1 == "false" and valor2 == "false"):
			setValor(result,"false")
		else:
			setValor(result,"true")

#compara dos valores con <= y retorna verdadero o falso
#verifica temporales indirectos
def MenorIgual(op1, op2, result):
	#no hay temporales indirectos
	if(op1 > 0 and op2 > 0):
		#valor
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		#compara y resuelve
		if(valor1 <= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op1 es indirecto
	elif(op1 < 0 and op2 > 0):
		#nueva direccion
		dirNueva1 = getValor(op1)
		#valores
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		#compara
		if(valor1 <= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op2 es indirecto
	elif(op1 > 0 and op2 < 0):
		#valor
		valor1 = getValor(op1)
		#direccion
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 <= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#ambos son indirectos
	else:
		#direccion y valor
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		#direccion y valor
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 <= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")

#compara dos valores con >= y retorna verdadero o falso
#verifica temporales indirectos
def MayorIgual(op1, op2, result):
	#no hay temporales indirectos
	if(op1 > 0 and op2 > 0):
		#valor
		valor1 = getValor(op1)
		valor2 = getValor(op2)
		#compara y resuelve
		if(valor1 >= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op1 es indirecto
	elif(op1 < 0 and op2 > 0):
		#nueva direccion
		dirNueva1 = getValor(op1)
		#valores
		valor1 = getValor(dirNueva1)
		valor2 = getValor(op2)
		#compara
		if(valor1 >= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#si op2 es indirecto
	elif(op1 > 0 and op2 < 0):
		#valor
		valor1 = getValor(op1)
		#direccion
		dirNueva2 = getValor(op2)
		#valor
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 >= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")
	#ambos son indirectos
	else:
		#direccion y valor
		dirNueva1 = getValor(op1)
		valor1 = getValor(dirNueva1)
		#direccion y valor
		dirNueva2 = getValor(op2)
		valor2 = getValor(dirNueva2)
		#compara
		if(valor1 >= valor2):
			setValor(result,"true")
		else:
			setValor(result,"false")

#imprime
#verifica temporales indirectos
def Print(result):
	#no hay temporales indirectos
	if(result > 0):
		#toma el valor e imprime
		res = getValor(result)
		print(res)
	#temporal indirecto
	else:
		#nueva direccipon
		dirNueva = getValor(result)
		#saca el valor e imprime
		res = getValor(dirNueva)
		print(res)

#lee un valor de consola
def Read(op1):
	#lee valor
	valor = input("teclea un valor: ")
	#verifica si es int
	if((op1 > 4999 and op1 < 6000 ) or (op1 > 9999 and op1 < 11000)):
		try:
			#parsea a int
			val = int(valor)
			setValor(op1,val)
		#error
		except:
			raise errorEjecucion("Debes guardar una variable de tipo int")
	#verifica float
	elif((op1 > 5999 and op1 < 7000) or (op1 > 10999 and op1 < 12000)):
		try:
			val = float(valor)
			setValor(op1,val)
		except:
			raise errorEjecucion("Debes guardar una variable de tipo float")
	#verifica string
	elif((op1 > 6999 and op1 < 8000) or (op1 > 11999 and op1 < 13000)):
		try:
			val = string(valor)
			setValor(op1,val)
		except:
			raise errorEjecucion("Debes guardar una variable de tipo string")
	#verifica bool
	else:
		if(valor == "true" or valor == "false"):
			setValor(op1,valor)
		else:
			raise errorEjecucion("Debes guardar una variable de tipo boleana")

#goto
def Goto(op1):
	global InstruccionActual
	#modifica instrucción actual a la del operador -1
	InstruccionActual = op1 - 1

#goto en caso de ser falso
def GotoF(op1,result):
	global InstruccionActual
	#verifica si valor es falso
	operando1 = getValor(op1)
	if(operando1 == "false"):
		#nueva isntruccción actual
		InstruccionActual = result - 1

#expande registro de memoria
def Era(op1):
	global bFuncion
	global FuncionActiva, iPosArray
	global diccionarioMemTemporalLl, diccionarioMemLocal
	global arregloFunciones,numParametros,iContadorParametros
	#entra a una funcion
	bFuncion = True
	#crea memoria local y temporal
	diccionarioMemLocal.append({})
	diccionarioMemTemporalLl.append({})
	iContadorParametros = 0
	#obtiene indice de función
	#es para no tener que buscarlo siempre,optimiza
	for x in range(0,len(arregloFunciones)):
		if(op1 == arregloFunciones[x].getNombre()):
			iPosArray = x
			numParametros = len(arregloFunciones[x].getDirecciones())

#va a función
def Gosub(op1):
	global InstruccionActual, iSaveInstruccionActual, iPosArray,FuncionActiva
	#agrgea la isntrucción actual a la pila
	iSaveInstruccionActual.append(InstruccionActual + 1)
	#nueva instruccióna actual
	InstruccionActual = arregloFunciones[iPosArray].getStart() - 1

#parametros recibidos
def Param(op1,result):
	global FuncionActiva
	global iContadorParametros,numParametros
	#obtiene valor de op1
	iContadorParametros += 1
	valor = getValor(op1)
	#accede a siguiente memoria
	FuncionActiva+=1
	#guarda el valor en la memoria recién creada
	setValor(result,valor)
	if(iContadorParametros != numParametros):
		FuncionActiva -= 1


#verifica que el inidice de un arreglo este en el rango
def Ver(op1,op2,result):
	global i
	var = True
	#verifica que este en el rango
	valor1 = getValor(op1)
	if(valor1 >= op2):
		if(valor1 <= result):
			var = True
		else:
			var = False
	else:
		var = False
	#levanta una excepcion
	if(var == False):
		raise errorEjecucion("Índice no válido")
		i = False

#guarda la dirección base en el temporal
def SumVer(op1,op2,result):
	valor1 = getValor(op1)
	newKey = valor1+op2
	setValor(result,newKey)

#termina funcion
def Ret():
	global InstruccionActual, iSaveInstruccionActual
	global diccionarioMemLocal, diccionarioMemTemporalLl
	global FuncionActiva,bFuncion
	#saca la utlimo contador a la instrucción local
	sav = iSaveInstruccionActual.pop()
	InstruccionActual = sav - 1
	#elimina el era
	diccionarioMemLocal.pop(FuncionActiva-1)
	diccionarioMemTemporalLl.pop(FuncionActiva-1)
	#termina funcion
	bFuncion = False
	#resetea contadores
	FuncionActiva -= 1
	iPosArray = -2

#regresa un valor
def Return(op1):
	global InstruccionActual
	#almacena el valor en la dirección de la función
	dvm = arregloFunciones[iPosArray].getDirs()
	valor = getValor(op1)
	setValor(dvm,valor)

#doggy
def move():
	global arregloGraphics
	arregloGraphics.append("move()")

def checkwall():
	global arregloGraphics
	arregloGraphics.append("checkwall()")

def turnRight():
	global arregloGraphics
	arregloGraphics.append("turnRight()")

def turnLeft():
	global arregloGraphics
	arregloGraphics.append("turnLeft()")

def pickBeeper():
	global arregloGraphics
	arregloGraphics.append("pickBeeper()")

def putBeeper():
	global arregloGraphics
	arregloGraphics.append("putBeeper()")

#termina ejecución
def End():
	global i
	print("terminé ejecucion")
	i = False

#switch MV
def Operacion(arregloCuadruplos):
	global FuncionActiva
	op = arregloCuadruplos[0]
	op1 = arregloCuadruplos[1]
	op2 = arregloCuadruplos[2]
	res = arregloCuadruplos[3]
	if(op == 0):
		Suma(op1,op2,res)
	elif(op == 1):
		Resta(op1,op2,res)
	elif(op == 2):
		Multiplicacion(op1,op2,res)
	elif(op == 3):
		Division(op1,op2,res)
	elif(op == 4):
		MenorQue(op1,op2,res)
	elif(op == 5):
		MayorQue(op1,op2,res)
	elif(op == 6):
		Asignacion(op1,res)
	elif(op == 7):
		Diferente(op1,op2,res)
	elif(op == 8):
		IgualQue(op1,op2,res)
	elif(op == 9):
		And(op1,op2,res)
	elif(op == 10):
		Or(op1,op2,res)
	elif(op == 11):
		MenorIgual(op1,op2,res)
	elif(op == 12):
		MayorIgual(op1,op2,res)
	elif(op == 13):
		Print(op1)
	elif(op == 14):
		Read(op1)
	elif(op == 15):
		End()
	elif(op == 16):
		Goto(op1)
	elif(op == 17):
		GotoF(op1,res)
	elif(op == 18):
		Era(op1)
	elif(op == 19):
		Gosub(op1)
	elif(op == 20):
		Param(op1,res)
	elif(op == 21):
		Ver(op1,op2,res)
	elif(op == 22):
		Ret()
	elif(op == 23):
		Return(op1)
	elif(op == 24):
		move()
	elif(op == 25):
		checkwall()
	elif(op == 26):
		turnRight()
	elif(op == 27):
		turnLeft()
	elif(op == 28):
		pickBeeper()
	elif(op == 29):
		putBeeper()
	elif(op == 30):
		SumVer(op1,op2,res)

#funcion de memoria que retorna el valor almacenado en una direccion
def getValor(memoriaVirtual):
	global diccionarioMemGlobal, diccionarioMemLocal, diccionarioMemConstante
	global diccionarioMemTemporalGl, diccionarioMemTemporalLl
	global bFuncion, FuncionActiva
	#global
	if(memoriaVirtual > 4999 and memoriaVirtual < 9000):
		try:
			return diccionarioMemGlobal[memoriaVirtual]
		except:
			raise errorEjecucion("Valor no asignado")
	#local
	elif(memoriaVirtual > 9999 and memoriaVirtual < 14000):
		try:
			return diccionarioMemLocal[FuncionActiva-1][memoriaVirtual]
		except:
			raise errorEjecucion("Valor no asignado")
	#temporal
	elif((memoriaVirtual > 19999 and memoriaVirtual < 24000) or (memoriaVirtual > -24000 and memoriaVirtual < -19999)):
		if(bFuncion == 0):
			try:
				return diccionarioMemTemporalGl[memoriaVirtual]
			except:
				raise errorEjecucion("Valor no asignado")
		else:
			try:
				return diccionarioMemTemporalLl[FuncionActiva-1][memoriaVirtual]
			except:
				raise errorEjecucion("Valor no asignado")
	#constantes
	elif(memoriaVirtual > 29999 and memoriaVirtual < 34000):
		try:
			return diccionarioMemConstante[memoriaVirtual]
		except:
			raise errorEjecucion("Valor no asignado")

#funcion de memoria que asigna un valor a una direccion
def setValor(memoriaVirtual, valor):
	global diccionarioMemGlobal, diccionarioMemLocal, diccionarioMemConstante
	global diccionarioMemTemporalGl, diccionarioMemTemporalLl
	global bFuncion, FuncionActiva
	#global
	if(memoriaVirtual > 4999 and memoriaVirtual < 9000):
		diccionarioMemGlobal[memoriaVirtual] = valor
	#local
	elif(memoriaVirtual > 9999 and memoriaVirtual < 14000):
		diccionarioMemLocal[FuncionActiva-1][memoriaVirtual] = valor
	#temporal
	elif((memoriaVirtual > 19999 and memoriaVirtual < 24000) or (memoriaVirtual > -24000 and memoriaVirtual < -19999)):
		if(bFuncion == 0):
			diccionarioMemTemporalGl[memoriaVirtual] = valor
		else:
			diccionarioMemTemporalLl[FuncionActiva-1][memoriaVirtual] = valor
	#cte
	elif(memoriaVirtual > 29999 and memoriaVirtual < 34000):
		diccionarioMemConstante[memoriaVirtual] = valor

#escribe comandos para el grafico
def writeGraphicsFile():
	#genera obj de constantes
	#toma el valor de la constante y su dirección virtual
	filename = argv
	filename = "aplusGraphics.txt"
	target = open(filename, 'w')
	target.truncate()
	for x in range(0,len(arregloGraphics)):
		target.write(str(arregloGraphics[x]))
		target.write("\n")
	target.close()

#main
leeObj()
while (i == True):
	Operacion(arregloCuadruplos[InstruccionActual])
	InstruccionActual += 1
writeGraphicsFile()