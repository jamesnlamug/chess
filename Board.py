import Pieces
import Helper

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
				if r == 0:
					if c == 4:
						row.append(Pieces.King(True))
					if c == 3:
						row.append(Pieces.Queen(True))
					elif c == 0 or c == 7:
						row.append(Pieces.Rook(True))
					elif c == 1 or c == 6:
						row.append(Pieces.Knight(True))
					elif c == 2 or c == 5:
						row.append(Pieces.Bishop(True))
				elif r == 1:
					row.append(Pieces.Pawn(True))
				elif r == 7:
					if c == 4:
						row.append(Pieces.King(False))
					if c == 3:
						row.append(Pieces.Queen(False))
					elif c == 0 or c == 7:
						row.append(Pieces.Rook(False))
					elif c == 1 or c == 6:
						row.append(Pieces.Knight(False))
					elif c == 2 or c == 5:
						row.append(Pieces.Bishop(False))
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
	
	def get_all_pieces_of_side(self, is_white):
		pieces = []
		for row in self.grid:
			for piece in row:
				if str(piece) == ".":
					continue
				if not piece.is_white == is_white:
					continue
				pieces.append(piece)
		
		return pieces

	def get_valid_moves(self, piece):
		valid_moves = []
		if str(piece) == ".":
			return valid_moves

		for move in piece.get_moves():

			position = self.get_position(piece)
			position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
			spaces_traveled = 0

			while position.is_valid() and spaces_traveled < move.max_spaces: #in line of sight or capture
				
				captured_piece = self.get_piece(position.row, position.col)
				if not captured_piece == None and captured_piece.is_white == piece.is_white:
					break
				elif not captured_piece == None and not move.is_capture and not captured_piece.is_white == piece.is_white:
					break
				elif (not move.is_move) and captured_piece == None:
					break

				valid_moves.append(BoardMove(piece, position.row, position.col, captured_piece))
				spaces_traveled += 1
				
				position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
				if not captured_piece == None:
					break
		
		return valid_moves

	def print_valid_moves(self, piece):
		if piece == None or str(piece) == ".":
			return
		
		grid = []
		for r in range(self.rows):
			row = []
			for c in range(self.cols):
				row.append(str(self.grid[r][c]))
			grid.append(row)

		for move in self.get_valid_moves(piece):
			move_symbol = "*" if move.captured_piece == None else "!"
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

	def find_king(self, is_white):
		for row in self.grid:
			for piece in row:
				if type(piece) == Pieces.King and piece.is_white == is_white:
					return piece
		return None

	def update_space_castling_requirement(self, is_white):
		king_row = 0 if is_white else self.rows-1
		king = self.find_king(is_white)

		king.left_castle_open = self.get_piece(king_row, 1) == None and self.get_piece(king_row, 2) == None and self.get_piece(king_row, 3) == None
		king.right_castle_open = self.get_piece(king_row, 5) == None and self.get_piece(king_row, 6) == None

	def update_rook_castling_requirement(self, rook, col):
		king = self.find_king(rook.is_white)

		if col == 0:
			king.left_rook_moved = True
		elif col == self.cols-1:
			king.right_rook_moved = True

	def move(self, piece, row, col):
		piece_pos = self.get_position(piece)
		if type(piece) == Pieces.King and not piece.has_moved:
			piece.has_moved = True
			if col == 2:
				self.move(self.get_piece(0, 0), row, col+1)
			elif col == 6:
				self.move(self.get_piece(0, self.rows-1), row, col-1)

		if type(piece) == Pieces.Rook:
			self.update_rook_castling_requirement(piece, piece_pos.col)

		self.grid[row][col] = piece
		self.grid[piece_pos.row][piece_pos.col] = self.create_blank_piece()

		self.update_space_castling_requirement(piece.is_white)

		if type(piece) == Pieces.Pawn:
			piece.can_double_move = False

	def play_human_readable_move(self, move):
		start_position = Helper.coordinate_to_position(move.coordinate1)
		piece = self.get_piece(start_position[0], start_position[1])

		move_position = Helper.coordinate_to_position(move.coordinate2)

		self.move(piece, move_position[0], move_position[1])

	def create_blank_piece(self):
		return Pieces.Piece(False, ".")
	
class BoardMove:
	def __init__(self, piece, row, col, captured_piece=None):
		self.piece = piece
		self.row = row
		self.col = col
		self.captured_piece = captured_piece

	def __str__(self):
		return "BoardMove " + str(self.piece) + str(self.row) + ", " + str(self.col)

class HumanReadableMove:
	def __init__(self, coordinate1, coordinate2):
		self.coordinate1 = coordinate1
		self.coordinate2 = coordinate2

letters =["a", "b", "c", "d", "e", "f", "g", "h"]
class BoardPosition:
	def __init__(self, row, col):
		self.row = row
		self.col = col

	def __str__(self):
		return "BoardPosition " + letters[self.col] + str(self.row+1)
	
	def is_valid(self):
		return not self.row < 0 and not self.row > 7 and not self.col < 0 and not self.col > 7