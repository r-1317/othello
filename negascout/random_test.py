import random as r
import time
from negascout import negascout
from othellomachine import othellomachine, calculate_valid_moves, board_to_bitboards

debug = False
if debug and __name__ == "__main__":
    from icecream import ic
else:
    def ic(*args):
        return None

# 初期盤面（数字で表現：-1=空, 0=黒, 1=白）
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
    win_count = 0   # negascout（AI）側の勝ちカウント（ここでは player1 とする）
    lose_count = 0
    draw_count = 0

    # m回ゲームを行う
    for i in range(m):
        # ビットボードで初期局面を設定（player0: ランダム, player1:  negascout AI）
        player_0, player_1 = DEFAULT_PLAYER_0, DEFAULT_PLAYER_1
        # 先手・後手をランダムに決める（ここでは、player1が negascout AI）
        turn = 1 if r.random() < 0.5 else 0 
        valid_cells = calculate_valid_moves(player_0, player_1, turn)
        start_time = time.time()

        while True:
            # 手を選ぶ
            if turn == 0:
                # ランダムプレイヤーの手番
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if not valid_cells:
                    move = None
                else:
                    move = r.choice(valid_cells)
            else:
                # negascout AIの手番
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if not valid_cells:
                    move = None
                else:
                    # 探索深度は適宜設定（例: 5）
                    depth = 8
                    score, move = negascout(player_0, player_1, turn, depth, float("-inf"), float("inf"))
                    # move が Noneの場合も考慮
                    if move is None:
                        move = r.choice(valid_cells)
            
            # 両者とも置ける手が無い場合、パス処理
            if move is None:
                turn = 1 - turn
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if not valid_cells:
                    # ゲーム終了：駒の枚数で勝敗判定（scores: (popcount(player_0), popcount(player_1))）
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
                # 不正な手の場合はランダムで再選択
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if valid_cells:
                    move = r.choice(valid_cells)
                    continue
                else:
                    turn = 1 - turn
            else:
                # ターン交代
                turn = 1 - turn
                # 両者手が無い場合はゲーム終了
                if len(valid_cells) == 0:
                    turn = 1 - turn
                    valid_cells = calculate_valid_moves(player_0, player_1, turn)
                    if not valid_cells:
                        # ゲーム終了：駒の枚数で勝敗を判定
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

    # 集計結果の表示
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