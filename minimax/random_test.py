import random as r
from minimax import minimax
from othellomachine import othellomachine, calculate_valid_moves

debug = True
if debug and __name__ == "__main__":
  from icecream import ic
else:
  def ic(*args):
    return None

# ランダムに手を打つプレイヤーに対する勝率を計算

DEFAULT_BOAD = [
  [-1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1],
  [-1, -1, -1,  1,  0, -1, -1, -1],
  [-1, -1, -1,  0,  1, -1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1], 
  [-1, -1, -1, -1, -1, -1, -1, -1]
  ]

def main():
  win_count = 0
  lose_count = 0
  draw_count = 0

  # 100回ゲームを行う
  for i in range(100):
    board = [row[:] for row in DEFAULT_BOAD]
    turn = i % 2
    valid_cells = calculate_valid_moves(board, turn)

    while True:
      # ランダムプレイヤーの手番
      if not turn:
        valid_cells = calculate_valid_moves(board, turn)
        move = r.choice(valid_cells)
      # ミニマックスプレイヤーの手番
      else:
        move = minimax(board)
      status, turn, board, scores, n, valid_cells = othellomachine(board, turn, move)
      assert status
      turn = not turn

      if len(valid_cells) == 0:
        turn = not turn
        valid_cells = calculate_valid_moves(board, turn)
        if len(valid_cells) == 0:
          if scores[0] < scores[1]:
            win_count += 1
          elif scores[1] < scores[0]:
            lose_count += 1
          else:
            draw_count += 1
          ic(win_count, lose_count, draw_count)
          break

  # 集計
  print(f"勝ち: {win_count}")
  print(f"負け: {lose_count}")
  print(f"引き分け: {draw_count}")

  # 勝率 (引き分けは除外)
  winning_rate = win_count / (win_count + lose_count)

  print(f"勝率: {winning_rate}")


if __name__ == "__main__":
  main()