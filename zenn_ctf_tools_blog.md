---
title: "【CTF入門】macOSでセキュリティツールを揃えよう！Homebrewで始めるCTF環境構築"
emoji: "🔐"
type: "tech"
topics: ["CTF", "セキュリティ", "macOS", "Homebrew", "初心者"]
published: false
---

## はじめに

こんにちは！CTF初心者の私が、先日**防衛省サイバーコンテスト**に参加してきました。

結果は...正直なところ、かなり苦戦しました😅
全体的に難易度が高く、「あのツールがあれば...」「この知識があれば...」と何度も思いました。

そこで今回は、**実際にCTFで必要になったツール**をまとめてみました。
これからCTFを始める方の参考になれば嬉しいです！

:::message
この記事はmacOS + Homebrewを前提としています。
Linuxの方は適宜読み替えてください。
:::

## 🎯 この記事の対象読者

- CTFに興味があるけど、何から始めればいいかわからない方
- macOSでセキュリティツールを揃えたい方
- 防衛省CTFのようなコンテストに挑戦したい方

## 📦 まずはこれ！一括インストールスクリプト

とりあえず必要なツールを一気に入れたい方はこちら：

```bash
# Homebrew Formulae（コマンドラインツール）
brew install aircrack-ng binwalk exiftool ghidra testdisk \
             p7zip squashfs tree wireshark

# Homebrew Casks（GUIアプリ）
brew install --cask wireshark gimp

# Ruby Gem（ステガノグラフィ用）
gem install zsteg
```

それでは、各ツールを**CTFのジャンル別**に紹介していきます！

---

## 🔍 Forensics（フォレンジック）問題で使うツール

フォレンジックは、ファイルやディスクイメージから隠された情報を見つけ出す問題です。
防衛省CTFでも出題され、**binwalk**と**testdisk**が大活躍しました。

### binwalk - ファームウェア解析の必需品

バイナリファイルに埋め込まれたファイルを検出・抽出するツールです。

```bash
brew install binwalk
```

**使い方：**
```bash
# ファイルのシグネチャを確認
binwalk suspicious_file

# 埋め込みファイルを自動抽出
binwalk -e suspicious_file

# 抽出結果は _suspicious_file.extracted/ に保存される
```

:::details 防衛省CTFでの体験談
問題で渡されたファームウェアイメージに`binwalk -e`を実行したところ、SquashFSファイルシステムが抽出できました。そこからさらに掘り下げていくと...というパターンが多かったです。
:::

### exiftool - メタデータの宝庫

画像ファイルには撮影日時、GPS座標、作成者名など様々な情報が埋め込まれています。

```bash
brew install exiftool
```

**使い方：**
```bash
# 全メタデータを表示
exiftool image.jpg

# GPS座標だけ表示
exiftool -gps* image.jpg

# コメントフィールドを確認（フラグが隠れてることも！）
exiftool -comment image.jpg
```

:::message alert
CTFでは画像ファイルのメタデータに**フラグがそのまま書いてある**こともあります。
まずは`exiftool`で確認する癖をつけましょう！
:::

### testdisk / photorec - 削除ファイルの復旧

ディスクイメージから削除されたファイルを復旧するツールです。

```bash
brew install testdisk
```

**使い方：**
```bash
# ディスクイメージを解析
testdisk disk_image.img

# ファイル復旧（photorecが便利）
photorec disk_image.img
```

---

## 🖼️ Stego（ステガノグラフィ）問題で使うツール

画像や音声ファイルにデータを隠す技術がステガノグラフィです。
**見た目は普通の画像なのに、中にフラグが隠されている**という問題が出ます。

### zsteg - PNG/BMP解析の決定版

LSB（最下位ビット）ステガノグラフィを自動検出してくれる神ツールです。

```bash
gem install zsteg
```

**使い方：**
```bash
# 全チャンネルをスキャン
zsteg image.png

# すべての手法で徹底的に解析
zsteg -a image.png

# 特定のチャンネルを抽出
zsteg -E "b1,rgb,lsb,xy" image.png > extracted.txt
```

:::details zstegの出力例
```
b1,rgb,lsb,xy       .. text: "flag{h1dd3n_1n_p1x3ls}"
b1,bgr,lsb,xy       .. <binary data>
b2,rgb,lsb,xy       .. <binary data>
```
こんな感じでフラグが見つかることがあります！
:::

### GIMP - 画像の色調整で隠しメッセージを発見

無料の画像編集ソフトですが、CTFでも活躍します。

```bash
brew install --cask gimp
```

**CTFでの使い方：**
1. 画像を開く
2. `色` → `カーブ` でコントラストを極端に上げる
3. `フィルター` → `強調` → `エッジ検出` を試す
4. 各色チャンネル（R/G/B）を個別に確認

---

## 🌐 Network（ネットワーク）問題で使うツール

パケットキャプチャファイル（.pcap）を解析して、通信内容からフラグを見つける問題です。

### Wireshark - パケット解析の王様

ネットワークフォレンジックには欠かせないツールです。

```bash
brew install --cask wireshark
```

**よく使うフィルタ：**
```
# HTTPリクエストだけ表示
http

# 特定のIPアドレスの通信
ip.addr == 192.168.1.1

# POST通信（ログイン情報などが見つかるかも）
http.request.method == "POST"

# DNSクエリ（DNSトンネリング問題で使う）
dns

# FTPでファイル転送してないか
ftp-data
```

:::details 防衛省CTFでの体験談
`.cap`ファイルが渡されて「無線LANの通信を解析せよ」という問題がありました。
まず`aircrack-ng`でWi-Fiパスワードを解読し、Wiresharkで復号化した通信を見ると...アプリケーション層に答えがありました！
:::

### aircrack-ng - 無線LAN解析

Wi-Fiのキャプチャファイルからパスワードを解読するツールです。

```bash
brew install aircrack-ng
```

**使い方：**
```bash
# 辞書攻撃でパスワードを解読
aircrack-ng -w /path/to/rockyou.txt capture.cap

# 複数のBSSIDがある場合は指定
aircrack-ng -w wordlist.txt -b AA:BB:CC:DD:EE:FF capture.cap
```

:::message
`rockyou.txt`は有名なパスワードリストです。
CTFでは「簡単なパスワード」というヒントがあれば、これを使うとほぼ解けます。
:::

---

## ⚙️ Reversing（リバースエンジニアリング）問題で使うツール

実行ファイルを解析して、隠された処理やフラグを見つける問題です。
防衛省CTFでは**かなり難しく感じたジャンル**でした。

### Ghidra - NSA製の最強リバエンツール

無料なのに超高機能なリバースエンジニアリングツールです。

```bash
brew install ghidra
```

**基本的な使い方：**
1. `ghidraRun`で起動
2. 新規プロジェクト作成
3. バイナリファイルをインポート
4. 自動解析を実行
5. `main`関数や怪しい関数を探す

:::details 初心者向けTips
- `Decompile`ウィンドウでC言語風のコードが見れます
- `Strings`ウィンドウで文字列一覧を確認（フラグのヒントがあるかも）
- `Functions`ウィンドウで関数一覧を確認
:::

---

## 🔐 Crypto（暗号）問題で使うツール

暗号の問題はツールというより**知識と実装力**が問われます。
ただ、以下のツールは持っておくと便利です。

### OpenSSL - 暗号操作の基本

```bash
# macOSにはデフォルトで入っていますが、最新版を入れるなら
brew install openssl@3
```

**使い方：**
```bash
# Base64デコード
echo "ZmxhZ3t0ZXN0fQ==" | openssl base64 -d

# AES復号
openssl enc -d -aes-256-cbc -in encrypted.bin -out decrypted.txt -pass pass:password

# RSA鍵の情報を見る
openssl rsa -in private.pem -text -noout

# ハッシュ計算
openssl dgst -sha256 file.txt
```

---

## 📁 その他便利ツール

### tree - ディレクトリ構造を可視化

```bash
brew install tree

# 使い方
tree -a extracted_files/  # 隠しファイルも表示
```

### p7zip - あらゆるアーカイブを展開

```bash
brew install p7zip

# 使い方
7z x archive.zip
7z x archive.7z
7z l archive.zip  # 中身を確認（展開せずに）
```

---

## 📊 ツール早見表

| ジャンル | 最初に試すツール | コマンド例 |
|---------|-----------------|-----------|
| Forensics | binwalk | `binwalk -e file` |
| Forensics | exiftool | `exiftool image.jpg` |
| Stego | zsteg | `zsteg -a image.png` |
| Network | Wireshark | GUIで.pcapを開く |
| Network | aircrack-ng | `aircrack-ng -w dict.txt cap` |
| Reversing | Ghidra | `ghidraRun` |
| Crypto | OpenSSL | `openssl enc -d ...` |

---

## 🎓 CTF練習サイトの紹介

ツールを揃えたら、実際に問題を解いて練習しましょう！

| サイト | 難易度 | 特徴 |
|--------|--------|------|
| [picoCTF](https://picoctf.org/) | ⭐ 初心者向け | 丁寧なヒント付き |
| [CryptoHack](https://cryptohack.org/) | ⭐⭐ | 暗号特化 |
| [Hack The Box](https://www.hackthebox.com/) | ⭐⭐⭐ | 実践的 |
| [TryHackMe](https://tryhackme.com/) | ⭐⭐ | 学習コンテンツ充実 |

---

## 🏁 まとめ

今回は、macOSでCTFを始めるために必要なツールを紹介しました。

**最低限これだけは入れておこう：**
- `binwalk` - バイナリ解析
- `exiftool` - メタデータ確認
- `zsteg` - ステガノグラフィ
- `Wireshark` - パケット解析
- `Ghidra` - リバースエンジニアリング

防衛省CTFは確かに難しかったですが、**ツールの使い方を覚える良い機会**になりました。
皆さんも一緒にCTFを楽しみましょう！💪

---

## 📚 参考リンク

- [CTF入門 - CTF Wiki](https://ctf-wiki.org/)
- [Ghidra公式ドキュメント](https://ghidra-sre.org/)
- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html/)

---

:::message
この記事が役に立ったら、いいね👍をお願いします！
質問があればコメント欄でお気軽にどうぞ。
:::
