class Piece:
	def __init__(self, is_white, name):
		self.is_white = is_white
		self.name = name
		self.moves = []

	def get_direction(self):
		return 1 if self.is_white else -1
	
	def __str__(self):
		if self.is_white:
			return self.name
		return self.name.upper()

class PieceMove:
	def __init__(self, row_offset, col_offset, max_spaces, is_move, is_capture):
		self.row_offset = row_offset
		self.col_offset = col_offset
		self.max_spaces = max_spaces
		self.is_move = is_move
		self.is_capture = is_capture

class Pawn(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "p")
		self.is_on_starting_row = True

		#forward
		self.moves.append(PieceMove(self.get_direction(), 0, 2, True, False))

		#diagonal capture
		self.moves.append(PieceMove(self.get_direction(), -1, 1, False, True))
		self.moves.append(PieceMove(self.get_direction(), 1, 1, False, True))

class Queen(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "q")
		
		#orthogonal
		self.moves.append(PieceMove(1,  0, 7, True, True))
		self.moves.append(PieceMove(0, -1, 7, True, True))
		self.moves.append(PieceMove(-1, 0, 7, True, True))
		self.moves.append(PieceMove(0,  1, 7, True, True))

		#diagonal
		self.moves.append(PieceMove(1,  -1, 7, True, True))
		self.moves.append(PieceMove(1,   1, 7, True, True))
		self.moves.append(PieceMove(-1, -1, 7, True, True))
		self.moves.append(PieceMove(-1,  1, 7, True, True))

class Rook(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "r")
		
		#orthogonal
		self.moves.append(PieceMove(1,  0, 7, True, True))
		self.moves.append(PieceMove(0, -1, 7, True, True))
		self.moves.append(PieceMove(-1, 0, 7, True, True))
		self.moves.append(PieceMove(0,  1, 7, True, True))

class Bishop(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "b")
		
		#diagonal
		self.moves.append(PieceMove(1,  -1, 7, True, True))
		self.moves.append(PieceMove(1,   1, 7, True, True))
		self.moves.append(PieceMove(-1, -1, 7, True, True))
		self.moves.append(PieceMove(-1,  1, 7, True, True))

class King(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "k")
		
		#orthogonal
		self.moves.append(PieceMove(1,  0, 1, True, True))
		self.moves.append(PieceMove(0, -1, 1, True, True))
		self.moves.append(PieceMove(-1, 0, 1, True, True))
		self.moves.append(PieceMove(0,  1, 1, True, True))

		#diagonal
		self.moves.append(PieceMove(1,  -1, 1, True, True))
		self.moves.append(PieceMove(1,   1, 1, True, True))
		self.moves.append(PieceMove(-1, -1, 1, True, True))
		self.moves.append(PieceMove(-1,  1, 1, True, True))

class Knight(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "n")
		
		#2x1 moves
		self.moves.append(PieceMove(-2, -1, 1, True, True))
		self.moves.append(PieceMove(-2,  1, 1, True, True))
		self.moves.append(PieceMove(-1, -2, 1, True, True))
		self.moves.append(PieceMove(-1,  2, 1, True, True))
		self.moves.append(PieceMove(1,  -2, 1, True, True))
		self.moves.append(PieceMove(1,   2, 1, True, True))
		self.moves.append(PieceMove(2,  -1, 1, True, True))
		self.moves.append(PieceMove(2,   1, 1, True, True))