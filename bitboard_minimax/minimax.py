from othellomachine import othellomachine, calculate_valid_moves, board_to_bitboards, bitboards_to_board, popcount
import time

N = 5  # 探索の深さ (5が限界?)
# N = 2  # テスト用

wheights = (
  (120, -20,  20,   5,   5,  20, -20, 120),
  (-20, -40,  -5,  -5,  -5,  -5, -40, -20),
  ( 20,  -5,  15,   3,   3,  15,  -5,  20),
  (  5,  -5,   3,   3,   3,   3,  -5,   5),
  (  5,  -5,   3,   3,   3,   3,  -5,   5),
  ( 20,  -5,  15,   3,   3,  15,  -5,  20),
  (-20, -40,  -5,  -5,  -5,  -5, -40, -20),
  (120, -20,  20,   5,   5,  20, -20, 120)
)

debug = False
# debug = True
if debug:
  from icecream import ic
else:
  def ic(*args):
    return None

def get_input():
  board = [list(map(int, input().split())) for _ in range(8)]
  return board

# 盤面の評価値を計算
def calc_score(player_0, player_1):
  scores = [0, 0]
  for bit_index in range(64):
    if player_0 & (1 << bit_index):
      scores[0] += wheights[bit_index//8][bit_index%8]
    elif player_1 & (1 << bit_index):
      scores[1] += wheights[bit_index//8][bit_index%8]
  return scores[1] - scores[0]

# 廃止
# def count_stone(board):
#   stone_count = 0
#   for i in range(8):
#     for j in range(8):
#       if board[i][j] != -1:
#         stone_count += 1
#   return stone_count

def final_score(player_0, player_1):
  return popcount(player_1) - popcount(player_0)

# minimaxで探索を行い、最善手とその評価値を返す
def search(player_0, player_1, b, depth):
  # まず、現在の盤面で置けるマスを計算
  # board = bitboards_to_board(player_0, player_1)
  valid_cells = calculate_valid_moves(player_0, player_1, b)
  n = len(valid_cells)
  # 合法手がない場合
  if n == 0:
    # 盤面がすべて埋まっている場合、最終評価を返す
    # if count_stone(board) == 64:
    if popcount(player_0) + popcount(player_1) == 64:
      return None, final_score(player_0, player_1)
    # パスの場合、相手の手番に移る
    else:
      b = not b
      valid_cells = calculate_valid_moves(player_0, player_1, b)
      n = len(valid_cells)
      # 相手もパスの場合、ゲーム終了
      if n == 0:
        return None, final_score(player_0, player_1)
  # 深さが0の場合、評価値を返す
  if depth == 0:
    return None, calc_score(player_0, player_1)
  # minmax法で再帰的に探索
  # 手番が1の場合、最大値を返す
  if b:
    best_move = None
    best_score = -10**9
    for move in valid_cells:
      status, _, new_player_0, new_player_1, _, _, _ = othellomachine(player_0, player_1, b, move)
      if not status:
        ic(bitboards_to_board(player_0, player_1), b, move)
      assert status
      # new_player_0, new_player_1 = board_to_bitboards(new_board)
      _, score = search(new_player_0, new_player_1, not b, depth-1)
      if best_score < score:
        # ic(best_move, best_score, move, score)
        best_move = move
        best_score = score
  # 手番が0の場合、最小値を返す
  else:
    best_move = None
    best_score = 10**9
    for move in valid_cells:
      status, _, new_player_0, new_player_1, _, _, _ = othellomachine(player_0, player_1, b, move)
      if not status:
        ic(bitboards_to_board(player_0, player_1), b, move)
      assert status
      # new_player_0, new_player_1 = board_to_bitboards(new_board)
      _, score = search(new_player_0, new_player_1, not b, depth-1)
      if score < best_score:
        best_move = move
        best_score = score
  # 最善手とその評価値を返す
  # ic(best_move, best_score)
  return best_move, best_score

# 盤面を受け取り、次の手(x, y)を返す
def minimax(player_0, player_1):
  # player_0, player_1 = board_to_bitboards(board)
  move, score = search(player_0, player_1, 1, N)
  ic(move, score)
  return move

if __name__ == "__main__":
  start = time.time()
  board = get_input()
  player_0, player_1 = board_to_bitboards(board)
  move = minimax(player_0, player_1)
  print(move)
  print(f"実行時間: {time.time()-start}秒")