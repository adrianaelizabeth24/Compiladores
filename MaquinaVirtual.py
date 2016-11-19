#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Adriana Valenzuela a01195331
#Mayra Ruiz a00812918

from tablaFunciones import tablaFunciones

#variables globales
diccionarioMemGlobal = {}
diccionarioMemTemporalGl = {}
diccionarioMemConstante = {}
diccionarioMemLocal = [{}]
diccionarioMemTemporalLl = [{}]
arregloCuadruplos = []
arregloFunciones = []
InstruccionActual = 0
FuncionActiva = 0
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

def leeObj():
	leeFunciones()
	leeConstantes()
	leeCuadruplos()

def leeFunciones():
	global arregloFunciones
	nombre = ""
	tipoFunc = ""
	listaParam = []
	inicioCuadruplo = 0
	f = open('aplusOBJFunciones.txt','r')
	for line in f:
		iContadorAux = 0
		for word in line.split():
			if(iContadorAux == 0):
				nombre = word
			elif(iContadorAux == 1):
				tipoFunc = word
			elif(iContadorAux == 2):
				word = word[1:]
				word = word[:-1]
				listaParam.extend(word)
			else:
				inicioCuadruplo = int(word)
			iContadorAux += 1
		arregloFunciones.append(tablaFunciones(nombre,tipoFunc,listaParam,inicioCuadruplo))
	for x in range(0,len(arregloFunciones)):
		print(arregloFunciones[x].getNombre())
		print(arregloFunciones[x].getTipo())
		print(arregloFunciones[x].getParametros())
		print(arregloFunciones[x].getStart())

def leeConstantes():
	global diccionarioMemConstante
	key = 0
	value = 0
	f = open('aplusOBJConstantes.txt', 'r')
	for line in f:
		iContadorAux = 0
		for word in line.split():
			if(iContadorAux == 0):
				key = int(word)
			else:
				if(key < 31000):
					value = int(word)
				elif(key > 30999 and key < 32000):
					value = float(word)
				else:
					if(iContadorAux == 1):
						value = word
					else:
						value = str(value) + " " + word
			iContadorAux+=1
		diccionarioMemConstante[key] = value

def leeCuadruplos():
	global arregloCuadruplos
	op = 0
	op1 = 0
	op2 = 0
	res = 0
	f = open('aplusOBJCuadruplos.txt', 'r')
	for line in f:
		iContadorAux = 0
		for word in line.split():
			if(iContadorAux == 0):
				op = int(word)
			elif(iContadorAux == 1):
				if(word == "nul"):
					op1 = -2
				else:
					op1 = int(word)
			elif(iContadorAux == 2):
				if(word == "nul"):
					op2 = -2
				else:
					op2 = int(word)
			else:
				if(word == "nul"):
					res = -2
				else:
					res = int(word)
			iContadorAux+=1
		arregloCuadruplos.append([op,op1,op2,res])

#funcion para sumar dos operandos
def Suma(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 + valor2
	setValor(result, res)

#funcion para restar dos operandos
def Resta(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 - valor2
	setValor(result, res)

#funcion para multiplicar dos operandos
def Multiplicacion(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 * valor2
	setValor(result, res)

#funcion para dividir dos operandos
def Division(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 / valor2
	setValor(result, res)

#compara dos valores y retorna verdadero o falso
#de acuerdo a los operadores
def MenorQue(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	if(valor1 < valor2):
		setValor(result,"true")
	else:
		setValor(result,"false")

def MayorQue(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	if(valor1 > valor2):
		setValor(result,"true")
	else:
		setValor(result,"false")

def Asignacion(op1,result):
	valor = getValor(op1)
	setValor(result,valor)

def Diferente(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	if(valor1 != valor2):
		setValor(result,"true")
	else:
		setValor(result,"false")

def IgualQue(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	if(valor1 == valor2):
		setValor(result,"true")
	else:
		setValor(result,"false")

def MenorIgual(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	if(valor1 <= valor2):
		setValor(result,"true")
	else:
		setValor(result,"false")

def MayorIgual(op1, op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	if(valor1 >= valor2):
		setValor(result,"true")
	else:
		setValor(result,"false")

def Print(result):
	res = getValor(result)
	print(res)

def Read():
	#
	print("un read")

def Goto(op1):
	global InstruccionActual
	InstruccionActual = op1 - 1

def GotoF(op1,result):
	global InstruccionActual
	operando1 = getValor(op1)
	if(operando1 == "false"):
		InstruccionActual = result - 1

def Era():
	print("era")

def Gosub():
	print("gosub")

def Param():
	print("param")

def Ver():
	print("ver")

def Ret():
	print("ret")

def Return():
	print("return")

def move():
	print("move")

def checkwall():
	print("checkwall")

def turnRight():
	print("turnrigjy")

def turnLeft():
	print("turnleft")

def pickBeeper():
	print("pickbeeper")

def putBeeper():
	print("putbeep")

def End():
	global i
	print("terminé ejecucion")
	i = False

def Operacion(arregloCuadruplos):
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

def getValor(memoriaVirtual):
	if(memoriaVirtual > 4999 and memoriaVirtual < 9000):
		return diccionarioMemGlobal[memoriaVirtual]
	elif(memoriaVirtual > 9999 and memoriaVirtual < 14000):
		return diccionarioMemLocal[memoriaVirtual]
	elif(memoriaVirtual > 19999 and memoriaVirtual < 24000):
		return diccionarioMemTemporalGl[memoriaVirtual]
	elif(memoriaVirtual > 29999 and memoriaVirtual < 34000):
		return diccionarioMemConstante[memoriaVirtual]

def setValor(memoriaVirtual, valor):
	if(memoriaVirtual > 4999 and memoriaVirtual < 9000):
		diccionarioMemGlobal[memoriaVirtual] = valor
	elif(memoriaVirtual > 9999 and memoriaVirtual < 14000):
		diccionarioMemLocal[memoriaVirtual] = valor
	elif(memoriaVirtual > 19999 and memoriaVirtual < 24000):
		diccionarioMemTemporalGl[memoriaVirtual] = valor
	elif(memoriaVirtual > 29999 and memoriaVirtual < 34000):
		diccionarioMemConstante[memoriaVirtual] = valor


leeObj()
while (i == True):
	Operacion(arregloCuadruplos[InstruccionActual])
	InstruccionActual += 1
