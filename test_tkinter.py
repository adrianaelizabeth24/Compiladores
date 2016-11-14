from tkinter import *
#import tkmessagebox
import tkinter as tk
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

def retrieve_input():
    input = CodeEntry.get("1.0",'end-1c')
    print(input)

# Crear barra de menu
win = Tk()
menubar = Menu(win)

CodeEntry = Text (win, height=10, width = 30)
CodeEntry.pack()
CodeEntry.insert(END, "hi")

# Seccion: File
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=win.quit)
menubar.add_cascade(label="File", menu=filemenu)

# Seccion: Edit
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)

# Seccion: Help
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

win.config(menu=menubar)
win.minsize(width=900, height=600)

'''
	Boton de menu
'''
mb=  Menubutton ( win, text="menu", relief=RAISED )
mb.grid()
mb.menu  =  Menu ( mb, tearoff = 0 )
mb["menu"]  =  mb.menu
    
mayoVar  = IntVar()
ketchVar = IntVar()

mb.menu.add_checkbutton ( label="cheap trills",
                          variable=mayoVar )
mb.menu.add_checkbutton ( label="hotline",
                          variable=ketchVar )
mb.pack()

'''
	Dibujar cuadricula
'''
draw = Canvas (win, width=550, height=500)
draw.pack()

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


# this list created with the PIL program
# it may be different in your case
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
retrieve_input()

#draw.create_rectangle(50,50,150,150, fill="blue")

win.mainloop()