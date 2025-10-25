class Piece:
	def __init__(self, color, name):
		self.color = color
		self.name = name
		self.directional_moves = []
		self.offset_moves = []

	def get_color_direction(self):
		return 1 if self.color else -1
	
	def __str__(self):
		if self.color:
			return self.name
		return self.name.upper()

class DirectionalMove:
	def __init__(self, x, y, x_max, y_max, move, capture):
		self.x = x
		self.y = y
		self.x_max = x_max
		self.y_max = y_max
		self.move = move
		self.capture = capture

class OffsetMove:
	def __init(self, x, y, move, capture):
		self.x = x
		self.y = y
		self.move = move
		self.capture = capture

class Pawn(Piece):
	def __init__(self, color):
		Piece.__init__(self, color, "p")
		self.directional_moves.append(DirectionalMove(0, self.get_color_direction(), 0, self.get_color_direction(), True, False))
		self.directional_moves.append(DirectionalMove(-1, self.get_color_direction(), -1, self.get_color_direction(), False, True))
		self.directional_moves.append(DirectionalMove(1, self.get_color_direction(), 1, self.get_color_direction(), False, True))