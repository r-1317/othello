import othellomachine
import visualizer
import pygame
import sys

def main():
    while True:
        # 初期ボードの設定
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
        turn = 1  # 1: 黒, 0: 白
        scores = (2, 2)
        valid_cells = othellomachine.calculate_valid_moves(board, turn)
        n = len(valid_cells)
        game_finished = False

        screen = visualizer.initialize_pygame()

        while True:
            # ボードの表示
            visualizer.visualize_othello(screen, turn, board, scores, n, valid_cells, game_finished)

            # ユーザーの入力を受け取る
            while True:
                move = input(f"Enter your next step (row col) for {'Black' if turn == 1 else 'White'}: ")
                try:
                    if len(move) == 2 and move.isdigit():
                        x, y = int(move[0]), int(move[1])
                    else:
                        x, y = map(int, move.split())
                    if (x, y) in valid_cells:
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter row and col as integers.")

            # オセロマシーンを実行
            status, turn, board, scores, n, valid_cells = othellomachine.othellomachine(board, turn, (x, y))

            if n == 0:
                game_finished = True
                visualizer.visualize_othello(screen, turn, board, scores, n, valid_cells, game_finished)
                while True:
                    choice = input("Game finished. Enter 'restart' to play again or 'exit' to quit: ").strip().lower()
                    if choice == 'restart':
                        main()  # ゲームを再スタート
                    elif choice == 'exit':
                        pygame.quit()
                        sys.exit()
                    else:
                        print("Invalid choice. Please enter 'restart' or 'exit'.")
                continue

            if not status:
                print("Invalid move. Try again.")
                continue

            # 手番を交代
            turn = 1 - turn

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()