def solve():
    stage1_shifts = [
        3,
        7,
        2,
        5,
        9,
        4,
        1,
        8,
        6,
        3,
        7,
        2,
        5,
        9,
        4,
        1,
        8,
        6,
        3,
        7,
        2,
        5,
        9,
        4,
        1,
        8,
    ]
    stage2_shifts = [5, 2, 8, 3, 1, 6, 4, 9, 7, 2]
    data = "}x0bv7t_g6t56wj_3u8i{nkvj"

    def decrypt_char(c, shift):
        if "a" <= c <= "z":
            base = ord("a")
            return chr((ord(c) - base - shift) % 26 + base)
        elif "A" <= c <= "Z":
            base = ord("A")
            return chr((ord(c) - base - shift) % 26 + base)
        elif "0" <= c <= "9":
            base = ord("0")
            return chr((ord(c) - base - shift) % 10 + base)
        else:
            return c

    def decrypt_string(s, shifts):
        res = []
        for i, char in enumerate(s):
            # Hint says: i is character position (0-based index)
            # shift[i mod N]
            shift = shifts[i % len(shifts)]
            res.append(decrypt_char(char, shift))
        return "".join(res)

    # Strategy 1: Reverse -> Decrypt Stage 2 -> Decrypt Stage 1
    # Assuming Encryption was: Stage1 -> Stage2 -> Reverse
    rev_data = data[::-1]
    temp1 = decrypt_string(rev_data, stage2_shifts)
    plain1 = decrypt_string(temp1, stage1_shifts)
    print(f"Strategy 1 (Rev -> D2 -> D1): {plain1}")

    # Strategy 2: Reverse -> Decrypt Stage 1 -> Decrypt Stage 2
    # Assuming Encryption was: Stage2 -> Stage1 -> Reverse
    temp2 = decrypt_string(rev_data, stage1_shifts)
    plain2 = decrypt_string(temp2, stage2_shifts)
    print(f"Strategy 2 (Rev -> D1 -> D2): {plain2}")

    # Strategy 3: Decrypt Stage 2 -> Decrypt Stage 1 -> Reverse
    # Assuming Encryption was: Reverse -> Stage1 -> Stage2
    temp3 = decrypt_string(data, stage2_shifts)
    temp3b = decrypt_string(temp3, stage1_shifts)
    plain3 = temp3b[::-1]
    print(f"Strategy 3 (D2 -> D1 -> Rev): {plain3}")

    # Strategy 4: Decrypt Stage 1 -> Decrypt Stage 2 -> Reverse
    temp4 = decrypt_string(data, stage1_shifts)
    temp4b = decrypt_string(temp4, stage2_shifts)
    plain4 = temp4b[::-1]
    print(f"Strategy 4 (D1 -> D2 -> Rev): {plain4}")

    # Strategy 5: Decrypt Stage 2 -> Reverse -> Decrypt Stage 1
    # Encryption: Stage1 -> Reverse -> Stage2
    temp5 = decrypt_string(data, stage2_shifts)
    temp5_rev = temp5[::-1]
    plain5 = decrypt_string(temp5_rev, stage1_shifts)
    print(f"Strategy 5 (D2 -> Rev -> D1): {plain5}")

    # Strategy 6: Decrypt Stage 1 -> Reverse -> Decrypt Stage 2
    # Encryption: Stage2 -> Reverse -> Stage1
    temp6 = decrypt_string(data, stage1_shifts)
    temp6_rev = temp6[::-1]
    plain6 = decrypt_string(temp6_rev, stage2_shifts)
    print(f"Strategy 6 (D1 -> Rev -> D2): {plain6}")

    # Strategy 7: Check if shifts should be ADDED (maybe reverse shift in encryption?)
    # Hint says Encrypt = + shift. So Decrypt = - shift.

    # Let's inspect plain5 and plain6.


if __name__ == "__main__":
    solve()
