from othellomachine import othellomachine

debug = True  # 完成時にはFalseにする
if debug and __name__ == "__main__":
  from icecream import ic
else:
  def ic(*args):
    return None

def get_input():
  board = [list(map(int, input().split())) for _ in range(8)]
  return board

# 盤面を受け取り、次の手(x, y)を返す
def minimax(board):
  ic(board)

if __name__ == "__main__":
  board = get_input()
  minimax(board)