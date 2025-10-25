import Pieces

class Board:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols

		self.grid = []
		for r in range(self.rows):
			row = []
			for c in range(self.cols):
				if r == 1:
					row.append(Pieces.Pawn(True))
				elif r == 6:
					row.append(Pieces.Pawn(False))
				else:
					row.append(Pieces.Piece(False, "."))
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