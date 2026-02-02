import socket
import struct

HOST = "10.2.4.9"
PORT = 9999


def recv_msg(sock):
    # Read 4 bytes for length
    raw_len = sock.recv(4)
    if not raw_len:
        return None
    msg_len = struct.unpack("<I", raw_len)[0]

    # Read the message content
    data = b""
    while len(data) < msg_len:
        packet = sock.recv(msg_len - len(data))
        if not packet:
            break
        data += packet
    return data


def send_msg(sock, msg_str):
    msg_bytes = msg_str.encode("utf-8")
    length = len(msg_bytes)
    # Pack length as 4-byte little-endian
    header = struct.pack("<I", length)
    sock.sendall(header + msg_bytes)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Read initial banner
        # The banner shown in nc output might be sent as raw text or framed.
        # Based on "Note: This service uses a binary protocol.", the commands/responses are likely framed.
        # But the initial banner appeared immediately in nc.
        # Let's see if we can read it. It might just be raw text dumped on connection before the protocol loop starts.
        # Or maybe it IS framed but nc just printed it?
        # Wait, if nc printed it perfectly, and the protocol requires 4-byte length valid binary,
        # then either the banner is NOT framed, or the framing bytes happened to look like valid text or were invisible?
        # A 4-byte length like 100 (0x64 00 00 00) would print 'd' then nulls.
        # The banner seems to be plain text. Let's receive until we see "Available commands" or similar, or just a large chunk.

        print("Connected. Receiving banner...")
        # Just creating a socket usually doesn't show text unless we recv.
        # We'll try to recv a chunk.
        initial_data = s.recv(4096)
        print("Initial data received:")
        print(initial_data.decode("utf-8", errors="replace"))

        # Step 1: Send HELLO to get token
        print("\nSending HELLO...")
        send_msg(s, "HELLO")

        # Step 2: Receive response (Token)
        # Assuming the response is framed according to the note.
        response = recv_msg(s)
        if response:
            resp_str = response.decode("utf-8")
            print(f"Response: {resp_str}")

            # Extract token if strictly formatted, e.g. "Session token: XXXXX"
            # It might just be the token string itself. Let's inspect the output first.
            if "Your token: " in resp_str:
                # Find the line containing the token
                lines = resp_str.split("\n")
                token = None
                for line in lines:
                    if "Your token: " in line:
                        token = line.split("Your token: ")[1].strip()
                        break

                if token:
                    print(f"Token extracted: {token}")

                    # Step 3: Send QUERY <token>
                    print(f"Sending QUERY {token}...")
                    send_msg(s, f"QUERY {token}")

                    # Step 4: Receive Flag
                    # The response might be the flag directly or text containing such.
                    final_resp = recv_msg(s)
                    if final_resp:
                        print(f"Final Response: {final_resp.decode('utf-8')}")
                else:
                    print("Could not parse token from response")
        else:
            print("No response to HELLO")


if __name__ == "__main__":
    main()
