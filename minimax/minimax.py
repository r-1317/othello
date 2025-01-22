from othellomachine import othellomachine

N = 10  # 探索の深さ

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

debug = True  # 完成時にはFalseにする
if debug and __name__ == "__main__":
  from icecream import ic
else:
  def ic(*args):
    return None

def get_input():
  board = [list(map(int, input().split())) for _ in range(8)]
  return board

# minimaxで探索を行い、最善手とその評価値を返す
def serch(board, b, depth):
  # まず、現在の盤面で置けるマスを計算
  status, b, board, scores, n, valid_cells = othellomachine(board, b, None)

# 盤面を受け取り、次の手(x, y)を返す
def minimax(board):
  ic(board)
  move, score = serch(board, 1, N)

  # 現在の状態(１の手番)深さnまでのminimaxを実行

if __name__ == "__main__":
  board = get_input()
  minimax(board)