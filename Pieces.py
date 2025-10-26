class Piece:
	def __init__(self, is_white, name):
		self.is_white = is_white
		self.name = name
		self.directional_moves = []
		self.offset_moves = []

	def get_direction(self):
		return 1 if self.is_white else -1
	
	def __str__(self):
		if self.is_white:
			return self.name
		return self.name.upper()

class DirectionalMove:
	def __init__(self, row_offset, col_offset, max_spaces, is_move, is_capture):
		self.row_offset = row_offset
		self.col_offset = col_offset
		self.max_spaces = max_spaces
		self.is_move = is_move
		self.is_capture = is_capture

class OffsetMove:
	def __init__(self, row_offset, col_offset, is_move, is_capture):
		self.row_offset = row_offset
		self.col_offset = col_offset
		self.move = is_move
		self.capture = is_capture

class Pawn(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "p")
		self.directional_moves.append(DirectionalMove(self.get_direction(), 0, 4, True, False))

		self.offset_moves.append(OffsetMove(self.get_direction(), -1, False, True))
		self.offset_moves.append(OffsetMove(self.get_direction(), 1, False, True))
		