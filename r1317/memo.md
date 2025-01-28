# 課題4  オセロゲーム

## 最初の方針
- minimax
  - chokudaiサーチも組み込みたい

### 測定
4 5 6 4 6 5 10 10 6 5 4 5 6 6 6 6 5 5 4 5 6 6 10 7 3 3 4 3 3 1<br>
4 5 9 9 6 9 13 8 9 12 14 15 18 18 17 12 9 13 12 11 9 10 8 7 5 6 1 0 1<br>
平均9.310344827586206
- 10で見積もっていいかな

## ゲーム木をどうするか
- グローバル変数
### 構造
- 長さ65の配列
  - 現在の石の数
- 要素数2の配列
  - 次の手番の色
- 各要素として辞書
  - 盤面をkeyとし、現時点でのスコアと次の盤面の配列をvalueにもつ

### 盤面同士の前後関係
- 木ではなくても

## まずはminimax
- DFSなのかな
- 再起関数
- 計算結果は保存しない
  - プログラムを単純にするため

### 評価値
原典は不明だが、複数のサイトで使われている
```
[
  [120, -20,  20,   5,   5,  20, -20, 120],
  [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
  [ 20,  -5,  15,   3,   3,  15,  -5,  20],
  [  5,  -5,   3,   3,   3,   3,  -5,   5],
  [  5,  -5,   3,   3,   3,   3,  -5,   5],
  [ 20,  -5,  15,   3,   3,  15,  -5,  20],
  [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
  [120, -20,  20,   5,   5,  20, -20, 120]
]
```

## minimax詳細
- 再起関数を用いて、深さnまで探索
- n層に到達するか最後まで行くかで終了
- 評価は、置かれている石に上の倍率をかけたものの(自分 - 相手)
- 最後まで行く場合、枚数の差*10**5を評価値とする
  - 勝ち確なら常に最高点、負け確なら常に最低点
- 次の手がなかったら手番の交代(パス)
  - それでも手がなかったら最後まで行ったのと同じ扱い

## minimax結果
### N = 4
- win_count: 44, lose_count: 4, draw_count: 2
- 勝率: 0.917

# 勝敗表
- r1317に対し、AIが勝ったかどうか
## bitboard_minimax
- 1 
## alphabeta (N = 5)
- 内容は同じなので、上と合算してもよい

## 今後の方針
- α-β法がわかるようでわからん
- 評価値を変えるとか
- 終盤まで角重視なのも違う
- 割とchokudaiサーチ的なのやりたい
  - 実装が大変な割に弱そう
  - そもそもchokudaiサーチはオセロで使えるのか？
- パターン評価が良いらしい
- https://note.com/nyanyan_cubetech/n/nb6067ce73ccd

## othellomachine修正
- 隣接マスの判定がおかしい
- 

```
pygame 2.6.1 (SDL 2.28.4, Python 3.10.12)
Hello from the pygame community. https://www.pygame.org/contribute.html
Enter your next step (row col) for White: 2 4
ic| move: (4, 5), score: -4
AI's move: 4 5
Enter your next step (row col) for White: 5 4
ic| move: (2, 3), score: -4
AI's move: 2 3
Enter your next step (row col) for White: 4 2
ic| move: (2, 5), score: 20
AI's move: 2 5
Enter your next step (row col) for White: 1 4
ic| move: (0, 5), score: 33
AI's move: 0 5
Enter your next step (row col) for White: 0 4
ic| move: (0, 3), score: 51
AI's move: 0 3
Enter your next step (row col) for White: 3 6
ic| move: (6, 4), score: 58
AI's move: 6 4
Enter your next step (row col) for White: 1 5
ic| move: (2, 2), score: 75
AI's move: 2 2
Enter your next step (row col) for White: 7 4
ic| move: (3, 5), score: 84
AI's move: 3 5
Enter your next step (row col) for White: 3 2
ic| move: (5, 2), score: 95
AI's move: 5 2
Enter your next step (row col) for White: 1 3
ic| move: (5, 5), score: 110
AI's move: 5 5
Enter your next step (row col) for White: 3 1
ic| move: (2, 1), score: 103
AI's move: 2 1
Enter your next step (row col) for White: 1 2
ic| move: (0, 2), score: 109
AI's move: 0 2
Enter your next step (row col) for White: 2 0
ic| move: (4, 0), score: 97
AI's move: 4 0
Enter your next step (row col) for White: 4 1
ic| move: (4, 6), score: 96
AI's move: 4 6
Enter your next step (row col) for White: 4 7
ic| move: (5, 1), score: 95
AI's move: 5 1
Enter your next step (row col) for White: 6 0
ic| move: (5, 3), score: 123
AI's move: 5 3
Enter your next step (row col) for White: 5 6
ic| move: (6, 2), score: 126
AI's move: 6 2
Enter your next step (row col) for White: 2 6
ic| move: (2, 7), score: 143
AI's move: 2 7
Enter your next step (row col) for White: 1 1
ic| move: (5, 7), score: 161
AI's move: 5 7
Enter your next step (row col) for White: 7 2
ic| move: (0, 0), score: 197
AI's move: 0 0
Enter your next step (row col) for White: 1 0
ic| move: (5, 0), score: 385
AI's move: 5 0
Enter your next step (row col) for White: 6 5
ic| move: (3, 7), score: 413
AI's move: 3 7
Enter your next step (row col) for White: 1 6 
ic| move: (6, 3), score: 518
AI's move: 6 3
Enter your next step (row col) for White: 7 3
ic| move: (0, 7), score: 593
AI's move: 0 7
Enter your next step (row col) for White: 0 6
ic| move: (7, 0), score: 594
AI's move: 7 0
Enter your next step (row col) for White: 6 1
ic| move: (0, 1), score: 781
AI's move: 0 1
No valid moves for White. Pass to Black.
ic| move: (3, 0), score: 772
AI's move: 3 0
No valid moves for White. Pass to Black.
ic| move: (6, 7), score: 664
AI's move: 6 7
Enter your next step (row col) for White: 6 6
ic| move: (1, 7), score: 46
AI's move: 1 7
No valid moves for White. Pass to Black.
ic| move: (7, 7), score: 46
AI's move: 7 7
Enter your next step (row col) for White: 7 6
ic| move: (7, 5), score: 46
AI's move: 7 5
No valid moves for White. Pass to Black.
ic| move: (7, 1), score: 46
AI's move: 7 1
```