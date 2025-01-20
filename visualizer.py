import pygame
import sys

# 定数の設定
WINDOW_SIZE = 800
INFO_WIDTH = 200  # 右側の情報表示エリアの幅
TOTAL_WIDTH = WINDOW_SIZE + INFO_WIDTH
GRID_SIZE = 8
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)

def initialize_pygame():
    pygame.init()
    screen = pygame.display.set_mode((TOTAL_WIDTH, WINDOW_SIZE))
    pygame.display.set_caption('Visualizer')
    return screen

def draw_board(screen, board, valid_cells):
    screen.fill(GREEN)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if board[i][j] == 0:  # 白の駒
                pygame.draw.circle(screen, WHITE, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                pygame.draw.circle(screen, BLACK, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5, 2)
            elif board[i][j] == 1:  # 黒の駒
                pygame.draw.circle(screen, BLACK, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            # 各マスに座標を表示
            font = pygame.font.SysFont(None, 24)
            text = font.render(f'({i},{j})', True, MAGENTA)
            screen.blit(text, (j * CELL_SIZE + 5, i * CELL_SIZE + 5))
    # 次に置けるマスの描画
    for (i, j) in valid_cells:
        rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect, 3)

def draw_info(screen, turn, scores, n, game_finished):
    font = pygame.font.SysFont(None, 36)
    info_x = WINDOW_SIZE + 20
    info_y = 20

    # 手番の表示
    player = "Black" if turn == 1 else "White"
    text = font.render(f"Turn: {player}", True, WHITE)
    screen.blit(text, (info_x, info_y))

    # スコアの表示
    info_y += 50
    text = font.render(f"White: {scores[0]}", True, WHITE)
    screen.blit(text, (info_x, info_y))
    info_y += 40
    text = font.render(f"Black: {scores[1]}", True, WHITE)
    screen.blit(text, (info_x, info_y))

    # 駒を置ける場所の数の表示
    info_y += 50
    if game_finished:
        text = font.render("Finish", True, RED)
    else:
        text = font.render(f"Valid Moves: {n}", True, WHITE)
    screen.blit(text, (info_x, info_y))

def visualize_othello(screen, turn, board, scores, n, valid_cells, game_finished):
    draw_board(screen, board, valid_cells)
    draw_info(screen, turn, scores, n, game_finished)
    pygame.display.flip()

# テスト用のデータ
if __name__ == "__main__":
    screen = initialize_pygame()
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
    n = 0  # 置ける場所がない場合
    valid_cells = []
    game_finished = True

    visualize_othello(screen, turn, board, scores, n, valid_cells, game_finished)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()