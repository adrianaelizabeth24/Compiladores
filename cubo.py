class Cubo(object):
	def __init__():
		int cubo[4][4][15] 
		'''Cubo [OP1][OP2][OPERACION] = TIPO
		
		OP

		INT 		0
		FLOAT		1
		STRING		2
		BOOL		3
		ERROR		-1

		OPERADOR
		+			0
		-			1
		*			2
		/			3
		<			4
		>			5
		=			6
		<>			7
		==			8
		&			9
		|			10

		'''

		# INT
		cubo[0][0][0] = 0 		# int + int = int
		cubo[0][1][0] = 1 		# int + float = float
		cubo[0][2][0] = -1 		# int + string = error
		cubo[0][3][0] = -1 		# int + bool = error

		cubo[0][0][1] = 0 		# int - int = int
		cubo[0][1][1] = 1 		# int - float = float
		cubo[0][2][1] = -1 		# int - string = error
		cubo[0][3][1] = -1 		# int - bool = error

		cubo[0][0][2] = 0 		# int * int = int
		cubo[0][1][2] = 1 		# int * float = float
		cubo[0][2][2] = -1 		# int * string = error
		cubo[0][3][2] = -1 		# int * bool = error

		cubo[0][0][3] = 1 		# int / int = int
		cubo[0][1][3] = 1 		# int / float = float
		cubo[0][2][3] = -1 		# int / string = error
		cubo[0][3][3] = -1 		# int / bool = error

		cubo[0][0][4] = 3 		# int < int = bool
		cubo[0][1][4] = 3 		# int < float = bool
		cubo[0][2][4] = -1 		# int < string = error
		cubo[0][3][4] = -1 		# int < bool = error

		cubo[0][0][5] = 3 		# int > int = bool
		cubo[0][1][5] = 3 		# int > float = bool
		cubo[0][2][5] = -1 		# int > string = error
		cubo[0][3][5] = -1 		# int > bool = error

		# ERRORRRR
		cubo[0][0][6] = -1 		# int = int = error
		cubo[0][1][6] = -1 		# int = float = error
		cubo[0][2][6] = -1 		# int = string = error
		cubo[0][3][6] = -1 		# int = bool = error

		cubo[0][0][7] = 3 		# int <> int = bool
		cubo[0][1][7] = 3 		# int <> float = bool
		cubo[0][2][7] = -1 		# int <> string = error
		cubo[0][3][7] = -1 		# int <> bool = error

		cubo[0][0][8] = 3 		# int == int = bool
		cubo[0][1][8] = 3 		# int == float = bool
		cubo[0][2][8] = -1 		# int == string = error
		cubo[0][3][8] = -1 		# int == bool = error

		cubo[0][0][9] = -1 		# int & int = error
		cubo[0][1][9] = -1 		# int & float = error
		cubo[0][2][9] = -1 		# int & string = error
		cubo[0][3][9] = -1 		# int & bool = error

		cubo[0][0][10] = -1 		# int | int = error
		cubo[0][1][10] = -1 		# int | float = error
		cubo[0][2][10] = -1 		# int | string = error
		cubo[0][3][10] = -1 		# int | bool = error

		# FLOAT

		cubo[1][0][0] = 1 		# float + int = float
		cubo[1][1][0] = 1 		# float + float = float
		cubo[1][2][0] = -1 		# float + string = error
		cubo[1][3][0] = -1 		# float + bool = error

		cubo[1][0][1] = 1 		# float - int = float
		cubo[1][1][1] = 1 		# float - float = float
		cubo[1][2][1] = -1 		# float - string = error
		cubo[1][3][1] = -1 		# float - bool = error

		cubo[1][0][2] = 1 		# float * int = float
		cubo[1][1][2] = 1 		# float * float = float
		cubo[1][2][2] = -1 		# float * string = error
		cubo[1][3][2] = -1 		# float * bool = error

		cubo[1][0][3] = 1 		# float / int = float
		cubo[1][1][3] = 1 		# float / float = float
		cubo[1][2][3] = -1 		# float / string = error
		cubo[1][3][3] = -1 		# float / bool = error

		cubo[1][0][4] = 3 		# float < int = bool
		cubo[1][1][4] = 3 		# float < float = bool
		cubo[1][2][4] = -1 		# float < string = error
		cubo[1][3][4] = -1 		# float < bool = error

		cubo[1][0][5] = 3 		# float > int = bool
		cubo[1][1][5] = 3 		# float > float = bool
		cubo[1][2][5] = -1 		# float > string = error
		cubo[1][3][5] = -1 		# float > bool = error

		# ERRORRRR
		cubo[1][0][6] = -1 		# float = int = error
		cubo[1][1][6] = -1 		# float = float = error
		cubo[1][2][6] = -1 		# float = string = error
		cubo[1][3][6] = -1 		# float = bool = error

		cubo[1][0][7] = 3 		# float <> int = bool
		cubo[1][1][7] = 3 		# float <> float = bool
		cubo[1][2][7] = -1 		# float <> string = error
		cubo[1][3][7] = -1 		# float <> bool = error

		cubo[1][0][8] = 3 		# float == int = bool
		cubo[1][1][8] = 3 		# float == float = bool
		cubo[1][2][8] = -1 		# float == string = error
		cubo[1][3][8] = -1 		# float == bool = error

		cubo[1][0][9] = -1 		# float & int = error
		cubo[1][1][9] = -1 		# float & float = error
		cubo[1][2][9] = -1 		# float & string = error
		cubo[1][3][9] = -1 		# float & bool = error

		cubo[1][0][10] = -1 		# float | int = error
		cubo[1][1][10] = -1 		# float | float = error
		cubo[1][2][10] = -1 		# float | string = error
		cubo[1][3][10] = -1 		# float | bool = error

		# STRING

		cubo[2][0][0] = -1 		# string + int = error
		cubo[2][1][0] = -1 		# string + float = error
		cubo[2][2][0] = -1 		# string + string = error
		cubo[2][3][0] = -1 		# string + bool = error

		cubo[2][0][1] = -1 		# string - int = error
		cubo[2][1][1] = -1 		# string - float = error
		cubo[2][2][1] = -1 		# string - string = error
		cubo[2][3][1] = -1 		# string - bool = error

		cubo[2][0][2] = -1 		# string * int = error
		cubo[2][1][2] = -1 		# string * float = error
		cubo[2][2][2] = -1 		# string * string = error
		cubo[2][3][2] = -1 		# string * bool = error

		cubo[2][0][3] = -1 		# string / int = error
		cubo[2][1][3] = -1 		# string / float = error
		cubo[2][2][3] = -1 		# string / string = error
		cubo[2][3][3] = -1 		# string / bool = error

		cubo[2][0][4] = -1 		# string < int = error
		cubo[2][1][4] = -1 		# string < float = error
		cubo[2][2][4] = 3 		# string < string = bool
		cubo[2][3][4] = -1 		# string < bool = error

		cubo[2][0][5] = -1 		# string > int = error
		cubo[2][1][5] = -1 		# string > float = error
		cubo[2][2][5] = 3 		# string > string = bool
		cubo[2][3][5] = -1 		# string > bool = error

		# ERRORRRR
		cubo[2][0][6] = -1 		# string = int = error
		cubo[2][1][6] = -1 		# string = float = error
		cubo[2][2][6] = -1 		# string = string = error
		cubo[2][3][6] = -1 		# string = bool = error

		cubo[2][0][7] = -1 		# string <> int = error
		cubo[2][1][7] = -1 		# string <> float = error
		cubo[2][2][7] = 3 		# string <> string = bool
		cubo[2][3][7] = -1 		# string <> bool = error

		cubo[2][0][8] = -1 		# string == int = error
		cubo[2][1][8] = -1 		# string == float = error
		cubo[2][2][8] = 3 		# string == string = bool
		cubo[2][3][8] = -1 		# string == bool = error

		cubo[2][0][9] = -1 		# string & int = error
		cubo[2][1][9] = -1 		# string & float = error
		cubo[2][2][9] = -1 		# string & string = error
		cubo[2][3][9] = -1 		# string & bool = error

		cubo[2][0][10] = -1 		# string | int = error
		cubo[2][1][10] = -1 		# string | float = error
		cubo[2][2][10] = -1 		# string | string = error
		cubo[2][3][10] = -1 		# string | bool = error

		# BOOL

		cubo[3][0][0] = -1 		# bool + int = error
		cubo[3][1][0] = -1 		# bool + float = error
		cubo[3][2][0] = -1 		# bool + string = error
		cubo[3][3][0] = -1 		# bool + bool = error

		cubo[3][0][1] = -1 		# bool - int = error
		cubo[3][1][1] = -1 		# bool - float = error
		cubo[3][2][1] = -1 		# bool - string = error
		cubo[3][3][1] = -1 		# bool - bool = error

		cubo[3][0][2] = -1 		# bool * int = error
		cubo[3][1][2] = -1 		# bool * float = error
		cubo[3][2][2] = -1 		# bool * string = error
		cubo[3][3][2] = -1 		# bool * bool = error

		cubo[3][0][3] = -1 		# bool / int = error
		cubo[3][1][3] = -1 		# bool / float = error
		cubo[3][2][3] = -1 		# bool / string = error
		cubo[3][3][3] = -1 		# bool / bool = error

		cubo[3][0][4] = -1 		# bool < int = error
		cubo[3][1][4] = -1 		# bool < float = error
		cubo[3][2][4] = -1 		# bool < string = error
		cubo[3][3][4] = -1 		# bool < bool = error

		cubo[3][0][5] = -1 		# bool > int = error
		cubo[3][1][5] = -1 		# bool > float = error
		cubo[3][2][5] = -1 		# bool > string = error
		cubo[3][3][5] = -1 		# bool > bool = error

		# ERRORRRR
		cubo[3][0][6] = -1 		# bool = int = error
		cubo[3][1][6] = -1 		# bool = float = error
		cubo[3][2][6] = -1 		# bool = string = error
		cubo[3][3][6] = -1 		# bool = bool = error

		cubo[3][0][7] = -1 		# bool <> int = error
		cubo[3][1][7] = -1 		# bool <> float = error
		cubo[3][2][7] = -1 		# bool <> string = error
		cubo[3][3][7] = 3 		# bool <> bool = bool

		cubo[3][0][8] = -1 		# bool == int = error
		cubo[3][1][8] = -1 		# bool == float = error
		cubo[3][2][8] = -1 		# bool == string = error
		cubo[3][3][8] = 3 		# bool == bool = bool

		cubo[3][0][9] = -1 		# bool & int = error
		cubo[3][1][9] = -1 		# bool & float = error
		cubo[3][2][9] = -1 		# bool & string = error
		cubo[3][3][9] = 3 		# bool & bool = bool

		cubo[3][0][10] = -1 		# bool | int = error
		cubo[3][1][10] = -1 		# bool | float = error
		cubo[3][2][10] = -1 		# bool | string = error
		cubo[3][3][10] = 3 		# bool | bool = bool
