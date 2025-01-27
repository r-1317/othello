# 知識科学概論 第4回発表会

## 評価方法

ランダムに手を打つやつに対しての勝率

## どんなアルゴリズムを使用したか

- MiniMax法
- AlphaBeta法
- NegaScout法

## オセロのサンプルや実装をどのように作ったのか

オセロマシーンと呼称

オセロマシーンの実装は、以下のような関数を使用して行った(othellomacine.pyを参照せよ)。

1. `get_flippable_cells(board, b, x, y)`: 駒を置いたときにひっくり返せる座標のリストを返す関数。8方向について相手の駒が続く限り座標を追加し、相手の駒の後に自分の駒がある場合にひっくり返せる座標をリストに追加する。

2. `calculate_valid_moves(board, b)`: 現在のボードで駒を置ける場所を計算する関数。空いているマスで、駒を置いたときにひっくり返せる座標がある場合、そのマスを有効な手としてリストに追加する。

3. `othellomachine(board, b, move)`: オセロの一手を実行する関数。入力形式のチェック、駒を置けるかのチェック、駒を置く処理、スコア計算、次に置けるマスの計算を行う。駒を置ける場合は`True`を返し、置けない場合は`False`を返す。

## 初期設定

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
pip install pygame
```

デバッグログが必要な場合はicecreamもインストール
```powershell
pip install icecream
```
