import Helper
import Board

myBoard = Board.Board(8, 8)
myBoard.print()

while True:
	coordinate = input("select piece: ")
	print(Helper.coordinate_is_valid(coordinate))