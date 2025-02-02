debug = False
if debug:
    from icecream import ic
else:
    def ic(*args):
        return None

from negascout import negascout
from othellomachine import calculate_valid_moves, othellomachine, board_to_bitboards

def mtdf(player_0, player_1, b, depth, first_guess):
    g = first_guess
    lowerBound = float("-inf")
    upperBound = float("inf")
    best_move = None
    # 収束するまでループ
    while lowerBound < upperBound:
        beta = g + 1 if g == lowerBound else g
        score, move = negascout(player_0, player_1, b, depth, beta - 1, beta)
        g = score
        best_move = move
        if g < beta:
            upperBound = g
        else:
            lowerBound = g
    return g, best_move

# テスト用：ランダムプレイヤーと MTD(f) AI の対戦を行い、勝率などを出力する例
import random as r
import time

# 初期盤面（数字: -1=空, 0=黒, 1=白）
DEFAULT_BOARD = [
    [-1, -1, -1, -1, -1, -1, -1, -1], 
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1,  1,  0, -1, -1, -1],
    [-1, -1, -1,  0,  1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1], 
    [-1, -1, -1, -1, -1, -1, -1, -1], 
    [-1, -1, -1, -1, -1, -1, -1, -1]
]

# または、ビットボード形式で初期盤面を定義
DEFAULT_PLAYER_0 = 0b0000000000000000000000000000100000010000000000000000000000000000
DEFAULT_PLAYER_1 = 0b0000000000000000000000000001000000001000000000000000000000000000

def main():
    m = int(input("試合数を入力(1試合10分目安): "))
    time_list = []
    win_count = 0   # MTD(f) AI 側（ここでは player1 が AI とする）
    lose_count = 0
    draw_count = 0

    for i in range(m):
        # ビットボードによる初期局面
        player_0, player_1 = DEFAULT_PLAYER_0, DEFAULT_PLAYER_1
        # 先手・後手：ここでは player1 が MTD(f) AI、turn==1 のとき AI の手番
        turn = 1 if r.random() < 0.5 else 0 
        start_time = time.time()
        
        while True:
            valid_cells = calculate_valid_moves(player_0, player_1, turn)
            if not valid_cells:
                move = None
            else:
                if turn == 0:
                    # ランダムプレイヤーの手番
                    move = r.choice(valid_cells)
                else:
                    # MTD(f) AI の手番：初期推定値は 0 とする（必要に応じて変更）
                    depth = 5  # 探索深度（適宜変更）
                    score, move = mtdf(player_0, player_1, turn, depth, 0)
                    if move is None:
                        move = r.choice(valid_cells)

            # 両者共、手が打てなければパス処理
            if move is None:
                turn = 1 - turn
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if not valid_cells:
                    # ゲーム終了（各プレイヤーの駒の数で判定）
                    scores = (bin(player_0).count("1"), bin(player_1).count("1"))
                    if scores[1] > scores[0]:
                        win_count += 1
                    elif scores[0] > scores[1]:
                        lose_count += 1
                    else:
                        draw_count += 1
                    break

            status, turn, player_0, player_1, scores, n, valid_cells = othellomachine(player_0, player_1, turn, move)
            if not status:
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if valid_cells:
                    move = r.choice(valid_cells)
                    continue
            # 次手へ（相手番）
            turn = 1 - turn
            # 両者共打てる手がなければ終了
            if len(valid_cells) == 0:
                turn = 1 - turn
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if not valid_cells:
                    if scores[1] > scores[0]:
                        win_count += 1
                    elif scores[0] > scores[1]:
                        lose_count += 1
                    else:
                        draw_count += 1
                    break

        end_time = time.time()
        time_list.append(end_time - start_time)
        print(f"試合 {i+1} 終了: {int(end_time - start_time)} 秒")
        print(f"勝ち: {win_count}, 負け: {lose_count}, 引き分け: {draw_count}")

    print(f"勝ち: {win_count}")
    print(f"負け: {lose_count}")
    print(f"引き分け: {draw_count}")
    if win_count + lose_count > 0:
        winning_rate = win_count / (win_count + lose_count)
    else:
        winning_rate = 0
    print(f"勝率: {winning_rate}")
    print(f"平均時間: {sum(time_list) / m:.2f} 秒")

if __name__ == "__main__":
    main()