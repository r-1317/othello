import random as r
from alphabeta import alphabeta
from othellomachine import othellomachine, calculate_valid_moves, board_to_bitboards
import time

debug = False
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

DEFAULT_PLAYER_0 = 0b0000000000000000000000000000100000010000000000000000000000000000
DEFAULT_PLAYER_1 = 0b0000000000000000000000000001000000001000000000000000000000000000

def main():
  m = (int(input("試合数を入力(1試合10分目安): ")))

  time_list = []
  win_count = 0
  lose_count = 0
  draw_count = 0

  # m回ゲームを行う
  for i in range(m):
    # board = [row[:] for row in DEFAULT_BOAD]
    player_0, player_1 = DEFAULT_PLAYER_0, DEFAULT_PLAYER_1
    turn = 1 if r.random() < 0.5 else 0
    valid_cells = calculate_valid_moves(player_0, player_1, turn)
    start_time = time.time()

    while True:
      # ランダムプレイヤーの手番
      if not turn:
        valid_cells = calculate_valid_moves(player_0, player_1, turn)
        move = r.choice(valid_cells)
      # ミニマックスプレイヤーの手番
      else:
        move = alphabeta(player_0, player_1)
      status, turn, player_0, player_1, scores, n, valid_cells = othellomachine(player_0, player_1, turn, move)
      assert status
      turn = not turn

      if len(valid_cells) == 0:
        turn = not turn
        valid_cells = calculate_valid_moves(player_0, player_1, turn)
        if len(valid_cells) == 0:
          if scores[0] < scores[1]:
            win_count += 1
          elif scores[1] < scores[0]:
            lose_count += 1
          else:
            draw_count += 1
          # ic(win_count, lose_count, draw_count)
          break

    end_time = time.time()
    time_list.append(end_time - start_time)
    print(f"試合{i+1}終了: {int(end_time - start_time)}秒")
    print(f"勝ち: {win_count}, 負け: {lose_count}, 引き分け: {draw_count}")

  # 集計
  print(f"勝ち: {win_count}")
  print(f"負け: {lose_count}")
  print(f"引き分け: {draw_count}")

  # 勝率 (引き分けは除外)
  winning_rate = win_count / (win_count + lose_count)

  print(f"勝率: {winning_rate}")
  print(f"平均時間: {sum(time_list) / m:.2f}秒")


if __name__ == "__main__":
  main()