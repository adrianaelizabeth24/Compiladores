from tkinter import *
import tkinter as tk
import itertools as it
import os
import subprocess
import random
import sys
from sys import argv
import time

clickBefore = False
lineaX = 0
lineaY = 0
posDogX = 200
posDogY = 210
gradDog = 1
posBoneX = 0
posBoneY = 0
runBefore = False

# every gif's frame
fname_list = \
['./image/frame_0_delay-0.1s.gif',
 './image/frame_1_delay-0.1s.gif',
 './image/frame_2_delay-0.1s.gif',
 './image/frame_3_delay-0.1s.gif',
 './image/frame_4_delay-0.1s.gif',
 './image/frame_5_delay-0.1s.gif',
 './image/frame_6_delay-0.1s.gif']

# store as tk img_objects
pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in fname_list)

def donothing():
   filewin = winlevel(win)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def animate():
    global posDogX
    global posDogY
    """ cycle through """
    img = next(pictures)
    draw.delete("dog")
    draw.create_image(posDogX, posDogY, anchor=NW, image=img, tags="dog")
    win.after(delay, animate)

def putBeeper():
    global posDogX
    global posDogY
    poop = tk.PhotoImage(file='./image/poop.gif')

    w = Label(draw, image=poop)
    w.poop = poop
    w.pack(side="left")
    draw.create_window(posDogX + 20, posDogY + 20, window=w)
    #valor = input("Dime stuffz: ")
    #print('Me dijiste: ' + valor)

def pickBeeper():
    global posBoneX
    global posBoneY
    global w2

    var = draw.find_overlapping(posDogX, posDogY, posDogX+50, posDogY+50)

    for item in var:
      if (draw.itemcget(item, "tags") == 'bone'):
        w2.destroy()
        print ("¡Recibiste un hueso!")
    

def drawBone():
    global posBoneX
    global posBoneY
    global w2

    #bone = tk.PhotoImage(file='./image/bone.gif')
    #w2 = Label(draw, image=bone)
    w2.bone = bone
    w2.pack()
    draw.create_window(posBoneX, posBoneY, window=w2, tags='bone')

def compileCode():
    input = codeText.get("1.0",'end-1c')
    text_file = open("prueba.txt", "w")
    text_file.write(input)
    text_file.close()
    subprocess.call(["python", "./aplus.py"]);

    with open("output.txt", "w+") as output:
      subprocess.call(["python", "./MaquinaVirtual.py"], stdout=output);

    out_file = open("output.txt", "r")
    outText.delete("1.0", "end-1c")
    outText.insert(END, out_file.read())

    with open('aplusGraphics.txt') as out:
      for line in out:
        if 'move()' in line:
          move()
        if 'turnLeft()' in line:
          turnLeft()
        if 'turnRight()' in line:
          turnRight()
        if 'pickBeeper()' in line:
          pickBeeper()
        if 'putBeeper()' in line:
          putBeeper()
        if 'checkwall()' in line:
          checkWall()
    '''if (runBefore == True): 
      reiniciar()
      runBefore = False
    else:
      runBefore = True'''


def moveUp():
    global posDogY
    posDogY = posDogY - 50

def moveDown():
    global posDogY
    posDogY = posDogY + 50

def moveLeft():
    global posDogX
    posDogX = posDogX - 50

def moveRight():
    global posDogX
    posDogX = posDogX + 50

def move():
    global gradDog

    if gradDog == 1:
      moveRight()
    elif gradDog == 2:
      moveDown()
    if gradDog == 3:
      moveLeft()
    elif gradDog == 0 or gradDog == 4:
      moveUp()

def turnLeft():
  global gradDog
  gradDog = gradDog - 1

  if gradDog == 0:
    gradDog = 4
  rotateDog()

def turnRight():
  global gradDog
  gradDog = gradDog + 1

  if gradDog == 5:
    gradDog = 1
  rotateDog()

def rotateDog():
    global gradDog
    global fname_list
    global pictures

    if gradDog == 1:
      #normal
      fname_list = \
        ['./image/frame_0_delay-0.1s.gif',
         './image/frame_1_delay-0.1s.gif',
        './image/frame_2_delay-0.1s.gif',
        './image/frame_3_delay-0.1s.gif',
        './image/frame_4_delay-0.1s.gif',
        './image/frame_5_delay-0.1s.gif',
        './image/frame_6_delay-0.1s.gif']
      pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in fname_list)
    elif gradDog == 2:
      #90grad
      fname_list = \
        ['./image/90grados/frame_0_delay-0.1s.gif',
         './image/90grados/frame_1_delay-0.1s.gif',
        './image/90grados/frame_2_delay-0.1s.gif',
        './image/90grados/frame_3_delay-0.1s.gif',
        './image/90grados/frame_4_delay-0.1s.gif',
        './image/90grados/frame_5_delay-0.1s.gif',
        './image/90grados/frame_6_delay-0.1s.gif']
      pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in fname_list)
    if gradDog == 3:
        #180 grad
        fname_list = \
        ['./image/180grados/frame_0_delay-0.1s.gif',
         './image/180grados/frame_1_delay-0.1s.gif',
        './image/180grados/frame_2_delay-0.1s.gif',
        './image/180grados/frame_3_delay-0.1s.gif',
        './image/180grados/frame_4_delay-0.1s.gif',
        './image/180grados/frame_5_delay-0.1s.gif',
        './image/180grados/frame_6_delay-0.1s.gif']
        pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in fname_list)
    elif gradDog == 4:
        # 270 grad
        fname_list = \
        ['./image/270grados/frame_0_delay-0.1s.gif',
         './image/270grados/frame_1_delay-0.1s.gif',
        './image/270grados/frame_2_delay-0.1s.gif',
        './image/270grados/frame_3_delay-0.1s.gif',
        './image/270grados/frame_4_delay-0.1s.gif',
        './image/270grados/frame_5_delay-0.1s.gif',
        './image/270grados/frame_6_delay-0.1s.gif']
        pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in fname_list)

def onObjectClick(event):
    global clickBefore
    global lineaX
    global lineaY
    #print('Got rec', event.x, event.y)
    if (clickBefore == False):
      lineaX = event.x
      lineaY = event.y
      clickBefore = True
    else:
      coord = lineaX, lineaY, event.x, event.y
      line = draw.create_line(coord, fill="black", tags="wall")
      clickBefore = False
      coord = 0, 0, 0, 0

def checkWall():
    global posDogX
    global posDogY

    var = draw.find_overlapping(posDogX, posDogY, posDogX+50, posDogY+50)

    for item in var:
      if (draw.itemcget(item, "tags") == 'wall'):
        print ("Hay un muro cercano")

def deleteAll(event):
    draw.delete("wall")

def reiniciar(event):
    global posDogX
    global posDogY
    global w2

    posDogX = 200
    posDogY = 210

    w2.destroy()

    randX = random.randint(0, 11)
    randY = random.randint(0, 7)

    posBoneX = 38 + (randX * 50) 
    posBoneY = 10 + (randY * 50)
    bone = tk.PhotoImage(file='./image/bone.gif')
    w2 = Label(draw, image=bone)
    drawBone()

    draw.delete("wall")

'''Crear divisiones de pantallas'''
win = PanedWindow()
win.pack(fill= BOTH, expand=1)

left = PanedWindow(win, orient=VERTICAL)
win.add(left)


codeText = Text (left, height=30, width = 30)
codeText.insert(END, 'main: print("Hello, world");')
left.add(codeText)

bottom = Label(left)

B = tk.Button(bottom, text="Compile", command = compileCode)
B.pack()
left.add(bottom)

right = PanedWindow(win, orient=VERTICAL)
win.add(right)

draw = Canvas (right, width=600, height=400)
draw.pack()
right.add(draw)

outText = Text (right, height=2)
outText.insert(END, 'Hello, world')
right.add(outText)

bone = tk.PhotoImage(file='./image/bone.gif')
w2 = Label(draw, image=bone)

'''
  Dibujar cuadricula
'''

randX = random.randint(0, 11)
randY = random.randint(0, 7)

posBoneX = 38 + (randX * 50) 
posBoneY = 10 + (randY * 50)

x1 = 0
x2 = 13
y1 = 10
y2 = 23
for x in range (0, 8):
  x1 = 38
  x2 = 51
  for y in range (0, 12):
    draw.create_rectangle(x1,y1,x2,y2, fill="blue", tags="grid")
    x1 = x1 + 50
    x2 = x2 + 50

  y1 = y1 + 50
  y2 = y2 + 50

drawBone()

draw.tag_bind("grid", '<ButtonPress-1>', onObjectClick)

draw.bind('<Double-Button-3>', reiniciar)

#draw.tag_bind("dog", '<ButtonPress-3>', turnLeft)
#draw.tag_bind("dog", '<ButtonPress-2>', pickBeeper)

# animation in 150 milliseconds
delay = 150
animate()



win.mainloop()