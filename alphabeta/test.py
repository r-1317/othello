import othellomachine
from icecream import ic

board = [
  [-1, -1, -1, -1, -1, -1, -1, -1],
  [-1, -1,  0, -1, -1, -1, -1, -1],
  [-1, -1, -1,  0, -1, -1,  1, -1],
  [-1, -1,  0,  0,  0,  1, -1, -1],
  [-1, -1, -1,  0,  1,  0,  1, -1],
  [ 0,  0,  0,  1, -1, -1, -1,  1],
  [-1,  0, -1, -1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1]]

board = [
  [1, 1, 1, 1, 1, 1, 0, 1],
  [1, 0, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 0, 1, 1],
  [1, 1, 1, 1, 0, 1, 1, 1],
  [1, 0, 1, 0, 1, 1, 0, 1],
  [1, 0, 0, 1, 1, 1, 0, 1],
  [1, 0, 0, 0, 1, 1, 1, 1],
  [1, -1, 0, 0, 0, 1, 1, 1],
]


player_0, player_1 = othellomachine.board_to_bitboards(board)

ic.enable()

ic(othellomachine.calculate_valid_moves(player_0, player_1, 1))

# ic(player_0)
# ic(player_1)

print(f"player_0 = {player_0}")
print(f"player_1 = {player_1}")

# ic(othellomachine.get_flippable_cells(player_0, player_1, 1, 0, 7))