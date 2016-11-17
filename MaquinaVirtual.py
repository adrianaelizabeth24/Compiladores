#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Adriana Valenzuela a01195331
#Mayra Ruiz a00812918

#variables globales
diccionarioMemGlobal = {}
diccionarioMemLocal = {}
diccionarioMemTemporalGl = {}
diccionarioMemTemporalLl = {}
diccionarioMemConstante = {}
arregloCuadruplos = []
InstruccionActual = 0
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
#"<" : 4, ">": 5, "=" : 6,"<>" : 7, "==" : 8, 
#"&": 9, "|": 10, "<=": 11, ">=": 12, "print" : 13 , "read": 14, 
#"end": 15, "Goto": 16, "GotoF": 17}

def leeObj():
	leeConstantes()
	leeCuadruplos()

def leeConstantes():
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

def Goto(op1):
	global InstruccionActual
	InstruccionActual = op1 - 1

def GotoF(op1,result):
	global InstruccionActual
	operando1 = getValor(op1)
	if(operando1 == "false"):
		InstruccionActual = result - 1

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
	elif(op == 15):
		End()
	elif(op == 16):
		Goto(op1)
	elif(op == 17):
		GotoF(op1,res)



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
