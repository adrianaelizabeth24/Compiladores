from graphics import *

def main():
	x1 = 8
	x2 = 21
	y1 = 10
	y2 = 23

	win = GraphWin("Karel", 450, 350)
	win.setBackground(color_rgb(238, 238, 238));
	#c = Circle(Point(100,100), 6)
	#win.plotPixel(35, 128, "blue")


	'''
		Dibujar Cuadricula
	'''
	for x in range (0, 8):
		x1 = 38
		x2 = 51

		for y in range (0, 15):
			aRectangle = Rectangle(Point(x1,y1), Point(x2,y2))
			aRectangle.setFill(color_rgb(188,75,75))
			x1 = x1 + 30
			x2 = x2 + 30
			aRectangle.draw(win)

		y1 = y1 + 30
		y2 = y2 + 30


	#c.draw(win)

	win.getMouse() # pause for click in window
	win.close()

main()