debug = False
if debug:
    from icecream import ic
else:
    def ic(*args):
        return None

# alphabeta.py からの参照（重みテーブル・評価関数）
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

def calc_score(player_0, player_1):
    score0, score1 = 0, 0
    for bit_index in range(64):
        if player_0 & (1 << bit_index):
            score0 += wheights[bit_index // 8][bit_index % 8]
        elif player_1 & (1 << bit_index):
            score1 += wheights[bit_index // 8][bit_index % 8]
    # 今回は "白(1) - 黒(0)" の差を評価値として返す
    return score1 - score0

from othellomachine import calculate_valid_moves, othellomachine, popcount

def negascout(player_0, player_1, b, depth, alpha, beta):
    valid_moves = calculate_valid_moves(player_0, player_1, b)
    # 探索深度0または合法手が存在しない場合は評価を返す
    if depth == 0 or not valid_moves:
        return calc_score(player_0, player_1), None

    best_value = float("-inf")
    best_move = None
    first_child = True

    for move in valid_moves:
        success, curr_b, new_player_0, new_player_1, scores, n, valid_cells = othellomachine(player_0, player_1, b, move)
        if not success:
            continue
        # 次手は相手番 (1 - b) に切り替える
        if first_child:
            score, _ = negascout(new_player_0, new_player_1, 1 - b, depth - 1, -beta, -alpha)
            score = -score
            first_child = False
        else:
            # Null window search
            score, _ = negascout(new_player_0, new_player_1, 1 - b, depth - 1, -alpha - 1, -alpha)
            score = -score
            if alpha < score < beta:
                # 再探索
                score, _ = negascout(new_player_0, new_player_1, 1 - b, depth - 1, -beta, -score)
                score = -score
        if score > best_value:
            best_value = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break   # βカット
    return best_value, best_move

# 例: メイン関数として探索結果を表示する場合
if __name__ == "__main__":
    # 初期盤面例（数字で表現：-1=空, 0=黒, 1=白）
    # 通常のオセロ初期盤面に合わせて設定してください
    board = [[-1] * 8 for _ in range(8)]
    board[3][3] = 1; board[3][4] = 0
    board[4][3] = 0; board[4][4] = 1

    # board からビットボードへ変換（othellomachine.py の関数を利用）
    from othellomachine import board_to_bitboards
    player_0, player_1 = board_to_bitboards(board)

    # 探索深度の設定（例: 5）
    depth = 5
    # 初期盤面の手番：ここでは 0 (黒) を例とする
    b = 0
    # 初期の α, β
    alpha = float("-inf")
    beta = float("inf")

    best_value, best_move = negascout(player_0, player_1, b, depth, alpha, beta)
    print("best value:", best_value)
    print("best move:", best_move)