import Pieces
import Helper

def get_position_in_direction(board, row, col, row_offset, col_offset):
	new_row = row+row_offset
	new_col = col+col_offset
	if row < 0 or row > board.rows-1 or col < 0 or col > board.cols-1:
		return None
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
		return None
	
	def get_all_pieces_of_side(self, is_white):
		pieces = []
		for row in self.grid:
			for piece in row:
				if piece == None or str(piece) == ".":
					continue
				if not piece.is_white == is_white:
					continue
				pieces.append(piece)
		
		return pieces
	
	def move_is_legal(self, move):

		piece_pos = self.get_position(move.piece)
		if piece_pos == None:
			print("Invalid position.")
			return False
		
		if piece_pos.row == move.row and piece_pos.col == move.col:
			print("Piece is moving to same position.")
			return False

		captured_piece = self.move(move.piece, move.row, move.col, True)

		if self.test_for_check(move.piece.is_white):
			
			self.undo_move(move.piece, piece_pos.row, piece_pos.col, move.row, move.col, captured_piece)
			return False

		self.undo_move(move.piece, piece_pos.row, piece_pos.col, move.row, move.col, captured_piece)
		return True

	def get_valid_moves(self, piece, testing_for_check = False):
		valid_moves = []
		if str(piece) == ".":
			return valid_moves

		for move in piece.get_moves():

			position = self.get_position(piece)
			if position == None:
				break
			
			position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
			if position == None:
				break

			spaces_traveled = 0

			while position.is_valid() and spaces_traveled < move.max_spaces: #in line of sight or capture
				
				captured_piece = self.get_piece(position.row, position.col)
				if not captured_piece == None and captured_piece.is_white == piece.is_white:
					break
				elif not captured_piece == None and not move.is_capture and not captured_piece.is_white == piece.is_white:
					break
				elif (not move.is_move) and captured_piece == None:
					break

				board_move = BoardMove(piece, position.row, position.col, captured_piece)
				if not testing_for_check and not self.move_is_legal(board_move):
					position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
					spaces_traveled += 1
					continue

				valid_moves.append(board_move)
				position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
				spaces_traveled += 1
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

	def get_all_valid_moves_of_side(self, is_white):
		pieces = self.get_all_pieces_of_side(is_white)
		valid_moves = []
		for piece in pieces:
			valid_moves += self.get_valid_moves(piece)
		return valid_moves

	def is_valid_move(self, piece, row, col):
		piece_pos = self.get_position(piece)
		if piece_pos == None:
			print("Invalid position.")
			return False
		
		if piece_pos.row == row and piece_pos.col == col:
			print("Piece is moving to same position.")
			return False

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
		print("Could not find king. ")
		return None
	
	def test_for_check(self, is_white):
		enemy_pieces = self.get_all_pieces_of_side(not is_white)
		for piece in enemy_pieces:
			if self.piece_is_checking_king(piece):
				return True
		
		return False
	
	def piece_is_checking_king(self, piece):
		if type(piece) == Pieces.King:
			return False
		
		king = self.find_king(not piece.is_white)
		moves = self.get_valid_moves(piece, True)
		for move in moves:
			if move.captured_piece == king:
				return True
		return False
	
	def update_pawn_double_move_requirement(self, pawn, row):
		starting_row = 1 if pawn.is_white else self.rows-2
		pawn.can_double_move = row == starting_row

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

	def move(self, piece, row, col, testing_for_check=False):
		#print("move: " + str(piece) + " to " + Helper.position_to_coordinate(row, col))

		piece_pos = self.get_position(piece)
		
		if type(piece) == Pieces.King and not piece.has_moved:
			piece.has_moved = True
			left_rook = self.get_piece(row, 0)
			right_rook = self.get_piece(row, self.rows-1)

			if col == 2:
				self.move(left_rook, row, col+1)
			elif col == 6:
				self.move(right_rook, row, col-1)

		if type(piece) == Pieces.Rook and not testing_for_check:
			self.update_rook_castling_requirement(piece, piece_pos.col)

		captured_piece = self.grid[row][col]
		self.grid[row][col] = piece
		self.grid[piece_pos.row][piece_pos.col] = self.create_blank_piece()

		self.update_space_castling_requirement(piece.is_white)

		if type(piece) == Pieces.Pawn:
			self.update_pawn_double_move_requirement(piece, row)
		
		return captured_piece
	
	def undo_move(self, piece, row_start, col_start, row_end, col_end, captured_piece):
		
		was_castled = type(piece) == Pieces.King and abs(col_start - col_end) > 1
		if was_castled:
			#reset king castle to normal - DO NOT PASS THROUGH MOVE FUNCTION so requirements are not set
			piece.has_moved = False
			'''
			if col_end == 2:
				print("undo left rook swap")
				left_rook = self.get_piece(row_end, col_end+1)
				print(str(left_rook))
				self.grid[row_end][col_end+1] = self.create_blank_piece()
				self.grid[row_end][0] = left_rook

				piece.left_castle_open = True
				piece.left_rook_moved = False

			elif col_end == 6:
				print("undo right rook swap")

				right_rook = self.get_piece(row_end, col_end-1)
				self.grid[row_end][col_end-1] = self.create_blank_piece()
				self.grid[row_end][0] = right_rook

				piece.right_castle_open = True
				piece.right_rook_moved = False
			'''

		self.grid[row_start][col_start] = piece
		self.grid[row_end][col_end] = captured_piece

		self.update_space_castling_requirement(piece.is_white)

		if type(piece) == Pieces.Pawn:
			self.update_pawn_double_move_requirement(piece, row_start)

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