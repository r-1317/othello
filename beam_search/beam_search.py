debug = False
if debug:
    from icecream import ic
else:
    def ic(*args):
        return None

from othellomachine import calculate_valid_moves, othellomachine

# 評価関数。ここでは簡易な重み付き評価を実装。
def eval_state(player_0, player_1):
    weights = (
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
            score0 += weights[bit_index // 8][bit_index % 8]
        elif player_1 & (1 << bit_index):
            score1 += weights[bit_index // 8][bit_index % 8]
    # AI側の視点として、ここでは手番 b が 1 の場合(score1 - score0)を直接返す
    return score1 - score0

def beamsearch(player_0, player_1, b, depth, beam_width=5):
    """
    ビームサーチによる探索
      player_0, player_1 : ビットボード形式の局面
      b                : 現在の手番 (0または1)
      depth            : 探索深さ (plie数)
      beam_width       : ビーム幅

    戻り値: 初手として選ぶべき手
    """
    # 各要素: (player_0, player_1, turn, move_chain, evaluation)
    # move_chain は初手からの手のリスト（空の場合はまだ手が選ばれていない状態）
    beam = [(player_0, player_1, b, [], eval_state(player_0, player_1))]
    
    for d in range(depth):
        new_beam = []
        for state in beam:
            p0, p1, turn, move_chain, _ = state
            valid_moves = calculate_valid_moves(p0, p1, turn)
            # 手がない場合はパス
            if not valid_moves:
                new_state = (p0, p1, 1 - turn, move_chain[:], eval_state(p0, p1))
                new_beam.append(new_state)
                continue

            for move in valid_moves:
                success, curr_turn, new_p0, new_p1, scores, flipped_count, valid_cells = othellomachine(p0, p1, turn, move)
                if not success:
                    continue
                # 局面評価（常に AI 側の評価視点としてcalc_scoreを使用）
                evaluation = eval_state(new_p0, new_p1)
                # 初手は move_chain が空なら、今回の move が初手
                new_move_chain = move_chain[:] + [move]
                new_state = (new_p0, new_p1, curr_turn, new_move_chain, evaluation)
                new_beam.append(new_state)
        # 評価が高い順に並べ、上位 beam_width 個に絞る
        if not new_beam:
            break
        new_beam.sort(key=lambda st: st[4], reverse=True)
        beam = new_beam[:beam_width]
    # 最終的に評価が最も高い局面の move_chain の先頭を初手として返す
    best_state = beam[0]
    move_chain = best_state[3]
    if move_chain:
        return move_chain[0]
    else:
        return None

# テスト用 main 関数（必要に応じて調整してください）
if __name__ == "__main__":
    # 例: 通常の初期オセロ局面（2次元リストからビットボード変換）
    board = [[-1] * 8 for _ in range(8)]
    board[3][3] = 1; board[3][4] = 0
    board[4][3] = 0; board[4][4] = 1

    # ここでは、外部から othellomachine の board_to_bitboards を利用
    from othellomachine import board_to_bitboards
    p0, p1 = board_to_bitboards(board)
    # 現在の手番を 0 (黒) とする例
    move = beamsearch(p0, p1, 0, depth=3000, beam_width=5000)
    print("ビームサーチで選択された初手:", move)