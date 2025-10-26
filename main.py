import Helper
import Board

my_board = Board.Board(8, 8)
my_board.print()

selected_piece = None
while True:
	player_input = input("[select, move]: ")
	if not Helper.input_is_valid(player_input):
		continue

	command = player_input.split()[0]
	coordinate = player_input.split()[1]
	if not Helper.command_is_valid(command) or not Helper.coordinate_is_valid(coordinate):
		continue

	c_list = Helper.coordinate_to_position(coordinate)
	c_row = c_list[0]
	c_col = c_list[1]
	print(command + "-" + str(c_list))
	
	match command:
		case "select":
			selected_piece = my_board.get_piece(c_row, c_col)
			if selected_piece == None:
				print("Cannot select: No piece at that position!")
				continue
			my_board.print_valid_moves(selected_piece)

		case "move":
			if selected_piece == None:
				print("Cannot move: No piece selected!")
				continue
			if not my_board.is_valid_move(selected_piece, c_row, c_col):
				print("Cannot move: invalid move for this piece!")
				continue

			my_board.move(selected_piece, c_row, c_col)
			selected_piece = None
			my_board.print()

		case "_":
			continue