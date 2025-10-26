def input_is_valid(inp):
	if not type(inp) == str:
		return False
	
	if not len(inp.split()) == 2:
		return False
	
	return True

def command_is_valid(command):
	if not type(command) == str:
		return False
	
	command_list = ["select", "move"]
	if not command in command_list:
		return False
	
	return True

letter_columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
def coordinate_is_valid(coordinate):
	if not type(coordinate) == str:
		return False
	if len(coordinate) > 2:
		return False
	
	coordinate_col = coordinate[0:1].lower()

	if not coordinate_col in letter_columns:
		return False
	
	try:
		coordinate_row = int(coordinate[1:2])
		if coordinate_row < 1 or coordinate_row > 8:
			return False
		return True
	except ValueError:
		return False

def coordinate_to_position(valid_coordinate):
	row = int(valid_coordinate[1:2]) -1
	col = letter_columns.index(valid_coordinate[0:1])
	return [row, col]