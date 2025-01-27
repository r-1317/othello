import othellomachine
import visualizer
import pygame
import sys
import minimax

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
        # bitboardの初期化
        player_0 = 0b0000000000000000000000000001000000001000000000000000000000000000
        player_1 = 0b0000000000000000000000000000100000010000000000000000000000000000
        player_0 = 570818803794944
        player_1 = 149877719826432
        turn = 0  # 1: 黒(AI), 0: 白(人間) <- 人間が先手に変更
        scores = (2, 2)
        valid_cells = othellomachine.calculate_valid_moves(player_0, player_1, turn)
        n = len(valid_cells)
        game_finished = False

        screen = visualizer.initialize_pygame()

        while True:
            # ボードの表示
            board = othellomachine.bitboards_to_board(player_0, player_1)
            visualizer.visualize_othello(screen, turn, board, scores, n, valid_cells, game_finished)

            # ユーザーの入力を受け取る
            while True:
                # 人間の手番の場合
                if turn == 0:
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
                # AIの手番の場合
                else:
                    move = minimax.minimax(player_0, player_1)
                    x, y = move
                    print(f"AI's move: {x} {y}")
                    break


            # オセロマシーンを実行
            status, turn, player_0, player_1, scores, n, valid_cells = othellomachine.othellomachine(player_0, player_1, turn, (x, y))

            if n == 0:
                # 次の合法手がない場合、パス
                valid_cells = othellomachine.calculate_valid_moves(player_0, player_1, turn)
                n = len(valid_cells)
                turn = 1 - turn
                # 相手の合法手もない場合、ゲーム終了
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
                else:
                    print(f"No valid moves for {'Black' if turn == 1 else 'White'}. Pass to {'White' if turn == 1 else 'Black'}.")

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