import Board
white_castling_left = []
white_castling_left.append(Board.HumanReadableMove("d2", "d3"))
white_castling_left.append(Board.HumanReadableMove("c1", "f4"))
white_castling_left.append(Board.HumanReadableMove("b1", "c3"))
white_castling_left.append(Board.HumanReadableMove("d1", "d2"))

white_castling_right = []
white_castling_right.append(Board.HumanReadableMove("g1", "f3"))
white_castling_right.append(Board.HumanReadableMove("e2", "e3"))
white_castling_right.append(Board.HumanReadableMove("f1", "e2"))

black_castling_left = []
black_castling_left.append(Board.HumanReadableMove("d7", "d6"))
black_castling_left.append(Board.HumanReadableMove("c8", "f5"))
black_castling_left.append(Board.HumanReadableMove("b8", "c6"))
black_castling_left.append(Board.HumanReadableMove("d8", "d7"))

black_castling_right = []
black_castling_right.append(Board.HumanReadableMove("g8", "f6"))
black_castling_right.append(Board.HumanReadableMove("e7", "e6"))
black_castling_right.append(Board.HumanReadableMove("f8", "e7"))

white_in_check = []
white_in_check.append(Board.HumanReadableMove("e7", "e6"))
white_in_check.append(Board.HumanReadableMove("d8", "h4"))
white_in_check.append(Board.HumanReadableMove("f2", "f3"))

black_in_check = []
black_in_check.append(Board.HumanReadableMove("e2", "e3"))
black_in_check.append(Board.HumanReadableMove("d1", "h5"))
black_in_check.append(Board.HumanReadableMove("f7", "f6"))

white_in_check_capture = []
white_in_check_capture.append(Board.HumanReadableMove("e2", "e4"))
white_in_check_capture.append(Board.HumanReadableMove("d8", "e3"))