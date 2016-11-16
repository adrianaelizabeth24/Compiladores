from tkinter import *
#import tkmessagebox
import tkinter as tk
import itertools as it
import aplus
import os
import subprocess

clickBefore = False
lineaX = 0
lineaY = 0
posDogX = 200
posDogY = 210

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

def compileCode():
    input = codeText.get("1.0",'end-1c')
    text_file = open("prueba.txt", "w")
    text_file.write(input)
    text_file.close()
    os.system('aplus.py')

    with open("output.txt", "w+") as output:
      subprocess.call(["python", "./MaquinaVirtual.py"], stdout=output);

    out_file = open("output.txt", "r")
    outText.delete("1.0", "end-1c")
    outText.insert(END, out_file.read())

def moveUp(event):
    global posDogY
    posDogY = posDogY - 50

def moveDown(event):
    global posDogY
    posDogY = posDogY + 50

def moveLeft(event):
    global posDogX
    posDogX = posDogX - 50

def moveRight(event):
    global posDogX
    posDogX = posDogX + 50

def onObjectClick(event):
    global clickBefore
    global lineaX
    global lineaY
    print('Got rec', event.x, event.y)
    if (clickBefore == False):
      lineaX = event.x
      lineaY = event.y
      clickBefore = True
    else:
      coord = lineaX, lineaY, event.x, event.y
      line = draw.create_line(coord, fill="black")
      clickBefore = False
      coord = 0, 0, 0, 0

'''Crear divisiones de pantallas'''
win = PanedWindow()
win.pack(fill= BOTH, expand=1)

left = PanedWindow(win, orient=VERTICAL)
win.add(left)


codeText = Text (left, height=30, width = 30)
codeText.insert(END, 'print("Hello, world")')
left.add(codeText)

bottom = Label(left)

B = tk.Button(bottom, text="Compile", command = compileCode)
B.pack()
left.add(bottom)

right = PanedWindow(win, orient=VERTICAL)
win.add(right)

draw = Canvas (right, width=550, height=300)
draw.pack()
right.add(draw)

outText = Text (right, height=2)
outText.insert(END, 'Hello, world')
right.add(outText)

'''
  Dibujar cuadricula
'''

x1 = 0
x2 = 13
y1 = 10
y2 = 23
for x in range (0, 8):
  x1 = 38
  x2 = 51
  for y in range (0, 15):
    draw.create_rectangle(x1,y1,x2,y2, fill="blue", tags="grid")
    x1 = x1 + 50
    x2 = x2 + 50

  y1 = y1 + 50
  y2 = y2 + 50

draw.tag_bind("grid", '<ButtonPress-1>', onObjectClick)
draw.tag_bind("dog", '<ButtonPress-1>', moveUp)

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

# milliseconds
delay = 150
animate()

win.mainloop()