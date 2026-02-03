# CTF関連ツール一覧

以下は、インストール済みのHomebrewパッケージおよびGemの中からCTF（Capture The Flag）で役立つツールをまとめたものです。

---

## 🔐 ネットワーク解析

### aircrack-ng
**カテゴリ**: ワイヤレスネットワークセキュリティ

Wi-Fiネットワークのセキュリティ監査ツールスイート。WEP/WPA/WPA2の暗号化キーをクラックするために使用されます。

**CTFでの用途**:
- 無線LANキャプチャファイル（.cap）からパスワードを解析
- 辞書攻撃によるWi-Fiパスワードの解読

**依存関係** (brew):
- `openssl@3` - 暗号化ライブラリ
- `sqlite` - データベース
- `pcre2` - 正規表現ライブラリ

```bash
# 使用例: rockyou.txtを使った辞書攻撃
aircrack-ng -w /path/to/rockyou.txt capture.cap
```

---

### wireshark / wireshark-app
**カテゴリ**: ネットワークプロトコル解析

最も広く使われているネットワークプロトコルアナライザー。パケットキャプチャとリアルタイムのトラフィック分析が可能。

**CTFでの用途**:
- pcapファイルの解析
- HTTP、DNS、TCPなどの通信内容の調査
- 隠されたデータやフラグの発見
- 異常な通信パターンの検出

**依存関係** (brew):
- `gnutls` - TLS/SSL通信の解析
- `lua` - Luaスクリプトによるカスタム解析
- `libssh` - SSH通信の解析
- `libsmi` - SNMP MIBファイルの解析
- `c-ares` - 非同期DNS解決
- `glib` - ユーティリティライブラリ

```bash
# CLIでの使用例（tshark）
tshark -r capture.pcap -Y "http"
```

---

## 🔍 フォレンジック・解析

### binwalk
**カテゴリ**: ファームウェア解析

バイナリファイル内の埋め込みファイルやコードを解析・抽出するツール。

**CTFでの用途**:
- ファームウェアからファイルシステムを抽出
- 画像ファイルに隠されたデータの検出
- バイナリ内の隠しファイルの発見

**依存関係** (brew):
- `xz` - XZ圧縮の展開
- `zstd` - Zstandard圧縮の展開
- `squashfs` - SquashFSファイルシステムの展開

```bash
# 使用例: ファイルの解析と抽出
binwalk -e firmware.bin
binwalk --signature suspicious_file
```

---

### exiftool
**カテゴリ**: メタデータ解析

画像、動画、PDFなど様々なファイルのメタデータを読み書きするツール。

**CTFでの用途**:
- 画像ファイルに隠されたフラグの発見
- GPSデータやコメントフィールドの調査
- ファイルの作成日時や作成者情報の確認

**依存関係** (brew):
- `perl` (システム付属) - Perlランタイム

```bash
# 使用例: 全メタデータの表示
exiftool image.jpg
exiftool -a -u -g1 suspicious_file.pdf
```

---

### testdisk
**カテゴリ**: データ復旧

削除されたパーティションやファイルを復旧するためのツール。

**CTFでの用途**:
- ディスクイメージからの削除ファイル復旧
- パーティションテーブルの修復
- ファイルシステムの解析

**依存関係** (brew):
- `jpeg-turbo` - JPEG画像の処理
- `libtiff` - TIFF画像の処理
- `libpng` - PNG画像の処理
- `e2fsprogs` - ext2/3/4ファイルシステムのサポート

```bash
# 使用例: ディスクイメージの解析
testdisk disk_image.img
photorec disk_image.img  # 付属のファイル復旧ツール
```

---

### e2fsprogs / e2tools
**カテゴリ**: ext2/3/4ファイルシステム操作

Linuxのext2/3/4ファイルシステムを操作するツール群。

**CTFでの用途**:
- Linuxディスクイメージの解析
- 削除されたファイルの復旧
- ファイルシステムのデバッグ

```bash
# 使用例
e2ls disk.img:/path/to/dir
e2cp disk.img:/path/to/file ./extracted_file
debugfs disk.img
```

---

## ⚙️ リバースエンジニアリング

### ghidra
**カテゴリ**: リバースエンジニアリング

NSAが開発したオープンソースのリバースエンジニアリングツール。

**CTFでの用途**:
- バイナリの逆アセンブル・逆コンパイル
- 実行ファイルの解析
- 関数の動作解析とフラグの発見
- マルウェア解析

**依存関係** (brew):
- `openjdk@21` - Javaランタイム

```bash
# GUIで起動
ghidraRun
```

---

## 🖼️ 画像解析・ステガノグラフィ

### zsteg (Ruby Gem)
**カテゴリ**: PNG/BMPステガノグラフィ解析

PNG/BMP画像に隠されたデータを検出・抽出するツール。

**CTFでの用途**:
- LSB（最下位ビット）ステガノグラフィの検出
- 隠しテキストやファイルの抽出
- 様々なステガノグラフィ手法の自動検出

**依存関係** (gem):
- `zpng` - PNG解析ライブラリ
- `iostruct` - バイナリ構造体解析
- `rainbow` - カラー出力

```bash
# 使用例
zsteg image.png           # 全チャンネルをスキャン
zsteg -a image.png        # すべての手法で解析
zsteg -E "b1,rgb,lsb,xy" image.png  # 特定の設定で抽出
```

---

### gimp
**カテゴリ**: 画像編集

オープンソースの画像編集ソフトウェア。

**CTFでの用途**:
- ステガノグラフィの解析
- 画像の色調整やレイヤー分析
- 隠されたメッセージの可視化
- LSB（最下位ビット）解析の補助

**依存関係** (brew):
- `cairo` - 2Dグラフィックス
- `glib` - ユーティリティライブラリ
- `libpng`, `jpeg-turbo`, `libtiff`, `webp` - 各種画像フォーマット対応
- `little-cms2` - カラーマネジメント

---

## 📦 アーカイブ・ファイル操作

### p7zip
**カテゴリ**: アーカイブ

7-Zipのコマンドライン版。様々なアーカイブ形式に対応。

**CTFでの用途**:
- パスワード付きアーカイブの解凍
- 様々な形式の圧縮ファイルの展開

```bash
# 使用例
7z x archive.zip
7z l archive.7z  # 内容一覧
```

---

### squashfs
**カテゴリ**: ファイルシステム

SquashFSファイルシステムを操作するツール。

**CTFでの用途**:
- Linuxファームウェアイメージの展開
- 組み込みシステムのファイルシステム解析

**依存関係** (brew):
- `lz4`, `lzo`, `xz`, `zstd` - 各種圧縮アルゴリズム対応

```bash
# 使用例
unsquashfs filesystem.squashfs
```

---

### xz / zstd / lz4
**カテゴリ**: 圧縮ツール

各種圧縮アルゴリズムのコマンドラインツール。

**CTFでの用途**:
- 圧縮されたファイルの展開
- binwalkなどで抽出されたデータの解凍

```bash
# 使用例
xz -d file.xz
zstd -d file.zst
lz4 -d file.lz4 output
```

---

## 🔑 暗号・ハッシュ関連

### openssl@3
**カテゴリ**: 暗号化

暗号化、復号化、証明書管理などを行うツール。

**CTFでの用途**:
- 暗号化されたファイルの復号
- ハッシュ値の計算
- SSL/TLS関連の解析
- RSA/AESなどの暗号操作

**依存関係** (brew):
- `ca-certificates` - ルート証明書

```bash
# 使用例
openssl enc -d -aes-256-cbc -in encrypted.bin -out decrypted.txt
openssl dgst -sha256 file.txt
openssl rsa -in private.pem -text  # RSA鍵の解析
```

---

## 📁 ファイル・ディレクトリ操作

### tree
**カテゴリ**: ファイル表示

ディレクトリ構造をツリー形式で表示。

**CTFでの用途**:
- 抽出したファイルシステムの構造確認
- 隠しファイルやディレクトリの発見

```bash
tree -a extracted_files/
```

---

## 📌 クイックリファレンス

| ツール | 主な用途 | よく使うコマンド |
|--------|----------|------------------|
| aircrack-ng | Wi-Fi解析 | `aircrack-ng -w wordlist.txt capture.cap` |
| wireshark | パケット解析 | GUI または `tshark -r file.pcap` |
| binwalk | バイナリ解析 | `binwalk -e file` |
| exiftool | メタデータ | `exiftool file` |
| zsteg | PNGステガノ | `zsteg -a image.png` |
| ghidra | リバエン | `ghidraRun` |
| testdisk | データ復旧 | `testdisk image.img` |
| e2tools | ext2/3/4解析 | `e2ls`, `e2cp`, `debugfs` |
| p7zip | アーカイブ | `7z x archive.zip` |
| openssl | 暗号操作 | `openssl enc -d ...` |

---

## 📥 追加でインストールを推奨するツール

以下のツールはCTFで頻繁に使用されますが、現在インストールされていません：

| ツール | 用途 | インストール方法 |
|--------|------|------------------|
| `foremost` | ファイルカービング | `brew install foremost` |
| `steghide` | ステガノグラフィ | `brew install steghide` |
| `john` | パスワードクラック | `brew install john` |
| `hashcat` | GPUハッシュクラック | `brew install hashcat` |
| `volatility` | メモリフォレンジック | Python pip経由 |
| `radare2` | リバースエンジニアリング | `brew install radare2` |
| `pwntools` | Pwn/Exploit開発 | `pip install pwntools` |
| `stegsolve` | 画像ステガノ解析 | Java JAR |

---

*最終更新: 2026-02-02*
