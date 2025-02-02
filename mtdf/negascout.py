debug = False
if debug:
    from icecream import ic
else:
    def ic(*args):
        return None

# グローバルな置換表
tt = {}

def calc_score(player_0, player_1):
    # alphabeta.py 等で用いている重みテーブルなどを参考に実装してください
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
    score0, score1 = 0, 0
    for bit_index in range(64):
        if player_0 & (1 << bit_index):
            score0 += wheights[bit_index // 8][bit_index % 8]
        elif player_1 & (1 << bit_index):
            score1 += wheights[bit_index // 8][bit_index % 8]
    return score1 - score0

from othellomachine import calculate_valid_moves, othellomachine, popcount

def negascout(player_0, player_1, b, depth, alpha, beta):
    # 置換表のキーとして、(player0, player1, turn, depth) を使用
    key = (player_0, player_1, b, depth)
    if key in tt:
        return tt[key]
        
    valid_moves = calculate_valid_moves(player_0, player_1, b)
    if depth == 0 or not valid_moves:
        value = calc_score(player_0, player_1)
        tt[key] = (value, None)
        return value, None

    best_value = float("-inf")
    best_move = None
    first_child = True

    for move in valid_moves:
        success, curr_b, new_player_0, new_player_1, scores, n, valid_cells = othellomachine(player_0, player_1, b, move)
        if not success:
            continue
        if first_child:
            score, _ = negascout(new_player_0, new_player_1, 1 - b, depth - 1, -beta, -alpha)
            score = -score
            first_child = False
        else:
            score, _ = negascout(new_player_0, new_player_1, 1 - b, depth - 1, -alpha - 1, -alpha)
            score = -score
            if alpha < score < beta:
                score, _ = negascout(new_player_0, new_player_1, 1 - b, depth - 1, -beta, -score)
                score = -score
        if score > best_value:
            best_value = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break   # βカット

    tt[key] = (best_value, best_move)
    return best_value, best_move