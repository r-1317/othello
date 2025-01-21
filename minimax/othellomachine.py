def get_flippable_cells(board, b, x, y):
    # 駒を置いたときにひっくり返せる座標のリストを返す
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # 8方向
    flippable = [] # ひっくり返せる座標のリスト
    for dx, dy in directions: # 8方向について
        nx, ny = x + dx, y + dy # 1マス先
        temp = []
        # 相手の駒が続く限りtempに座標を追加
        while 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == 1 - b: 
            temp.append((nx, ny))
            nx += dx
            ny += dy
        # 相手の駒の後に自分の駒がある場合、flippableにtempを全部追加
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] == b and temp:
            flippable.extend(temp)
    return flippable

def calculate_valid_moves(board, b):
    # 現在のボードで駒を置ける場所を計算する
    valid_moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == -1 and get_flippable_cells(board, b, i, j):
                valid_moves.append((i, j))
    return valid_moves

def othellomachine(board, b, move):
    # 入力形式のチェック
    x, y = move
    if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] != -1:
        return False, b, board, None, None, None

    # 駒を置けるかチェック
    flippable_cells = get_flippable_cells(board, b, x, y)
    if not flippable_cells:
        return False, b, board, None, None, None

    # 駒を置く
    board[x][y] = b
    for fx, fy in flippable_cells:
        board[fx][fy] = b

    # スコア計算
    scores = (
        sum(row.count(0) for row in board),
        sum(row.count(1) for row in board)
    )

    # 次に置けるマスを計算
    valid_cells = calculate_valid_moves(board, 1 - b)
    n = len(valid_cells)

    return True, b, board, scores, n, valid_cells