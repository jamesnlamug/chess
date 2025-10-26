class Piece:
	def __init__(self, is_white, name):
		self.is_white = is_white
		self.name = name
		self.moves = []

	def get_direction(self):
		return 1 if self.is_white else -1
	
	def get_moves(self):
		return self.moves

	def __str__(self):
		if self.is_white:
			return self.name
		return self.name.upper()
	
	def get_full_name(self):
		match self.name:
			case "k":
				return "king"
			case "q":
				return "queen"
			case "r":
				return "rook"
			case "b":
				return "bishop"
			case "n":
				return "knight"
			case "p":
				return "pawn"
			case "_":
				return "unknown"

class PieceMove:
	def __init__(self, row_offset, col_offset, max_spaces, is_move, is_capture, special_command = ""):
		self.row_offset = row_offset
		self.col_offset = col_offset
		self.max_spaces = max_spaces
		self.is_move = is_move
		self.is_capture = is_capture
		self.special_command = special_command

class Pawn(Piece):
	def __init__(self, is_white):
		Piece.__init__(self, is_white, "p")
		self.can_double_move = True

		#forward
		self.moves.append(PieceMove(self.get_direction(), 0, 1, True, False))

		#diagonal capture
		self.moves.append(PieceMove(self.get_direction(), -1, 1, False, True))
		self.moves.append(PieceMove(self.get_direction(), 1, 1, False, True))

	def get_moves(self):
		return self.moves + self.get_special_moves()
	
	def get_special_moves(self):
		special_moves = []
		if self.can_double_move:
			special_moves.append(PieceMove(self.get_direction(), 0, 2, True, False))
		return special_moves

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
		self.has_moved = False
		self.left_rook_moved = False
		self.left_castle_open = False
		self.right_rook_moved = False
		self.right_castle_open = False
		
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

	def get_moves(self):
		return self.moves + self.get_special_moves()
	
	def get_special_moves(self):
		special_moves = []
		if self.has_moved:
			return special_moves
		
		if not self.left_rook_moved and self.left_castle_open:
			special_moves.append(PieceMove(0, -2, 1, True, False, "swap-left-rook"))
		if not self.right_rook_moved and self.right_castle_open:
			special_moves.append(PieceMove(0, 2, 1, True, False, "swap-right-rook"))
		
		return special_moves

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