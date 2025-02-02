import random as r
import time
from hybrid import hybrid_search
from othellomachine import othellomachine, calculate_valid_moves, board_to_bitboards

debug = False
if debug:
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

# または、ビットボード形式で定義（初期局面: 通常盤面）
DEFAULT_PLAYER_0 = 0b0000000000000000000000000000100000010000000000000000000000000000
DEFAULT_PLAYER_1 = 0b0000000000000000000000000001000000001000000000000000000000000000

def main():
    m = int(input("試合数を入力(1試合の所要時間は局面によります): "))
    time_list = []
    win_count = 0    # ハイブリッドAI側（ここでは player1 を使用）
    lose_count = 0
    draw_count = 0

    # ハイブリッドAIのパラメータ例
    beam_depth = 30       # ビーム探索の深さ（ply）
    beam_width = 50      # ビーム幅
    negascout_depth = 8  # 候補局面評価用の negascout 探索深さ

    for i in range(m):
        # 初期局面（ビットボード）にリセット
        player_0, player_1 = DEFAULT_PLAYER_0, DEFAULT_PLAYER_1
        # ハイブリッドAI (player1) とランダム (player0) を対局
        turn = 1 if r.random() < 0.5 else 0
        start_time = time.time()

        while True:
            valid_moves = calculate_valid_moves(player_0, player_1, turn)
            if not valid_moves:
                move = None
            else:
                if turn == 0:
                    # ランダムプレイヤーの手番：合法手からランダムに選択
                    move = r.choice(valid_moves)
                else:
                    # ハイブリッドAI の手番
                    move = hybrid_search(player_0, player_1, turn, beam_depth, beam_width, negascout_depth)
                    if move is None:
                        move = r.choice(valid_moves)

            # 両者とも手が打てなければパス処理
            if move is None:
                turn = 1 - turn
                valid_moves = calculate_valid_moves(player_0, player_1, turn)
                if not valid_moves:
                    # ゲーム終了：各プレイヤーの駒の枚数で判定
                    score0 = bin(player_0).count("1")
                    score1 = bin(player_1).count("1")
                    if score1 > score0:
                        win_count += 1
                    elif score0 > score1:
                        lose_count += 1
                    else:
                        draw_count += 1
                    break

            # 選択した手を盤面へ適用
            status, turn, player_0, player_1, scores, flipped_count, valid_moves = othellomachine(player_0, player_1, turn, move)
            if not status:
                valid_moves = calculate_valid_moves(player_0, player_1, turn)
                if valid_moves:
                    move = r.choice(valid_moves)
                    continue

            # 次ターンへ
            if not valid_moves:
                turn = 1 - turn
                valid_moves = calculate_valid_moves(player_0, player_1, turn)
                if not valid_moves:
                    score0 = bin(player_0).count("1")
                    score1 = bin(player_1).count("1")
                    if score1 > score0:
                        win_count += 1
                    elif score0 > score1:
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
    print(f"勝率 (ハイブリッドAI視点): {winning_rate}")
    print(f"平均時間: {sum(time_list)/m:.2f} 秒")

if __name__ == "__main__":
    main()