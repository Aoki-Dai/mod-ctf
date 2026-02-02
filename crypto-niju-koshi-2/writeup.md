# 二重の格子 (Double Lattice) Writeup

## 問題概要

- **カテゴリ**: 暗号 (Crypto)
- **得点**: 20点
- **問題文**: 古い書庫から、古典暗号を二重に用いた文書が発見されました。外側の暗号を解読すると、内側の暗号の鍵が判明します。

## 暗号文

```
EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV
LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR
YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU
```

## 解法

### ステップ1: 外側の暗号の特定

ヒント1より、外側の暗号は**多表式換字暗号（ヴィジュネル暗号）**であることが分かりました。

まず、Kasiski検定とIndex of Coincidence（一致指数）分析を行って鍵の長さを推定しました：

```python
# 繰り返しパターン "HJV" が位置41と59で発見（距離18）
# 因数: 2, 3, 6, 9, 18
# 鍵長6のICが0.0467と高い値を示す
```

### ステップ2: ヴィジュネル暗号の解読

一般的な暗号学用語を鍵として試したところ、**「CRYPTO」**が正解でした。

```python
def decrypt_vigenere(ciphertext, key):
    key = key.upper()
    plaintext = []
    key_idx = 0
    for char in ciphertext:
        if char in string.ascii_uppercase:
            shift = ord(key[key_idx % len(key)]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            plaintext.append(decrypted_char)
            key_idx += 1
    return "".join(plaintext)
```

**復号結果**:

```
CONGRATULATIONS YOU HAVE SUCCESSFULLY DECODED THE OUTER ENCRYPTION
THE KEY IS MONARCHY
UGSUTCNAGCMVBOUFDMMBEFKZCFQPNBIOKABEVFKMPDFGSMIKTSMLGMXFDLNMSB
```

### ステップ3: 内側の暗号の特定

**「MONARCHY」**は暗号学で有名なPlayfair暗号の例題で使われる鍵です。
残りの暗号文をPlayfair暗号として解読します。

### ステップ4: Playfair暗号の解読

Playfairマトリックス（鍵: MONARCHY）:

```
M O N A R
C H Y B D
E F G I K
L P Q S T
U V W X Z
```

```python
def decrypt_playfair(ciphertext, key):
    # 5x5マトリックスを作成（JはIと同一視）
    # 2文字ずつのペアで復号
    # - 同じ行: 左にシフト
    # - 同じ列: 上にシフト
    # - それ以外: 矩形のルールで置換
```

**復号結果**:

```
WELL DONE YOU HAVE CRACKED THE PLAYFAIR CIPHER
THE FLAG IS QUEENVICTORIA
```

（"WELXLDONE"の"X"はPlayfair暗号で同じ文字が連続する場合に挿入されるパディング文字）

## フラグ

```
flag{queenvictoria}
```

## 使用した暗号技術

1. **ヴィジュネル暗号 (Vigenère Cipher)**
   - 16世紀にブレーズ・ド・ヴィジュネルが発明した多表式換字暗号
   - 鍵の各文字に対応するシフト量でアルファベットをずらす

2. **Playfair暗号**
   - 1854年にチャールズ・ホイートストンが発明
   - 5x5のマトリックスを使用し、2文字ずつのダイグラフ（二重文字）単位で暗号化
   - 同じ文字が連続する場合はXなどのパディング文字を挿入

## 学んだこと

- 二重暗号の解読では、外側の暗号を解くと内側の暗号のヒントが得られることがある
- MONARCHYはPlayfair暗号の有名な例題鍵
- 古典暗号の組み合わせは現代でもCTFの問題として出題される
