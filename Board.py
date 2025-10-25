class Board:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols

		self.grid = []
		for r in range(self.rows):
			row = []
			for c in range(self.cols):
				row.append(0)
			self.grid.append(row)
	
	def print(self):
		print(" v"*8)
		for row in self.grid:
			string = "-"
			connector = " "
			string = string + connector.join(map(str, row)) + "-"
			print(string)

		print(" ^"*8)