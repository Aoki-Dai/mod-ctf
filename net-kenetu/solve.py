
def solve():
    with open('icmp_data.txt', 'r') as f:
        lines = f.readlines()

    flag_chars = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        
        seq = parts[0]
        data = parts[1]
        
        # The modified byte is at offset 16 (0-indexed)
        # In hex string, that is index 32
        if len(data) > 34:
             byte_hex = data[32:34]
             try:
                 char = chr(int(byte_hex, 16))
                 flag_chars.append(char)
             except ValueError:
                 pass
    
    print("".join(flag_chars))

if __name__ == '__main__':
    solve()
