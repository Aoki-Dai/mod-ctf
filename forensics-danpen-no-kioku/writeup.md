# Writeup: 断片の記憶 (Forensics)

## 問題概要

- **ファイル**: `challenge_binary`
- **概要**: 実行すると診断メッセージが表示されるバイナリファイルを解析し、フラグを取得する。
- **ヒント**:
  - `binwalk` で実行ファイル内の埋め込みデータを確認。
  - 削除されたファイルの復旧（カービング）。
  - 画像内の LSB ステガノグラフィの解析（`zsteg` など）。

## 解析手順

### 1. 埋め込みデータの確認

`binwalk` コマンドで `challenge_binary` を解析すると、ELF バイナリの後に **EXT ファイルシステム** が結合されていることがわかります。

```bash
binwalk challenge_binary
```

出力結果から、オフセット `0xAE360` 以降に約 50MB の EXT ファイルシステムが存在することが確認できました。

### 2. ファイルシステムの調査

抽出したファイルシステムイメージ（`embedded_fs.img`）の中身を調べると、`config.txt` に以下の記述がありました。

```text
[Archive Inventory]
# Files stored in evidence/ directory (before deletion):
# - incident_report.txt
# - access_log.txt
# - note.txt
# - critical_data.png

[Notes]
Some data may have been deliberately removed.
Recovery of deleted artifacts is recommended.
```

重要なデータである `critical_data.png` が削除されていることが示唆されています。

### 3. ファイルの復元（カービング）

`photorec` 等のツールを使用して、ファイルシステムイメージから削除された PNG ファイルを復元しました。
復元されたファイルの中に、元の `image1.png`～`image5.png` とは異なるデータ（`recovered_png_1.png`）が含まれていました。

### 4. ステガノグラフィの解析

復元された各画像の LSB（Least Significant Bit）を解析しました。Python の `Pillow` ライブラリを使用して、各ピクセルの RGB 値の最下位ビットを抽出するスクリプトを実行しました。

```python
from PIL import Image

def extract_lsb(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    bits = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits += str(r & 1) + str(g & 1) + str(b & 1)

    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            data.append(int(byte, 2))
    return data
```

この解析により、`recovered_png_1.png` から以下のフラグが抽出されました。

## フラグ

`flag{fr4gm3nt3d_m3m0ry_r3c0v3r3d}`
