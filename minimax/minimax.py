from othellomachine import othellomachine, calculate_valid_moves
import time

N = 2  # 探索の深さ (7が限界かな)

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
if debug and __name__ == "__main__":
  from icecream import ic
else:
  def ic(*args):
    return None

def get_input():
  board = [list(map(int, input().split())) for _ in range(8)]
  return board

# 盤面の評価値を計算
def calc_score(board):
  scores = [0, 0]
  for i in range(8):
    for j in range(8):
      if board[i][j] != -1:
        scores[board[i][j]] += wheights[i][j]
  return scores[1] - scores[0]

def count_stone(board):
  stone_count = 0
  for i in range(8):
    for j in range(8):
      if board[i][j] != -1:
        stone_count += 1
  return stone_count

def final_score(board):
  scores = [0, 0]
  for i in range(8):
    for j in range(8):
      if board[i][j] != -1:
        scores[board[i][j]] += 1
  return (scores[1] - scores[0])*10**5

# minimaxで探索を行い、最善手とその評価値を返す
def serch(board, b, depth):
  # まず、現在の盤面で置けるマスを計算
  valid_cells = calculate_valid_moves(board, b)
  n = len(valid_cells) 
  # 合法手がない場合
  if n == 0:
    # 盤面がすべて埋まっている場合、最終評価を返す
    if count_stone(board) == 64:
      return None, final_score(board)
    # パスの場合、相手の手番に移る
    else:
      b = not b
      valid_cells = calculate_valid_moves(board, b)
      n = len(valid_cells)
      # 相手もパスの場合、ゲーム終了
      if n == 0:
        return None, final_score(board)
  # 深さが0の場合、評価値を返す
  if depth == 0:
    return None, calc_score(board)
  # minmax法で再帰的に探索
  # 手番が1の場合、最大値を返す
  if b:
    best_move = None
    best_score = -10**9
    for move in valid_cells:
      status, _, new_board, _, _, _ = othellomachine([row[:] for row in board], b, move)  # ボードをdeepcopyして渡す
      if not status:
        ic(valid_cells)
        ic(board, b, move, new_board)
      assert status
      _, score = serch(new_board, not b, depth-1)
      if best_score < score:
        ic(best_move, best_score, move, score)
        best_move = move
        best_score = score
  # 手番が0の場合、最小値を返す
  else:
    best_move = None
    best_score = 10**9
    for move in valid_cells:
      status, _, new_board, _, _, _ = othellomachine([row[:] for row in board], b, move)
      assert status
      _, score = serch(new_board, not b, depth-1)
      if score < best_score:
        best_move = move
        best_score = score
  # 最善手とその評価値を返す
  ic(best_move, best_score)
  return best_move, score

# 盤面を受け取り、次の手(x, y)を返す
def minimax(board):
  ic(board)
  move, score = serch(board, 1, N)
  ic(move, score)
  return move

if __name__ == "__main__":
  start = time.time()
  board = get_input()
  move = minimax(board)
  print(move)
  print(f"実行時間: {time.time()-start}秒")