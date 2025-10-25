def coordinate_is_valid(coordinate):
	if not type(coordinate) == str:
		return False
	if len(coordinate) > 2:
		return False
	
	coordinate_col = coordinate[0:1].lower()
	letter_columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

	if not coordinate_col in letter_columns:
		return False
	
	try:
		coordinate_row = int(coordinate[1:2])
		if coordinate_row < 1 or coordinate_row > 8:
			return False
		return True
	except ValueError:
		return False
	
