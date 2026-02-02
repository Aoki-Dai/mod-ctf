# 解決手順

## 1. 調査と準備

まず、CoAPプロトコルを扱うためのツールが必要です。環境には `coap-client` (libcoap) が入っていなかったため、Pythonの `aiocoap` ライブラリをインストールしました。

```bash
pip3 install aiocoap
```

## 2. リソース探索 (Discovery)

CoAPの標準的なリソース探索先である `/.well-known/core` にアクセスし、利用可能なエンドポイントを確認しました。

```bash
aiocoap-client coap://10.2.4.8:5683/.well-known/core
```

結果：

- `/bulb`: "Smart Bulb"
- `/bulb/brightness`: "Brightness Control"
- `/sos`: "SOS Signal"
- `/start`: "Start"
- `/status`: "Status"
- `/history`: "Blink History"

## 3. 動作のトリガー

`/history` を確認しても最初は空でした。システムを動作させる必要があると考え、`/start` エンドポイントにアプローチしました。GETリクエストは拒否されたため、POSTリクエストを送信しました。

```bash
aiocoap-client -m POST coap://10.2.4.8:5683/start
```

これにより「Blinking started」という応答が得られ、電球の点滅が始まりました。

## 4. データ収集

点滅が終了するのを待ち（`/status` で確認可能）、`/history` から点滅の履歴データを取得しました。

```bash
aiocoap-client coap://10.2.4.8:5683/history > history.txt
```

取得されたデータは `ON,timestamp` と `OFF,timestamp` のリストでした。

## 5. 解読

点灯時間（ONからOFFまでの時間）を分析すると、約0.3秒と約0.9秒の2種類があることがわかりました。これはモールス信号（短点と長点）の特徴です。

- 短点 (Dot): ~0.3秒
- 長点 (Dash): ~0.9秒

Pythonスクリプトを作成し、このタイミングデータをモールス信号に変換し、テキストに復号しました。

復号結果: `FLAG(M0RS3_SM4RT_BU1B)`

指示に従い、形式を `flag{...}` に変更して提出します。

## 答え

`flag{M0RS3_SM4RT_BU1B}`
