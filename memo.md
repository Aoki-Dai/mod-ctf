# 防衛省CTF終了後学習メモ

## 音声ファイル

data:audio/wav;base64,UklGRnQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YVAAAACAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgA==

## 細胞の回帰

[http://10.2.4.11:5000/](http://10.2.4.11:5000/)

## SquashFS

SquashFSは、Linux向けの軽量で高圧縮な読み込み専用（Read-only）ファイルシステムです。ファイル、inode、ディレクトリを効率的に圧縮し、OSのライブイメージ（LiveCD/USB）、組み込みLinuxのルートファイルシステム、アーカイブなどで広く利用されています。

## Ghidra

Ghidraは、アメリカ国家安全保障局によって開発されたオープンソースのリバースエンジニアリングツール

## 多表式換字暗号

多表式換字暗号（Polyalphabetic Substitution Cipher）は、複数の換字表（アルファベット配列）を周期的に切り替えて文字を置換する古典暗号です。単一の換字表を使う単一換字式暗号の弱点である頻度分析を無効化し、ヴィジュネル暗号がその代表例として知られています。

## tshark

TSharkは、人気のGUIパケットキャプチャツール「Wireshark」のコマンドライン版（CUIツール）であり、ネットワークトラフィックのキャプチャ、解析、デコードをコマンド上で高速に行えるツールです。GUI環境がないサーバーでの使用、スクリプトによる自動化、特定のフィールド抽出などに最適で、Wiresharkがインストールされている環境であればWindows、Linux、Macで利用可能です。

## objdump

objdump は、バイナリファイル（実行ファイルやオブジェクトファイル）の内部情報を表示するためのコマンドラインツールです。GNU Binutils の一部として提供されており、プログラムの動作解析やデバッグ、CTF（セキュリティ競技）などで広く利用されます。
→逆アセンブリに使用

```bash
# 逆アセンブル結果を表示
objdump -d a.out
```

## tcpdump

tcpdumpは、ネットワーク上を流れるパケットをキャプチャし、解析するための強力なオープンソース・コマンドラインツールです。Linux、macOS、Unix系OSで動作し、通信トラブルシューティングやデバッグ、セキュリティ監視に不可欠です。リアルタイム監視に加え、フィルタリング、PCAPファイルへの保存、Wiresharkでの詳細分析が可能です。

## CTFにおいてJohn

### セキュリティ研究者：John Hammond氏

John Hammond氏は、世界的に有名なサイバーセキュリティ研究者であり、教育者です。
活動: YouTubeチャンネルでCTFの解法動画（Walkthrough）を多数公開しており、初心者のバイブル的存在です。
実績: 自身もpicoCTFなどの問題作成に携わっているほか、米国防総省（DoD）のサイバートレーニングアカデミーでの教官経験もあります。
最新の取り組み: 2025年からは独自のトレーニングプラットフォーム「Just Hacking Training」を立ち上げ、手頃な価格で学べるCTF演習などを提供しています。
[John Hammond氏のウェブサイト](https://www.johnhammond.llc/)

### パスワード解析ツール：John the Ripper

CTFの競技中に使用される、有名なパスワードクラッキング（解析）ツールです。
用途: 暗号化されたパスワード（ハッシュ値）を高速で解析し、元の文字列を特定するために使われます。
コマンド: CTFの問題では、よく「zip2john」でZIPファイルのハッシュを抽出し、「john」コマンドで辞書攻撃を仕掛けるといった手順が使われます。
出題例: 国内のksnctfなど、問題タイトル自体が「John」となっているものは、このツールの使用を想定した問題であることが多いです。

## Aircrack-ng

Aircrack-ngは、802.11無線LANのセキュリティを評価するためのツールセットであり、パケットスニッフィング、WEP/WPA/WPA2-PSKの暗号解読（クラック）、分析、テスト機能を提供します。

Kali LinuxやParrot OSなどのセキュリティ特化型ディストリビューションにプリインストールされています。

## grep

grepは、ファイルやコマンドの出力から指定した文字列（正規表現パターン）に一致する行を検索・抽出して表示する、UNIX/Linuxで広く使われる強力なコマンド

## nm

nmコマンドは、LinuxなどのUNIX系OSにおいて、オブジェクトファイル、静的ライブラリ、実行可能ファイル（ELF形式など）のシンボルテーブル（関数名や変数名）を表示するデバッグツール

使用例：オブジェクトファイルのシンボルを確認する

```bash
nm test.o
```
