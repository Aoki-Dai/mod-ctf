細胞の回帰
このライフゲームのグリッドは2世代進行した後の状態です。

時が進む前の初期状態を見つけ出してください。

APIエンドポイント:
GET /problem - 問題データを取得（JSON形式）
GET /final_state - 最終状態をテキスト形式で取得
POST /submit - 解答を提出（初期状態のグリッド）
提出フォーマット:
POST /submit
Content-Type: application/json

{
  "initial_state": [[0,1,0,...], [1,0,1,...], ...]
}
グリッドは16x16の2次元配列（0と1）で指定してください。