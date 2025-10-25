import Helper
import Board

myBoard = Board.Board(8, 8)
myBoard.print()

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
	print(Helper.coordinate_to_position(coordinate))
