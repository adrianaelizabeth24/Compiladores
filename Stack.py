#!/usr/bin/env python
# -*- coding: utf-8 -*-

#clase stack
class Stack:

       #función que define que un elemento es de tipo stack comienza con una lista vacía
       #por default las listas en phython se comportan como Stacks (lifo)
       # var = Stack() por definición
       def __init__(self):
               self.items = []
       #metodo que regresa verdadero o falso dependiendo de si la stack contiene elementos o no
       def isEmpty(self):
              if(len(self.items) == 0):
                     return 1
              else:
                     return 0

       #agrega el elemento "item" al final de la lista, utiliza el método ya existente de las listas append
       def push(self, item):
              self.items.append(item)

       #regresa el último elemento en ser insertado a la lista
       def pop(self):
              return self.items.pop()
       
       #regresa el tamaño de la stack utilizando el metodo len de las listas
       def size(self):
              return len(self.items)
       
       #regresa el elemento 0 de la lista
       def back(self):
              return self.items[0]
       
       #regresa el ultimo elemento de la lista se le conoce como el -1
       def peek(self):
               temp = self.items.pop()
               self.push(temp)
               return temp

       #imprime los elementos de la lista en orden en el que fueron insertados
       def printSelf(self):
              size = len(self.items)
              s = 0
              while s < size:
                     print(self.items[s], " ")
                     s+=1
