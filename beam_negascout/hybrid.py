import random as r
import time
from othellomachine import calculate_valid_moves, othellomachine, board_to_bitboards
from negascout import negascout

debug = False
if debug:
    from icecream import ic
else:
    def ic(*args):
        return None

def eval_state(player_0, player_1):
    """
    簡易な重み付き評価関数（AIは player1 の視点）
    """
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
    return score1 - score0

def hybrid_search(player_0, player_1, b, beam_depth, beam_width, negascout_depth):
    """
    ハイブリッド探索アルゴリズム:
      - ビームサーチ（chokudaiサーチ）で局面展開し、候補状態を beam_width に絞る
      - 最終レベルでは、各候補局面は negascout によりさらに深く探索して評価する
      
    引数:
      player_0, player_1: ビットボード形式の局面
      b: 現在の手番 (0または1)
      beam_depth: ビームサーチの探索深さ（ply数）
      beam_width: ビーム幅
      negascout_depth: 各候補局面評価用の Negascout 探索深さ
      
    戻り値:
      初手として選ぶべき手（move_chain の先頭）
    """
    # 各要素: (player_0, player_1, turn, move_chain, evaluation)
    # 初期評価は eval_state により算出
    beam = [(player_0, player_1, b, [], eval_state(player_0, player_1))]
    
    for d in range(beam_depth):
        next_beam = []
        for state in beam:
            p0, p1, turn, move_chain, _ = state
            moves = calculate_valid_moves(p0, p1, turn)
            if not moves:
                # パスの場合：手番交代のみ行う
                next_state = (p0, p1, 1 - turn, move_chain, eval_state(p0, p1))
                next_beam.append(next_state)
                continue
            for move in moves:
                success, new_turn, new_p0, new_p1, scores, flipped, valid_cells = othellomachine(p0, p1, turn, move)
                if not success:
                    continue
                # 最終層なら negascout を用いた深い探索で評価
                if d == beam_depth - 1:
                    score, _ = negascout(new_p0, new_p1, new_turn, negascout_depth, float("-inf"), float("inf"))
                    evaluation = score
                else:
                    evaluation = eval_state(new_p0, new_p1)
                new_chain = move_chain + [move]
                next_state = (new_p0, new_p1, new_turn, new_chain, evaluation)
                next_beam.append(next_state)
        if not next_beam:
            break
        # 評価が高い順に並べ、上位 beam_width 件のみを残す（AIは player1 の視点）
        next_beam.sort(key=lambda s: s[4], reverse=True)
        beam = next_beam[:beam_width]
    
    if beam:
        best_state = max(beam, key=lambda s: s[4])
        if best_state[3]:
            return best_state[3][0]
    return None

# テスト用 main 関数例
if __name__ == "__main__":
    # 通常のオセロ初期局面を使用（2次元板 → ビットボード変換）
    board = [[-1] * 8 for _ in range(8)]
    board[3][3] = 1; board[3][4] = 0
    board[4][3] = 0; board[4][4] = 1
    p0, p1 = board_to_bitboards(board)
    
    # パラメータ例: beam_depth=3, beam_width=5, negascout_depth=4
    move = hybrid_search(p0, p1, 0, beam_depth=300, beam_width=500, negascout_depth=8)
    print("ハイブリッド探索で選択された初手:", move)