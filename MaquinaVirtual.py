#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Adriana Valenzuela a01195331
#Mayra Ruiz a00812918

from tablaFunciones import tablaFunciones

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
				word = word[1:]
				word = word[:-1]
				if(word != ""):
					listaParam.append(int(word))
				else:
					listaParam.append(-2)
			iContadorAux += 1
		#agrega la función al arreglo de funciones
		arregloFunciones.append(tablaFunciones(nombre,tipoFunc,-2,listaParam,inicioCuadruplo,dvm))

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

def Read(op1):
	valor = input("teclea un valor: ")
	setValor(op1,valor)

def Goto(op1):
	global InstruccionActual
	InstruccionActual = op1 - 1

def GotoF(op1,result):
	global InstruccionActual
	operando1 = getValor(op1)
	if(operando1 == "false"):
		InstruccionActual = result - 1

def Era(op1):
	global bFuncion
	global FuncionActiva, iPosArray
	global diccionarioMemTemporalLl, diccionarioMemLocal
	global arregloFunciones
	#entra a una funcion
	bFuncion = True
	diccionarioMemLocal.append({})
	diccionarioMemTemporalLl.append({})
	for x in range(0,len(arregloFunciones)):
		if(op1 == arregloFunciones[x].getNombre()):
			iPosArray = x

def Gosub(op1):
	global InstruccionActual, iSaveInstruccionActual, iPosArray,FuncionActiva
	iSaveInstruccionActual.append(InstruccionActual + 1)
	InstruccionActual = arregloFunciones[iPosArray].getStart() - 1

def Param(op1,result):
	global FuncionActiva
	valor = getValor(op1)
	FuncionActiva+=1
	setValor(result,valor)

def Ver(op1,op2,result):
	global i
	var = True
	valor1 = getValor(op1)
	if(valor1 >= op2):
		if(valor1 <= result):
			var = True
		else:
			var = False
	else:
		var = False
	if(var == False):
		print("error de indexación")
		i = False

def SumVer(op1,op2,result):
	valor1 = getValor(op1)
	newKey = valor1+op2
	setValor(result,valor1)

def Ret():
	global InstruccionActual, iSaveInstruccionActual
	global diccionarioMemLocal, diccionarioMemTemporalLl
	global FuncionActiva,bFuncion
	sav = iSaveInstruccionActual.pop()
	InstruccionActual = sav - 1
	diccionarioMemLocal.pop(FuncionActiva-1)
	diccionarioMemTemporalLl.pop(FuncionActiva-1)
	bFuncion = False
	FuncionActiva -= 1
	iPosArray = -2

def Return(op1):
	dvm = arregloFunciones[iPosArray].getDirs()
	valor = getValor(op1)
	setValor(dvm,valor)

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

def End():
	global i
	print("terminé ejecucion")
	i = False

#switch MV
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
	elif(op == 30):
		SumVer(op1,op2,res)


#funcion de memoria que retorna el valor almacenado en una direccion
def getValor(memoriaVirtual):
	global diccionarioMemGlobal, diccionarioMemLocal, diccionarioMemConstante
	global diccionarioMemTemporalGl, diccionarioMemTemporalLl
	global bFuncion, FuncionActiva
	#global
	if(memoriaVirtual > 4999 and memoriaVirtual < 9000):
		return diccionarioMemGlobal[memoriaVirtual]
	#local
	elif(memoriaVirtual > 9999 and memoriaVirtual < 14000):
		return diccionarioMemLocal[FuncionActiva-1][memoriaVirtual]
	#temporal
	elif(memoriaVirtual > 19999 and memoriaVirtual < 24000):
		if(bFuncion == 0):
			return diccionarioMemTemporalGl[memoriaVirtual]
		else:
			return diccionarioMemTemporalLl[FuncionActiva-1][memoriaVirtual]
	#constantes
	elif(memoriaVirtual > 29999 and memoriaVirtual < 34000):
		return diccionarioMemConstante[memoriaVirtual]

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
	elif(memoriaVirtual > 19999 and memoriaVirtual < 24000):
		if(bFuncion == 0):
			diccionarioMemTemporalGl[memoriaVirtual] = valor
		else:
			diccionarioMemTemporalLl[FuncionActiva-1][memoriaVirtual] = valor
	#cte
	elif(memoriaVirtual > 29999 and memoriaVirtual < 34000):
		diccionarioMemConstante[memoriaVirtual] = valor

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