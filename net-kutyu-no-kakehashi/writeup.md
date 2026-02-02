# 空中の架け橋 - Writeup

## 問題概要

- **ポイント**: 30
- **カテゴリ**: Network
- **説明**: ある工場内の無線LAN通信をキャプチャしました。キャプチャファイルを解析し、フラグを取得してください。
- **添付ファイル**: Plant.cap (SHA1: 5cdb6a8b0cd45ec27730b0b4a6f178f63baef687)
- **解答形式**: flag{XXXXXX} (半角英数記号)

## 解法

### Step 1: キャプチャファイルの確認

まず、キャプチャファイルの種類を確認します。

```bash
file Plant.cap
# 出力: Plant.cap: pcap capture file, microsecond ts (little-endian) - version 2.4 (802.11, capture length 65535)
```

802.11（無線LAN）のキャプチャファイルであることがわかります。

### Step 2: 無線LANパスワードのクラック

`aircrack-ng`でキャプチャファイルを解析します。

```bash
aircrack-ng Plant.cap
```

出力から以下の情報が判明します：

- **BSSID**: 00:00:E8:6E:6E:5A
- **ESSID**: CTF_Challenge
- **暗号化**: WPA (1 handshake)

WPAハンドシェイクが含まれているため、辞書攻撃でパスワードをクラックできます。

```bash
aircrack-ng -w rockyou.txt Plant.cap
```

または簡単なパスワードリストを使用：

```
KEY FOUND! [ password123 ]
```

### Step 3: 通信の復号化

取得したパスワードを使用して通信を復号化します。

```bash
airdecap-ng -e CTF_Challenge -p password123 Plant.cap
```

出力：

```
Total number of WPA data packets       493
Number of decrypted WPA  packets       472
```

これにより `Plant-dec.cap` という復号化されたファイルが生成されます。

### Step 4: HTTP通信の分析

復号化されたキャプチャからHTTPオブジェクトを抽出します。

```bash
tshark -r Plant-dec.cap -Y "http" --export-objects http,http_objects
```

工場プラント監視システム（SCADA）へのWeb通信が確認できます。

#### ログインリクエストの発見

```json
{
  "username": "admin",
  "password": "RUgSWSnENkGwF5XxpYJDN3TkPAVEsEiOmS8ys6tj"
}
```

パスワードは何らかの形で暗号化されています。

### Step 5: 暗号鍵の発見

`/api/devices` と `/api/users` のレスポンスを確認すると、暗号化の情報が漏洩しています。

```json
{
  "crypto": {
    "key": "PLANT_ChaCha20_SecretKey_2026!!",
    "nonce": "PLC_N0nc3_!!",
    "algorithm": "ChaCha20"
  }
}
```

および

```json
{
  "chacha_key": "PLANT_ChaCha20_SecretKey_2026!!",
  "chacha_nonce": "PLC_N0nc3_!!"
}
```

### Step 6: ChaCha20復号化

暗号化されたパスワードはBase64エンコードされたChaCha20暗号文です。取得した鍵とnonceを使用して復号化します。

```python
#!/usr/bin/env python3
import base64

# ChaCha20 parameters
key = b"PLANT_ChaCha20_SecretKey_2026!!"  # 31 bytes
nonce = b"PLC_N0nc3_!!"  # 12 bytes

# Encrypted password (base64 encoded)
encrypted_b64 = "RUgSWSnENkGwF5XxpYJDN3TkPAVEsEiOmS8ys6tj"
encrypted = base64.b64decode(encrypted_b64)

# ChaCha20 decryption (implementation omitted for brevity)
decrypted = chacha20_decrypt(key, nonce, encrypted)
print(decrypted.decode('utf-8'))
# 出力: flag{Ch4Ch4_Str34m_Vuln3r4bl3}
```

## フラグ

```
flag{Ch4Ch4_Str34m_Vuln3r4bl3}
```

## 学んだこと

1. **無線LANセキュリティ**: WPAで保護された無線LANでも、弱いパスワード（例：password123）を使用していると辞書攻撃により短時間でクラックされる
2. **APIセキュリティ**: APIレスポンスに暗号鍵などの機密情報を含めてはならない
3. **ChaCha20暗号**: 高速なストリーム暗号だが、鍵が漏洩すると容易に復号化される

## 使用ツール

- `aircrack-ng` - 無線LANパスワードクラック
- `airdecap-ng` - WPA通信の復号化
- `tshark` - パケット解析
- Python - ChaCha20復号化
