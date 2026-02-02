# 運命の数字 Writeup

## 問題概要
1から100までの数字を5回連続で当てるゲームです。
サーバーのソースコード `server.py` が提供されており、接続先は `nc 10.2.4.10 10007` です。

## 解法

### 1. ソースコードの分析
提供された `server.py` を確認すると、以下の処理が見つかります。

```python
41:         current_time = int(time.time())
42:         random.seed(current_time)
43: 
44:         conn.sendall(b"=== Oracle of Numbers ===\n")
45:         conn.sendall(f"Seed: {current_time}\n".encode())
```

サーバーは乱数のシード（種）として現在時刻（`time.time()`）を使用しており、さらにその値をクライアントに送信しています。

### 2. 脆弱性の特定
Pythonの `random` モジュールは疑似乱数生成器（PRNG）を使用しています。**同じシード値で初期化された場合、生成される乱数の列は常に同じになります。**

この問題では、シード値が与えられているため、手元の環境で同じシード値を使って `random.seed(seed)` を実行することで、サーバーが生成する乱数を完全に予測することができます。

### 3. エクスプロイトコードの作成
以下の手順を行うスクリプトを作成します。

1. サーバーに接続し、表示される `Seed` を取得する。
2. 取得した `Seed` でローカルの乱数生成器を初期化する。
3. サーバーと同じロジック（`random.randint(1, 100)`）で乱数を5つ生成する。
4. 生成した乱数を順番にサーバーに送信する。

実装したソルバースクリプト (`solve.py`) は以下の通りです。

```python
import socket
import re
import random

HOST = '10.2.4.10'
PORT = 10007

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # シードの受信
    buffer = ""
    while "Enter your guess" not in buffer:
        data = s.recv(1024).decode()
        if not data: break
        buffer += data
    
    match = re.search(r"Seed: (\d+)", buffer)
    if not match:
        print("Seed not found")
        return
        
    seed = int(match.group(1))
    print(f"[+] Seed: {seed}")
    
    # 乱数予測
    random.seed(seed)
    targets = [random.randint(1, 100) for _ in range(5)]
    
    # 解答の送信
    for t in targets:
        print(f"Sending: {t}")
        s.sendall(f"{t}\n".encode())
        res = s.recv(4096).decode()
        print(f"Response: {res.strip()}")
        if "Correct" not in res:
            # 次のプロンプトの中にCorrectが含まれている場合もあるため、簡易的なチェック
            pass

    # フラグの受信
    s.settimeout(2)
    try:
        while True:
            extra = s.recv(1024).decode()
            if not extra: break
            print(extra)
    except:
        pass
    s.close()

if __name__ == "__main__":
    solve()
```

### 4. 実行結果
スクリプトを実行すると、全問正解しフラグが得られます。

```
The secret is: flag{r4nd0m_1s_n0t_s0_r4nd0m}
```

## FLAG
`flag{r4nd0m_1s_n0t_s0_r4nd0m}`
