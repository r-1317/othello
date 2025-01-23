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

# 駒を置いたときにひっくり返せる座標のリストを返す
def get_flippable_cells(board, b, x, y):
    player_0, player_1 = board_to_bitboards(board)
    current_player = player_0 if b == 0 else player_1
    opponent = player_1 if b == 0 else player_0
    bit_index = x * 8 + y

    if (current_player | opponent) & (1 << bit_index):  # すでに駒がある場合
        return []

    flippable = []
    directions = [-8, 8, -1, 1, -9, -7, 7, 9]  # 各方向のビットシフト
    for direction in directions:
        temp = []
        mask = 1 << (bit_index + direction)
        while 0 <= (bit_index + direction) < 64 and (opponent & mask):
            temp.append(((bit_index + direction) // 8, (bit_index + direction) % 8))
            direction += direction
            mask = 1 << (bit_index + direction)
        if 0 <= (bit_index + direction) < 64 and (current_player & mask):
            flippable.extend(temp)

    return flippable

# 現在のボードで駒を置ける場所を計算する
def calculate_valid_moves(board, b):
    player_0, player_1 = board_to_bitboards(board)
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

    # 水平方向のチェック
    if direction in [-1, 1] and row != new_row:
        return False

    # ボード全体の範囲内かどうか
    return 0 <= new_row < 8 and 0 <= new_col < 8


def othellomachine(board, b, move):
    x, y = move
    if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] != -1:
        return False, b, board, None, None, None

    flippable_cells = get_flippable_cells(board, b, x, y)
    if not flippable_cells:
        return False, b, board, None, None, None

    # 駒を置く
    player_0, player_1 = board_to_bitboards(board)
    current_player = player_0 if b == 0 else player_1
    opponent = player_1 if b == 0 else player_0

    bit_index = x * 8 + y
    current_player |= 1 << bit_index
    for fx, fy in flippable_cells:
        flip_index = fx * 8 + fy
        current_player |= 1 << flip_index
        opponent &= ~(1 << flip_index)

    if b == 0:
        player_0, player_1 = current_player, opponent
    else:
        player_0, player_1 = opponent, current_player

    board = bitboards_to_board(player_0, player_1)

    # スコア計算
    scores = (
        sum(row.count(0) for row in board),
        sum(row.count(1) for row in board)
    )

    # 次に置けるマスを計算
    valid_cells = calculate_valid_moves(board, 1 - b)
    n = len(valid_cells)

    return True, b, board, scores, n, valid_cells
