import Pieces

def get_position_in_direction(board, row, col, row_offset, col_offset):
	new_row = row+row_offset
	new_col = col+col_offset
	if row < 0 or row > board.rows-1 or col < 0 or col > board.cols-1:
		return BoardPosition(-1, -1)
	return BoardPosition(new_row, new_col)

class Board:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols

		self.grid = []
		for r in range(self.rows):
			row = []
			for c in range(self.cols):
				if r == 1:
					row.append(Pieces.Pawn(True))
				elif r == 6:
					row.append(Pieces.Pawn(False))
				else:
					row.append(self.create_blank_piece())
			self.grid.append(row)
	
	def print(self):
		print(" v"*8)
		for i in range(self.rows, 0, -1):
			row = self.grid[i-1]
			string = "-"
			connector = " "
			string = string + connector.join(str(piece) for piece in row) + "-"
			print(string)

		print(" ^"*8)

	def get_piece(self, row, col):
		if str(self.grid[row][col]) == ".":
			return None
		return self.grid[row][col]

	def get_position(self, piece):
		for r in range(self.rows):
			for c in range(self.cols):
				if self.grid[r][c] == piece:
					return BoardPosition(r, c)
		return BoardPosition(-1, -1)

	def get_valid_moves(self, piece):
		valid_moves = []
		if str(piece) == ".":
			return valid_moves

		for move in piece.directional_moves:

			position = self.get_position(piece)
			position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
			spaces_traveled = 0

			while position.is_valid() and spaces_traveled < move.max_spaces: #in line of sight or capture
				
				captured_piece = None
				valid_moves.append(BoardMove(piece, position.row, position.col, captured_piece))
				spaces_traveled += 1
				
				position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
		
		return valid_moves

	def print_valid_moves(self, piece):
		grid = []
		for r in range(self.rows):
			row = []
			for c in range(self.cols):
				row.append(".")
			grid.append(row)

		for move in self.get_valid_moves(piece):
			move_symbol = "o" if move.captured_piece == None else "X"
			grid[move.row][move.col] = move_symbol

			print(" v"*8)
		for i in range(self.rows, 0, -1):
			row = grid[i-1]
			string = "-"
			connector = " "
			string = string + connector.join(row) + "-"
			print(string)

		print(" ^"*8)

	def is_valid_move(self, piece, row, col):
		valid_moves = self.get_valid_moves(piece)
		for move in valid_moves:
			if move.row == row and move.col == col:
				return True
		return False

	def move(self, piece, row, col):
		piece_pos = self.get_position(piece)
		self.grid[row][col] = piece
		self.grid[piece_pos.row][piece_pos.col] = self.create_blank_piece()
		pass

	def create_blank_piece(self):
		return Pieces.Piece(False, ".")
	
class BoardMove:
	def __init__(self, piece, row, col, captured_piece=None):
		self.piece = piece
		self.row = row
		self.col = col
		self.captured_piece = captured_piece

letters =["a", "b", "c", "d", "e", "f", "g", "h"]
class BoardPosition:
	def __init__(self, row, col):
		self.row = row
		self.col = col

	def __str__(self):
		return "BoardPosition " + letters[self.col] + str(self.row+1)
	
	def is_valid(self):
		return not self.row == -1 and not self.col == -1