# Writeup: 怪しい名前解決

## 問題の概要

社内ネットワークで検出された不審なDNS通信のパケットキャプチャ（`capture.pcap`）を解析し、隠されたフラグを見つける問題です。

## 解析手順

1. **パケットの分析**
   `tcpdump` や `tshark` を使用して、DNS通信（ポート53）の内容を確認しました。
   その結果、`internal-sys.local` ドメインに対する不審なクエリが多数見つかりました。

   例:

   ```
   exfil.pmrgq33toqrduise.internal-sys.local.
   exfil.ivjuwvcpkawucmkc.internal-sys.local.
   ```

   `exfil` というプレフィックスが付いており、データの持ち出し（Exfiltration）が疑われます。また、サブドメイン部分（`pmrgq33toqrduise` など）はランダムな英数字に見えますが、Base32エンコーディングの特徴（英字A-Zと数字2-7）と一致します。

2. **データの抽出と復号**
   Pythonスクリプトを作成し、以下の手順でデータを復元しました。
   1. パケットから `exfil.<エンコードされたデータ>.internal-sys.local` という形式のクエリを抽出。
   2. エンコードされたデータ部分を連結。
   3. 連結した文字列をBase32でデコード。

   使用したスクリプト（`solve_dns.py`）により、連結された文字列はJSONデータとして復元されました。

3. **復号結果**
   デコードされたデータは以下の通りです（整形済み）。

   ```json
   {
       "host": "DESKTOP-A1B2C3D",
       "user": "user",
       "documents": [
           "C:\\Users\\user\\Documents\\Passwords.xlsx",
           "C:\\Users\\user\\Documents\\社外秘_顧客リスト.xlsx",
           "C:\\Users\\user\\Documents\\VPN_credentials.txt",
           "C:\\Users\\user\\Documents\\flag{dn5_tunn3l_3xf1l}.txt",
           "C:\\Users\\user\\Documents\\人事評価_2024.docx"
       ],
       "chrome": {
           "login_data": "C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data",
           ...
       },
       ...
   }
   ```

   このデータの中に、フラグを含むファイルパスが含まれていました。

## フラグ

```
flag{dn5_tunn3l_3xf1l}
```
