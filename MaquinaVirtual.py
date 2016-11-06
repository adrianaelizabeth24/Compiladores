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
operador = -2
operando1 = -2
operando2 = -2
resultado = -2
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

#dicOperadores = {"+" : 0, "-" : 1, "*" : 2, "/" : 3, "<" : 4, ">": 5, "=" : 6,"<>" : 7, "==" : 8, "&": 9, "|": 10, "print" : 11}


def Suma(op1,op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 + valor2
	setValor(resultado, res)
	print(res)

def Resta(op1,op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 - valor2
	setValor(resultado, res)
	print(res)

def Multiplicacion(op1,op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 * valor2
	setValor(resultado, res)
	print(res)

def Division(op1,op2, result):
	valor1 = getValor(op1)
	valor2 = getValor(op2)
	res = valor1 / valor2
	setValor(resultado, res)
	print(res)

def Print(result):
	res = getValor(result)
	print(res)

def Operacion(op,op1,op2,res):
	if(op == 0):
		Suma(op1,op2,res)
	elif(op == 1):
		Resta(op1,op2,res)
	elif(op == 2):
		Multiplicacion(op1,op2,res)
	elif(op == 3):
		Division(op1,op2,res)
	elif(op == 11):
		Print(res)

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





