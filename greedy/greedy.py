debug = False
if debug:
    from icecream import ic
else:
    def ic(*args):
        return None

from othellomachine import calculate_valid_moves, othellomachine

def greedy(player_0, player_1, b):
    """
    貪欲法による探索
    - player_0, player_1: ビットボード形式の局面
    - b: 現在の手番 (0 または 1)
    
    合法手のうち、今回の手で返せる駒の枚数 (flipped_count) が最大となるものを選ぶ。
    """
    valid_moves = calculate_valid_moves(player_0, player_1, b)
    if not valid_moves:
        return None

    best_move = None
    best_flip = -1
    for move in valid_moves:
        # othellomachine で手をシミュレーションし、flipped_count を得る
        success, curr_b, new_player_0, new_player_1, scores, flipped_count, valid_cells = othellomachine(player_0, player_1, b, move)
        if not success:
            continue
        if flipped_count > best_flip:
            best_flip = flipped_count
            best_move = move

    return best_move

# テスト用の main 関数例（必要に応じて調整してください）
if __name__ == "__main__":
    # ここでは、盤面の初期設定例として4箇所に駒が置いてある通常のオセロ初期盤面を使用します
    board = [[-1] * 8 for _ in range(8)]
    board[3][3] = 1; board[3][4] = 0
    board[4][3] = 0; board[4][4] = 1

    from othellomachine import board_to_bitboards
    player_0, player_1 = board_to_bitboards(board)
    
    # 現在の手番として 0 (黒) を例とする
    move = greedy(player_0, player_1, 0)
    print("貪欲法で選択された手:", move)