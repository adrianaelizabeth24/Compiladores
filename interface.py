from Tkinter import *
#import tkmessagebox
import Tkinter as tk
import itertools as it

def donothing():
   filewin = winlevel(win)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def animate():
    """ cycle through """
    img = next(pictures)
    draw.delete("dog")
    draw.create_image(200,210, anchor=NW, image=img, tags="dog")
    win.after(delay, animate)

def compileCode():
    input = codeText.get("1.0",'end-1c')
    print(input)

# Crear barra de menu
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

#draw = Canvas (right, width=550, height=300)
#draw.pack()


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
compileCode()



win.mainloop()