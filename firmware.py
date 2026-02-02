import zlib


def find_flag():
    try:
        with open("firmware.bin", "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print("エラー: firmware.bin が見つかりません。")
        return

    # zlib (Best Compression) のヘッダーシグネチャ
    header = b"\x78\xda"
    offset = 0

    print("探索を開始します...")

    while True:
        # 次のヘッダーを検索
        idx = data.find(header, offset)
        if idx == -1:
            break

        try:
            # データの解凍を試みる
            # zlib.decompressは有効なストリームの終わりまでを自動で処理します
            decompressed = zlib.decompress(data[idx:])

            # フラグのパターンを検索
            if b"flag{" in decompressed:
                print(f"\n[!] フラグを発見しました (Offset: {idx}):")
                print("-" * 30)
                # UTF-8でデコードして表示
                print(decompressed.decode("utf-8", errors="ignore"))
                print("-" * 30)
                return

        except Exception:
            # 解凍エラーは無視して次へ
            pass

        offset = idx + 1

    print("探索終了。")


if __name__ == "__main__":
    find_flag()
