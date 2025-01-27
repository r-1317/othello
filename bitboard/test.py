import othellomachine

board = [
  [ 1, -1, -1, -1, -1, -1, -1, -1],
  [-1,  1, -1, -1, -1, -1, -1, -1],
  [ 0,  1,  0,  0,  0,  0,  0, -1],
  [-1,  0, -1,  0,  0,  0,  0, -1],
  [ 0,  1,  1,  1,  1,  1, -1, -1],
  [-1, -1, -1,  0,  1, -1, -1, -1],
  [-1, -1, -1, -1, -1,  1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1]
]

player_0, player_1 = othellomachine.board_to_bitboards(board)

valid_moves = othellomachine.calculate_valid_moves(board, 1)

print(valid_moves)  # [(0, 7), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 7), (5, 2), (6, 2), (6, 3), (6, 4)]