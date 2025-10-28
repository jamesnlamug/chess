import time
import random
import Helper
import Board
import testcases

def get_player_piece(board, is_white):
	player_input = input("select a piece(a1-h8): ")
	if not Helper.coordinate_is_valid(player_input):
		print("Cannot select piece - Invalid coordinate!")
		return None
	
	c_list = Helper.coordinate_to_position(player_input)
	c_row = c_list[0]
	c_col = c_list[1]
	
	if board.get_piece(c_row, c_col) == None:
		print("Cannot select piece - cannot select empty square!")
		return None

	if not board.get_piece(c_row, c_col).is_white == is_white:
		print("Cannot select piece - cannot select enemy pieces!")
		return None

	return board.get_piece(c_row, c_col)

def make_player_move(piece, board):
	if piece == None:
		print("Cannot move - No piece selected!")
		return False
	
	player_input = input("select a location to move to(a1-h8): ")
	if not Helper.coordinate_is_valid(player_input):
		print("Cannot move - Invalid coordinate!")
		return False
	
	c_list = Helper.coordinate_to_position(player_input)
	c_row = c_list[0]
	c_col = c_list[1]

	board.print()

	if not board.is_valid_move(piece, c_row, c_col):
		print("Cannot move - Invalid move!")
		return False

	board.move(piece, c_row, c_col)
	return True

def make_random_ai_move(board, is_white):
	print(my_board.board_state)
	valid_moves = board.get_all_valid_moves_of_side(is_white)

	if len(valid_moves) <= 0:
		return

	move = valid_moves[random.randint(0, len(valid_moves)-1)]
	board.move(move.piece, move.row, move.col)

	print("ai played " + move.piece.get_full_name() + " to " + Helper.position_to_coordinate(move.row, move.col))
	return

def run_moves(moves):
	for move in moves:
		my_board.play_human_readable_move(move)

def run_auto(auto_time):
	while True:
		time.sleep(auto_time)
		make_random_ai_move(my_board, True)
		#Helper.clear()
		my_board.print()
		

		time.sleep(auto_time)
		make_random_ai_move(my_board, False)
		#Helper.clear()
		my_board.print()

#main
my_board = Board.Board(8, 8)

game_running = True
player_is_white = True

test_case = testcases.white_can_scholars_mate
run_moves(test_case)

while my_board.is_playable():

	player_piece = None
	player_moved = False
	while not player_moved:
		print(my_board.board_state)
		my_board.print()
		player_piece = get_player_piece(my_board, player_is_white)
		
		if not player_piece == None:
			#Helper.clear()
			my_board.print_valid_moves(player_piece)

		player_moved = make_player_move(player_piece, my_board)
	
	#Helper.clear()
	make_random_ai_move(my_board, not player_is_white)

print("game over.")
print(my_board.board_state)

#run_auto(0.01)