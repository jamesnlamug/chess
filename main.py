import Helper
import Board

my_board = Board.Board(8, 8)
my_board.print()

while True:
	player_input = input("[select, move]: ")
	if not Helper.input_is_valid(player_input):
		continue

	command = player_input.split()[0]
	coordinate = player_input.split()[1]
	if not Helper.command_is_valid(command) or not Helper.coordinate_is_valid(coordinate):
		continue

	print(command)
	print(coordinate)
	coordinate_as_list = Helper.coordinate_to_position(coordinate)
	my_board.get_valid_moves(my_board.get_piece(coordinate_as_list[0], coordinate_as_list[1]))