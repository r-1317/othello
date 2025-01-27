debug = False
# debug = True
if debug :
    from icecream import ic
else:
    def ic(*args):
        return None

# 2次元配列をビットボード形式に変換する
def board_to_bitboards(board):
    player_0, player_1 = 0, 0
    for i in range(8):
        for j in range(8):
            bit_index = i * 8 + j
            if board[i][j] == 0:
                player_0 |= 1 << bit_index
            elif board[i][j] == 1:
                player_1 |= 1 << bit_index
    return player_0, player_1

# ビットボード形式を2次元配列に変換する
def bitboards_to_board(player_0, player_1):
    board = [[-1] * 8 for _ in range(8)]
    for i in range(8):
        for j in range(8):
            bit_index = i * 8 + j
            if (player_0 >> bit_index) & 1:
                board[i][j] = 0
            elif (player_1 >> bit_index) & 1:
                board[i][j] = 1
    return board

# 枚数を数える
# コピペなので仕組みはよくわかっていない
# 出典: https://qiita.com/zawawahoge/items/8bbd4c2319e7f7746266
def popcount(x):
    # 2bitごとの組に分け、立っているビット数を2bitで表現する
    x = x - ((x >> 1) & 0x5555555555555555)

    # 4bit整数に 上位2bit + 下位2bit を計算した値を入れる
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)

    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f # 8bitごと
    x = x + (x >> 8) # 16bitごと
    x = x + (x >> 16) # 32bitごと
    x = x + (x >> 32) # 64bitごと = 全部の合計
    return x & 0x0000007f

# 2つのマスが隣り合っているかどうかを判定する
def is_adjacent(prev_index, next_index):
    prev_x, prev_y = prev_index // 8, prev_index % 8
    next_x, next_y = next_index // 8, next_index % 8
    return abs(prev_x - next_x) <= 1 and abs(prev_y - next_y) <= 1

# 駒を置いたときにひっくり返せる座標のリストを返す
def get_flippable_cells(player_0, player_1, b, x, y):
    # player_0, player_1 = board_to_bitboards(board)
    current_player = player_0 if b == 0 else player_1
    opponent = player_1 if b == 0 else player_0
    bit_index = x * 8 + y

    if (current_player | opponent) & (1 << bit_index):  # すでに駒がある場合
        return []

    flippable = []
    directions = [-8, 8, -1, 1, -9, -7, 7, 9]  # 各方向のビットシフト
    for direction in directions:
        temp = []
        shift = direction
        prev_bit_index = bit_index
        mask_index = bit_index + shift
        while 0 <= mask_index < 64 and (opponent & (1 << mask_index)) and is_adjacent(prev_bit_index, mask_index):
            temp.append((mask_index // 8, mask_index % 8))
            shift += direction
            prev_bit_index = mask_index
            mask_index = bit_index + shift
        if 0 <= mask_index < 64 and (current_player & (1 << mask_index)) and is_adjacent(prev_bit_index, mask_index):
            flippable.extend(temp)

    return flippable

# 現在のボードで駒を置ける場所を計算する
def calculate_valid_moves(player_0, player_1, b):
    # player_0, player_1 = board_to_bitboards(board)
    current_player = player_0 if b == 0 else player_1
    opponent = player_1 if b == 0 else player_0

    valid_moves = []
    empty = ~(current_player | opponent) & ((1 << 64) - 1)
    directions = [-8, 8, -1, 1, -9, -7, 7, 9]

    for i in range(64):
        if (empty >> i) & 1:  # 空きマスの場合のみ検討
            for direction in directions:
                shift = direction
                mask_index = i + shift

                # 範囲外や無効な方向をスキップ
                if mask_index < 0 or mask_index >= 64 or not is_valid_move_within_bounds(i, shift):
                    continue

                mask = 1 << mask_index
                has_opponent = False

                # 方向ごとに駒を確認
                while mask_index >= 0 and mask_index < 64 and (opponent & mask) and is_valid_move_within_bounds(i, shift):
                    has_opponent = True
                    shift += direction
                    mask_index = i + shift
                    if mask_index < 0 or mask_index >= 64:
                        break
                    mask = 1 << mask_index

                # 相手の駒を挟むように自分の駒がある場合、有効手とする
                if has_opponent and 0 <= mask_index < 64 and (current_player & mask):
                    valid_moves.append((i // 8, i % 8))
                    break

    return valid_moves

# 特定の方向に移動した場合にボードの境界条件を満たすか確認する
def is_valid_move_within_bounds(index, direction):
    row, col = index // 8, index % 8
    new_row, new_col = (index + direction) // 8, (index + direction) % 8

    if debug and (row, col) == (0, 7):
        ic(row, col, new_row, new_col, direction)

    # 水平方向のチェック
    if direction in [-1, 1] and row != new_row:
        return False
    # 斜め方向のチェック
    if direction in [-7, -9, 7, 9] and abs(row - new_row) != abs(col - new_col):
        return False

    # ボード全体の範囲内かどうか
    return 0 <= new_row < 8 and 0 <= new_col < 8


def othellomachine(player_0, player_1, b, move):
    x, y = move
    bit_index = x * 8 + y
    # if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] != -1:
    #     return False, b, board, None, None, None
    if (player_0 | player_1) & (1 << bit_index):  # すでに駒がある場合
        return False, b, player_0, player_1, None, None, None

    flippable_cells = get_flippable_cells(player_0, player_1, b, x, y)  # 変更
    if not flippable_cells:
        return False, b, player_0, player_1, None, None, None

    # 駒を置く
    # player_0, player_1 = board_to_bitboards(board)
    current_player = player_0 if b == 0 else player_1
    opponent = player_1 if b == 0 else player_0

    # bit_index = x * 8 + y  # すでに計算済み
    current_player |= 1 << bit_index
    for fx, fy in flippable_cells:
        flip_index = fx * 8 + fy
        current_player |= 1 << flip_index
        opponent &= ~(1 << flip_index)

    if b == 0:
        player_0, player_1 = current_player, opponent
    else:
        player_0, player_1 = opponent, current_player

    # board = bitboards_to_board(player_0, player_1)

    # スコア計算
    # scores = (
    #     sum(row.count(0) for row in board),
    #     sum(row.count(1) for row in board)
    # )
    scores = (popcount(player_0), popcount(player_1))

    # 次に置けるマスを計算
    valid_cells = calculate_valid_moves(player_0, player_1, 1 - b)  # 変更
    n = len(valid_cells)

    return True, b, player_0, player_1, scores, n, valid_cells
