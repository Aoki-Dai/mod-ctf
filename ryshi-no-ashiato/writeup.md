# 量子の足音 Writeup

## 問題概要

- **カテゴリ**: 暗号（Crypto）
- **ポイント**: 30
- **フラグ**: `flag{w34k_n0nc3_r3us3}`

ML-DSA（FIPS 204、旧称 CRYSTALS-Dilithium）署名サーバーに「独自の簡略化」が施されており、秘密鍵 `s1` を復元する問題でした。

## 背景知識

### ML-DSA（Module-Lattice Digital Signature Algorithm）

ML-DSAは、格子暗号ベースの耐量子計算機暗号署名方式です。2024年8月にNISTがFIPS 204として標準化しました。

### 署名生成式

```
z = y + c * s1  (mod Q, in Z_Q[X]/(X^256 + 1))
```

- `z`: 署名の一部（公開される）
- `y`: ランダムなノンス/マスキングベクトル（秘密）
- `c`: チャレンジ多項式（メッセージと公開鍵から計算）
- `s1`: 秘密鍵の一部
- `*`: 多項式乗算（negacyclic、mod X^256 + 1）
- `Q = 8380417`: モジュラス

## 脆弱性の発見

### 観察1: 署名データの構造

サーバーに接続して署名を取得すると、以下の形式でデータが返されました：

- `z`: 2つの多項式（各256係数）
- `c`: 1つのsparse多項式（ほとんどが0で、±1のみ）

### 観察2: 複数署名の比較

複数の署名を取得して比較すると、`z` の値がメッセージによってわずかに異なることが分かりました：

```
Signature 0: z[0][:5] = [8341420, 9558, 61417, 16655, 8271553]
Signature 1: z[0][:5] = [8341424, 9553, 61432, 16645, 8271557]
差分（dz）:            = [4, -5, 15, -10, 4]
```

差分が非常に小さい（-20～20程度）ことから、**同じノンス y が再利用されている**ことが推測できました。

## 攻撃手法：ノンス再利用攻撃

### 数学的根拠

ノンス y が固定の場合：

```
z1 = y + c1 * s1
z2 = y + c2 * s1
```

差を取ると：

```
dz = z1 - z2 = (c1 - c2) * s1 = dc * s1
```

これにより、`dc` と `dz` から `s1` を求める問題に帰着します。

### 多項式乗算を線形方程式として表現

Negacyclic多項式乗算 `dc * s1 = dz` は、以下の行列演算として表現できます：

```
M @ s1 = dz (mod Q)
```

ここで `M` は `dc` から構築されるToeplitz-like行列です：

```python
def build_negacyclic_matrix(c):
    M = np.zeros((N, N), dtype=np.int64)
    for k in range(N):
        for i in range(N):
            if i <= k:
                j = k - i
                M[k, j] = (M[k, j] + c[i]) % Q
            else:
                j = N + k - i
                M[k, j] = (M[k, j] - c[i]) % Q  # negacyclic: X^N = -1
    return M
```

### 線形方程式の求解

Gaussian elimination を mod Q で実行して s1 を求めます。

## 解法スクリプト

```python
#!/usr/bin/env python3
import socket
import json
import re
import numpy as np

Q = 8380417
N = 256

def build_negacyclic_matrix(c):
    M = np.zeros((N, N), dtype=np.int64)
    for k in range(N):
        for i in range(N):
            if i <= k:
                j = k - i
                M[k, j] = (M[k, j] + c[i]) % Q
            else:
                j = N + k - i
                M[k, j] = (M[k, j] - c[i]) % Q
    return M

def solve_mod_q(M, b, q=Q):
    # Gaussian elimination mod Q
    n = M.shape[0]
    aug = np.hstack([M.copy(), b.reshape(-1, 1)])
    aug = aug.astype(object)

    for col in range(n):
        pivot_row = None
        for row in range(col, n):
            if aug[row, col] % q != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        aug[[col, pivot_row]] = aug[[pivot_row, col]]
        pivot_inv = pow(int(aug[col, col]) % q, -1, q)
        aug[col] = (aug[col] * pivot_inv) % q

        for row in range(col + 1, n):
            if aug[row, col] % q != 0:
                factor = aug[row, col]
                aug[row] = (aug[row] - factor * aug[col]) % q

    x = np.zeros(n, dtype=object)
    for col in range(n - 1, -1, -1):
        if aug[col, col] % q == 0:
            x[col] = 0
        else:
            x[col] = aug[col, n]
            for j in range(col + 1, n):
                x[col] = (x[col] - aug[col, j] * x[j]) % q
            x[col] = (x[col] * pow(int(aug[col, col]), -1, q)) % q

    return np.array([int(v) for v in x])

# 1. 2つの署名を取得
# 2. dc = c1 - c0, dz = z1 - z0 を計算
# 3. negacyclic行列 M を構築
# 4. s1 = solve(M, dz) で秘密鍵を復元
# 5. 復元した s1 をサーバーに送信してフラグを取得
```

## 結果

復元された秘密鍵 s1 は、全ての係数が -2 から 2 の範囲（ML-DSA-44 の η=2 に一致）でした：

```
s1[0][:20]: [0, -2, 1, 1, 2, 2, -1, 2, -1, -1, 1, -2, 0, 0, -2, -2, 2, 1, 1, 1]
s1[1][:20]: [1, 0, -1, 0, 2, 1, 1, 1, 0, -2, -2, 0, 0, 2, 2, 0, 2, 0, 1, -1]
```

これをサーバーに送信してフラグを取得しました。

## 教訓

1. **ノンス（乱数）の再利用は致命的**: ECDSA のような他の署名方式でも同様で、ノンス再利用は秘密鍵の漏洩に直結します。
2. **暗号実装の「簡略化」は危険**: 標準仕様を勝手に変更すると、セキュリティ上の問題を引き起こす可能性があります。
3. **耐量子暗号も古典的な実装ミスには弱い**: ML-DSAは量子コンピュータに対して安全ですが、ノンス再利用のような実装ミスは従来の手法で攻撃可能です。

## フラグ

```
flag{w34k_n0nc3_r3us3}
```

（weak nonce reuse = 弱いノンス再利用）
