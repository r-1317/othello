import random as r
import time
from greedy import greedy
from othellomachine import othellomachine, calculate_valid_moves, board_to_bitboards

debug = False
if debug and __name__ == "__main__":
    from icecream import ic
else:
    def ic(*args):
        return None

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

# または、ビットボード形式で定義（下記は例）
DEFAULT_PLAYER_0 = 0b0000000000000000000000000000100000010000000000000000000000000000
DEFAULT_PLAYER_1 = 0b0000000000000000000000000001000000001000000000000000000000000000

def main():
    m = int(input("試合数を入力(1試合10分目安): "))
    time_list = []
    win_count = 0    # greedy AI (ここでは player1 が AI)
    lose_count = 0
    draw_count = 0

    for i in range(m):
        # ビットボードによる初期局面にリセット
        player_0, player_1 = DEFAULT_PLAYER_0, DEFAULT_PLAYER_1
        # greedy AI を player1 (手番==1)とする
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
                    # greedy AI の手番
                    move = greedy(player_0, player_1, turn)
                    if move is None:
                        move = r.choice(valid_cells)

            # 両者とも打てる手がなければパス処理
            if move is None:
                turn = 1 - turn
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if not valid_cells:
                    # ゲーム終了：各プレイヤーの駒の枚数で勝敗を判定
                    scores = (bin(player_0).count("1"), bin(player_1).count("1"))
                    if scores[1] > scores[0]:
                        win_count += 1
                    elif scores[0] > scores[1]:
                        lose_count += 1
                    else:
                        draw_count += 1
                    break

            status, turn, player_0, player_1, scores, flipped_count, valid_cells = othellomachine(player_0, player_1, turn, move)
            # 有効な手でなければ再選択
            if not status:
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if valid_cells:
                    move = r.choice(valid_cells)
                    continue

            # ターン交代
            turn = 1 - turn
            # 両者共手が打てなければゲーム終了
            if len(valid_cells) == 0:
                turn = 1 - turn
                valid_cells = calculate_valid_moves(player_0, player_1, turn)
                if not valid_cells:
                    # 勝敗判定（駒の枚数で判断）
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

    print(f"総試合数: {m}")
    print(f"勝ち: {win_count}")
    print(f"負け: {lose_count}")
    print(f"引き分け: {draw_count}")
    if win_count + lose_count > 0:
        winning_rate = win_count / (win_count + lose_count)
    else:
        winning_rate = 0
    print(f"勝率 (greedy AI視点): {winning_rate}")
    print(f"平均時間: {sum(time_list)/m:.2f} 秒")

if __name__ == "__main__":
    main()