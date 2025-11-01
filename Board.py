from colorama import Fore, Back
from enum import Enum
import Pieces
import Helper

def get_position_in_direction(board, row, col, row_offset, col_offset):
	new_row = row+row_offset
	new_col = col+col_offset
	if row < 0 or row > board.rows-1 or col < 0 or col > board.cols-1:
		return None
	return BoardPosition(new_row, new_col)

class BoardState(Enum):
	NO_CHECK = 0
	WHITE_IN_CHECK = 1
	BLACK_IN_CHECK = 2
	WHITE_IN_CHECKMATE = 3
	BLACK_IN_CHECKMATE = 4
	WHITE_IN_STALEMATE = 5
	BLACK_IN_STALEMATE = 6
	DRAW_INSUFFICIENT = 7

class Board:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols

		self.board_state = BoardState.NO_CHECK
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
	
		self.auto_promoted_piece = "q"
		self.can_auto_promote = False

	def get_tile_color(self, r, c):
		tile_num = r*9 + c
		return Back.BLACK if tile_num % 2 == 0 else Back.WHITE

	def get_bishop_is_light_squared(self, bishop):
		bishop_pos = self.get_position(bishop)
		tile_num = bishop_pos.row*9 + bishop_pos.col
		return tile_num % 2 == 1

	def print(self):
		for r in range(self.rows-1, -1, -1):
			string = Fore.RESET + Back.RESET
			for c in range(self.cols):
				string += " " + self.get_tile_color(r, c) + str(self.get_piece(r, c))
			string += Fore.RESET + " " + Back.RESET
			print(string)

	def update_board_state(self, is_white):
		
		white_in_check = self.test_for_check(True)
		black_in_check = self.test_for_check(False)
		white_has_moves = len(self.get_all_valid_moves_of_side(True)) > 0
		black_has_moves = len(self.get_all_valid_moves_of_side(False)) > 0
		
		if is_white and white_in_check and white_has_moves:
			self.board_state = BoardState.WHITE_IN_CHECK

		elif is_white and white_in_check and not white_has_moves:
			self.board_state = BoardState.WHITE_IN_CHECKMATE
		
		elif is_white and not white_in_check and not white_has_moves:
			self.board_state = BoardState.WHITE_IN_STALEMATE
		
		elif not is_white and black_in_check and black_has_moves:
			self.board_state = BoardState.BLACK_IN_CHECK

		elif not is_white and black_in_check and not black_has_moves:
			self.board_state = BoardState.BLACK_IN_CHECKMATE
		
		elif not is_white and not black_in_check and not black_has_moves:
			self.board_state = BoardState.BLACK_IN_STALEMATE
		
		elif self.is_drawn():
			self.board_state = BoardState.DRAW_INSUFFICIENT

		else:
			self.board_state = BoardState.NO_CHECK
		return

	def is_playable(self):
		match self.board_state:
			case BoardState.NO_CHECK | BoardState.WHITE_IN_CHECK | BoardState.BLACK_IN_CHECK:
				return True
			case BoardState.WHITE_IN_CHECKMATE | BoardState.BLACK_IN_CHECKMATE | BoardState.WHITE_IN_STALEMATE | BoardState.BLACK_IN_STALEMATE | BoardState.DRAW_INSUFFICIENT:
				return False
			case "_":
				return False

	def is_drawn(self):
		all_pieces = self.get_all_pieces_of_side(True) + self.get_all_pieces_of_side(False)

		white_light_squared_bishops = 0
		white_dark_squared_bishops = 0
		white_knights = 0
		black_light_squared_bishops = 0
		black_dark_squared_bishops = 0
		black_knights = 0

		for piece in all_pieces:
			if type(piece) == Pieces.Queen:
				return False
			
			if type(piece) == Pieces.Rook:
				return False
			
			if type(piece) == Pieces.Pawn:
				return False
			
			if type(piece) == Pieces.Knight:
				if piece.is_white:
					white_knights += 1
				else:
					black_knights += 1
				continue

			if type(piece) == Pieces.Bishop:
				if piece.is_white:
					if self.get_bishop_is_light_squared(piece):
						white_light_squared_bishops += 1
					else:
						white_dark_squared_bishops += 1
				else:
					if self.get_bishop_is_light_squared(piece):
						black_light_squared_bishops += 1
					else:
						black_dark_squared_bishops += 1
				continue

			#various combinations of pieces sufficient to checkmate
			if white_knights > 2 or black_knights > 2:
				return False
			if (white_light_squared_bishops > 0 and white_dark_squared_bishops > 0) or (black_light_squared_bishops > 0 and black_dark_squared_bishops > 0):
				return False
			if (white_light_squared_bishops + white_dark_squared_bishops > 0 and white_knights > 0) or (black_light_squared_bishops + black_dark_squared_bishops > 0 and black_knights > 0):
				return False

		return True

	def get_piece(self, row, col):
		if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
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
				if str(piece) == str(self.create_blank_piece()):
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
		if str(piece) == str(self.create_blank_piece()):
			return valid_moves

		for move in piece.get_moves():

			position = self.get_position(piece)
			if position == None:
				continue

			position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
			if position == None:
				continue

			spaces_traveled = 0

			while position.is_valid() and spaces_traveled < move.max_spaces: #in line of sight or capture
				
				captured_piece = self.get_piece(position.row, position.col)
				piece_is_none = str(captured_piece) == str(self.create_blank_piece())
				if not piece_is_none and captured_piece.is_white == piece.is_white:
					break
				elif not piece_is_none and not move.is_capture and not captured_piece.is_white == piece.is_white:
					break
				elif piece_is_none and not move.is_move:
					break

				board_move = BoardMove(piece, position.row, position.col, captured_piece)
				if not testing_for_check and not self.move_is_legal(board_move):
					position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
					spaces_traveled += 1
					
					#cannot move through check
					if type(piece) == Pieces.King:
						break
					continue

				valid_moves.append(board_move)
				position = get_position_in_direction(self, position.row, position.col, move.row_offset, move.col_offset)
				spaces_traveled += 1
				if not piece_is_none:
					break
		
		return valid_moves

	def print_valid_moves(self, piece):
		if str(piece) == str(self.create_blank_piece()):
			return
		
		grid = []
		for r in range(self.rows):
			row = []
			for c in range(self.cols):
				row.append(str(self.grid[r][c]))
			grid.append(row)

		for move in self.get_valid_moves(piece):
			move_symbol = Fore.RED + "*" if str(move.captured_piece) == str(self.create_blank_piece()) else Fore.RED + "!"
			grid[move.row][move.col] = move_symbol

		for r in range(self.rows-1, -1, -1):
			string = Fore.RESET + Back.RESET
			for c in range(self.cols):
				string += " " + self.get_tile_color(r, c) + str(grid[r][c])
			string += Fore.RESET + " " + Back.RESET
			print(string)

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
		
		king = self.find_king(not piece.is_white)
		moves = self.get_valid_moves(piece, True)
		for move in moves:
			if move.captured_piece == king:
				return True
		return False
	
	def is_pawn_double_move(self, pawn, row):
		return False
	
	def update_enpassant_requirement(self, pawn, row):
		return False

	def update_pawn_double_move_requirement(self, pawn, row):
		starting_row = 1 if pawn.is_white else self.rows-2
		pawn.can_double_move = row == starting_row

	def was_double_move(self, row_start, row_end):
		return abs(row_start-row_end) == 2

	def reset_en_passant(self, is_white):
		pieces = self.get_all_pieces_of_side(is_white)
		for piece in pieces:
			if not type(piece) == Pieces.Pawn:
				continue
			piece.can_capture_en_passant_left = False
			piece.can_capture_en_passant_right = False
			p = self.get_position(piece)

	def update_neighbors_en_passant(self, pawn):
		pawn_pos = self.get_position(pawn)

		piece_left = self.get_piece(pawn_pos.row, pawn_pos.col-1)
		piece_right = self.get_piece(pawn_pos.row, pawn_pos.col+1)
		if not piece_left == None and type(piece_left) == Pieces.Pawn:
			piece_left.can_capture_en_passant_right = True

		if not piece_right == None and type(piece_right) == Pieces.Pawn:
			piece_right.can_capture_en_passant_left = True

	def was_en_passant_move(self, captured_piece, col_start, col_end):
		if str(captured_piece) == " ":
			return False
		if col_start == col_end:
			return False
		return True

	def capture_en_passant(self, pawn, row, col):
		self.grid[row - pawn.get_direction()][col] = self.create_blank_piece()

	def update_castling_space_requirement(self, is_white):
		king_row = 0 if is_white else self.rows-1
		king = self.find_king(is_white)

		blank_piece = self.create_blank_piece()

		left_piece1_is_blank = str(self.get_piece(king_row, 1)) == str(blank_piece)
		left_piece2_is_blank = str(self.get_piece(king_row, 2)) == str(blank_piece)
		left_piece3_is_blank = str(self.get_piece(king_row, 3)) == str(blank_piece)

		right_piece1_is_blank = str(self.get_piece(king_row, 5)) == str(blank_piece)
		right_piece2_is_blank = str(self.get_piece(king_row, 6)) == str(blank_piece)

		king.left_castle_open = left_piece1_is_blank and left_piece2_is_blank and left_piece3_is_blank
		king.right_castle_open = right_piece1_is_blank and right_piece2_is_blank

	def update_rook_castling_requirement(self, rook, col):
		king = self.find_king(rook.is_white)

		if col == 0:
			king.left_rook_moved = True
		elif col == self.cols-1:
			king.right_rook_moved = True

	def promote(self, pawn):
		promotion_pieces = ["q", "r", "b", "n"]
		promoted_piece = None
		selected_promotion = self.auto_promoted_piece if self.can_auto_promote else ""

		while not selected_promotion in promotion_pieces:
			selected_promotion = input("promote your pawn(q/r/b/n): ")
		
		match selected_promotion:
			case "q":
				promoted_piece = Pieces.Queen(pawn.is_white)
			case "r":
				promoted_piece = Pieces.Rook(pawn.is_white)
			case "b":
				promoted_piece = Pieces.Bishop(pawn.is_white)
			case "n":
				promoted_piece = Pieces.Knight(pawn.is_white)

		pawn_pos = self.get_position(pawn)

		self.grid[pawn_pos.row][pawn_pos.col] = promoted_piece

		self.update_board_state(not promoted_piece.is_white)

	def castle_rook(self, king, row, col):
		king.has_moved = True
		left_rook = self.get_piece(row, 0)
		right_rook = self.get_piece(row, self.rows-1)

		if col == 2:
			self.move(left_rook, row, col+1)
		elif col == 6:
			self.move(right_rook, row, col-1)

	def move(self, piece, row, col, testing_for_check=False):
		#print("move: " + str(piece) + " to " + Helper.position_to_coordinate(row, col))

		piece_pos = self.get_position(piece)
		
		if type(piece) == Pieces.King and not piece.has_moved and not testing_for_check:
			self.castle_rook(piece, row, col)

		if type(piece) == Pieces.Rook and not testing_for_check:
			self.update_rook_castling_requirement(piece, piece_pos.col)

		captured_piece = self.grid[row][col]
		self.grid[row][col] = piece
		self.grid[piece_pos.row][piece_pos.col] = self.create_blank_piece()

		if testing_for_check:
			return captured_piece

		self.reset_en_passant(piece.is_white)
		if type(piece) == Pieces.Pawn:
			self.update_pawn_double_move_requirement(piece, row)

			if self.was_en_passant_move(captured_piece, piece_pos.col, col):
				self.capture_en_passant(piece, row, col)

			if self.was_double_move(piece_pos.row, row):
				self.update_neighbors_en_passant(piece)
			if row == (self.rows-1 if piece.is_white else 0):
				self.promote(piece)
		
		self.update_board_state(not piece.is_white)
		self.update_castling_space_requirement(piece.is_white)

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

		if type(piece) == Pieces.Pawn:
			self.update_pawn_double_move_requirement(piece, row_start)

	def play_human_readable_move(self, move):
		start_position = Helper.coordinate_to_position(move.coordinate1)
		piece = self.get_piece(start_position[0], start_position[1])

		move_position = Helper.coordinate_to_position(move.coordinate2)

		self.move(piece, move_position[0], move_position[1])

	def create_blank_piece(self):
		return Pieces.Piece(False, " ")
	
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