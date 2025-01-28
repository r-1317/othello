from othellomachine import othellomachine, calculate_valid_moves, board_to_bitboards, bitboards_to_board, popcount
import time

N = 5  # 探索の深さ (5程度が限界?)

# 重み付けテーブル
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

# デバッグ用（必要に応じて切り替え）
debug = False
if debug:
  from icecream import ic
else:
  def ic(*args):
    return None

def get_input():
  board = [list(map(int, input().split())) for _ in range(8)]
  return board

# 盤面の評価値を計算（中盤〜終盤向けの評価）
def calc_score(player_0, player_1):
  scores = [0, 0]
  for bit_index in range(64):
    if player_0 & (1 << bit_index):
      scores[0] += wheights[bit_index//8][bit_index%8]
    elif player_1 & (1 << bit_index):
      scores[1] += wheights[bit_index//8][bit_index%8]
  # 今回は "白(1) - 黒(0)" を返す形にしている
  return scores[1] - scores[0]

# ゲーム終了時の最終スコア（駒数差）
def final_score(player_0, player_1):
  return popcount(player_1) - popcount(player_0)

def search_alpha_beta(player_0, player_1, b, depth, alpha, beta):
  """
  アルファ–ベータ法を用いた探索関数
  player_0: 黒のbitboard
  player_1: 白のbitboard
  b: 現在の手番(True=白, False=黒)
  depth: 残り探索深さ
  alpha, beta: アルファ–ベータカット用パラメータ
  """
  # 合法手を取得
  valid_cells = calculate_valid_moves(player_0, player_1, b)
  n = len(valid_cells)

  # 合法手がない場合
  if n == 0:
    # 盤面がすべて埋まっている場合はゲーム終了とみなし、最終スコアを返す
    if popcount(player_0) + popcount(player_1) == 64:
      return None, final_score(player_0, player_1)
    else:
      # パスの場合は手番を入れ替えてチェック
      b = not b
      valid_cells = calculate_valid_moves(player_0, player_1, b)
      n = len(valid_cells)
      # 相手もパスならゲーム終了
      if n == 0:
          return None, final_score(player_0, player_1)
      # パスではあるがゲーム続行の場合、depthは同じで手番を進める
      return search_alpha_beta(player_0, player_1, b, depth, alpha, beta)

  # 深さが0になった場合は評価値を返す
  if depth == 0:
    return None, calc_score(player_0, player_1)

  # 手番が白(b=True) -> 最大化
  if b:
    best_move = None
    best_score = float("-inf")

    for move in valid_cells:
      status, _, new_p0, new_p1, _, _, _ = othellomachine(player_0, player_1, b, move)
      # 念のためステータスチェック
      if not status:
        ic(bitboards_to_board(player_0, player_1), b, move)
      assert status

      # 再帰探索
      _, score = search_alpha_beta(new_p0, new_p1, not b, depth - 1, alpha, beta)

      # 最大値の更新
      if score > best_score:
        best_score = score
        best_move = move

      # alpha の更新
      alpha = max(alpha, best_score)

      # βより大きくなればカット
      if beta <= alpha:
        break

    return best_move, best_score

  # 手番が黒(b=False) -> 最小化
  else:
    best_move = None
    best_score = float("inf")

    for move in valid_cells:
      status, _, new_p0, new_p1, _, _, _ = othellomachine(player_0, player_1, b, move)
      if not status:
        ic(bitboards_to_board(player_0, player_1), b, move)
      assert status

      _, score = search_alpha_beta(new_p0, new_p1, not b, depth - 1, alpha, beta)

      # 最小値の更新
      if score < best_score:
        best_score = score
        best_move = move

      # beta の更新
      beta = min(beta, best_score)

      # αより小さくなればカット
      if beta <= alpha:
        break

    return best_move, best_score

def alphabeta(player_0, player_1):
  """
  アルファ–ベータ探索を呼び出して次の手を取得する関数。
  b=1(白手番) で深さ N から探索を開始。
  """
  # 初期alpha, betaはそれぞれ -∞, +∞
  move, score = search_alpha_beta(player_0, player_1, b=True, depth=N, alpha=float("-inf"), beta=float("inf"))
  ic(move, score)
  return move

if __name__ == "__main__":
  start = time.time()
  board = get_input()
  player_0, player_1 = board_to_bitboards(board)
  # 白手番を想定
  move = alphabeta(player_0, player_1)
  print(move)
  print(f"実行時間: {time.time() - start} 秒")
