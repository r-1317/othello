import pygame
import sys

# 定数の設定
WINDOW_SIZE = 1000  # ウィンドウサイズを大きくする
INFO_WIDTH = 300  # 右側の情報表示エリアの幅を大きくする
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
    screen = pygame.display.set_mode((TOTAL_WIDTH, WINDOW_SIZE), pygame.SRCALPHA)
    pygame.display.set_caption('Visualizer')
    return screen

def draw_text_with_outline(screen, text, font, color, outline_color, pos):
    outline_text = font.render(text, True, outline_color)
    screen.blit(outline_text, (pos[0] - 1, pos[1] - 1))
    screen.blit(outline_text, (pos[0] + 1, pos[1] - 1))
    screen.blit(outline_text, (pos[0] - 1, pos[1] + 1))
    screen.blit(outline_text, (pos[0] + 1, pos[1] + 1))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

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
            font = pygame.font.SysFont(None, 36)  # フォントサイズを大きくする
            draw_text_with_outline(screen, f'({i},{j})', font, MAGENTA, WHITE, (j * CELL_SIZE + 10, i * CELL_SIZE + 10))  # 縁取りを白に変更
    # 次に置けるマスの描画
    for (i, j) in valid_cells:
        rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect, 5)  # 枠線の太さを調整

def draw_info(screen, turn, scores, n, game_finished):
    font = pygame.font.SysFont(None, 48)  # フォントサイズを大きくする
    info_x = WINDOW_SIZE + 20
    info_y = 20

    # 手番の表示
    player = "Black" if turn == 1 else "White"
    draw_text_with_outline(screen, f"Turn: {player}", font, WHITE, BLACK, (info_x, info_y))  # 縁取りを追加

    # スコアの表示
    info_y += 70  # 行間を調整
    draw_text_with_outline(screen, f"White: {scores[0]}", font, WHITE, BLACK, (info_x, info_y))  # 縁取りを追加
    info_y += 60  # 行間を調整
    draw_text_with_outline(screen, f"Black: {scores[1]}", font, WHITE, BLACK, (info_x, info_y))  # 縁取りを追加

    # 駒を置ける場所の数の表示
    info_y += 70  # 行間を調整
    if game_finished:
        draw_text_with_outline(screen, "Finish", font, RED, WHITE, (info_x, info_y))  # 縁取りを追加
    else:
        draw_text_with_outline(screen, f"Valid Moves: {n}", font, WHITE, BLACK, (info_x, info_y))  # 縁取りを追加

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