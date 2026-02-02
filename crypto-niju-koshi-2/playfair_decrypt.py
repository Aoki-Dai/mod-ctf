def create_playfair_matrix(key):
    """Playfair暗号用の5x5マトリックスを作成"""
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()

    # キーの文字を追加
    for char in key:
        if char not in used and char.isalpha():
            matrix.append(char)
            used.add(char)

    # 残りのアルファベットを追加（J を除く、I と同じ扱い）
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # Jを除く
        if char not in used:
            matrix.append(char)
            used.add(char)

    return matrix


def get_position(matrix, char):
    """マトリックス内の文字の位置を取得"""
    char = char.upper()
    if char == "J":
        char = "I"
    idx = matrix.index(char)
    return idx // 5, idx % 5


def decrypt_playfair(ciphertext, key):
    """Playfair暗号を復号"""
    matrix = create_playfair_matrix(key)
    ciphertext = ciphertext.upper().replace("J", "I")
    ciphertext = "".join(c for c in ciphertext if c.isalpha())

    # 2文字ずつのペアに分割
    pairs = [ciphertext[i : i + 2] for i in range(0, len(ciphertext), 2)]

    plaintext = []
    for pair in pairs:
        if len(pair) < 2:
            break
        r1, c1 = get_position(matrix, pair[0])
        r2, c2 = get_position(matrix, pair[1])

        if r1 == r2:  # 同じ行
            plaintext.append(matrix[r1 * 5 + (c1 - 1) % 5])
            plaintext.append(matrix[r2 * 5 + (c2 - 1) % 5])
        elif c1 == c2:  # 同じ列
            plaintext.append(matrix[((r1 - 1) % 5) * 5 + c1])
            plaintext.append(matrix[((r2 - 1) % 5) * 5 + c2])
        else:  # 矩形
            plaintext.append(matrix[r1 * 5 + c2])
            plaintext.append(matrix[r2 * 5 + c1])

    return "".join(plaintext)


# 内側の暗号文
inner_ciphertext = "UGSUTCNAGCMVBOUFDMMBEFKZCFQPNBIOKABEVFKMPDFGSMIKTSMLGMXFDLNMSB"

# Playfair暗号で復号
key = "MONARCHY"
plaintext = decrypt_playfair(inner_ciphertext, key)
print(f"鍵: {key}")
print(f"暗号文: {inner_ciphertext}")
print(f"平文: {plaintext}")
print()

# マトリックスを表示
matrix = create_playfair_matrix(key)
print("Playfairマトリックス:")
for i in range(5):
    print(" ".join(matrix[i * 5 : (i + 1) * 5]))
