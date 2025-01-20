import matplotlib.pyplot as plt
import numpy as np

def visualize_othello(turn, board, scores, n, valid_cells):
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(0.5, 8.5, 1))
    ax.set_yticks(np.arange(0.5, 8.5, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)

    # 背景色の設定
    ax.set_facecolor('green')

    # ボードの描画
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:  # 白の駒
                circle = plt.Circle((j + 0.5, i + 0.5), 0.4, edgecolor='white', facecolor='white', linewidth=2)
            elif board[i][j] == 1:  # 黒の駒
                circle = plt.Circle((j + 0.5, i + 0.5), 0.4, color='black')
            else:
                continue
            ax.add_artist(circle)

    # 次に置けるマスの描画
    for (i, j) in valid_cells:
        rect = plt.Rectangle((j, i), 1, 1, linewidth=1, edgecolor='red', facecolor='none')
        ax.add_artist(rect)

    # タイトルとスコアの表示
    player = "Black" if turn == 1 else "White"
    plt.title(f"Turn: {player}\nScores - White: {scores[0]}, Black: {scores[1]}\nValid Moves: {n}")

    plt.show()

# テスト用のデータ
if __name__ == "__main__":
    board = [
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1,  0,  1, -1, -1, -1],
        [-1, -1, -1,  1,  0, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1]
    ]
    turn = 1
    scores = (2, 2)
    n = 4
    valid_cells = [(2, 3), (3, 2), (4, 5), (5, 4)]

    visualize_othello(turn, board, scores, n, valid_cells)