ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ct = ciphertext.replace(" ", "")


def print_grid_rows(width, text):
    print(f"\n--- Width {width} (Rows) ---")
    rows = len(text) // width
    if len(text) % width != 0:
        rows += 1

    for r in range(rows):
        line = ""
        for c in range(width):
            idx = r * width + c
            if idx < len(text):
                line += text[idx]
            else:
                line += " "
        print(line)


def print_grid_cols(height, text):  # Writing in columns (Decrypting pure columnar)
    # If we assume 'text' is columns concatenated.
    # Height H. Width = ceil(L/H).
    # But usually we define Width.
    pass


# Try 5 and 9
print_grid_rows(5, ct)
print_grid_rows(9, ct)
print_grid_rows(15, ct)
print_grid_rows(27, ct)


# Decrypt Columnar (taking text as columns)
# Width 9. 137 chars.
# Cols 0,1 length 16. Cols 2-8 length 15.
# Total 2*16 + 7*15 = 32 + 105 = 137.
def decrypt_columnar_standard(width, text):
    # Lengths
    col_lens = []
    full_cols = len(text) % width
    base_len = len(text) // width

    for i in range(width):
        if i < full_cols:
            col_lens.append(base_len + 1)
        else:
            col_lens.append(base_len)

    # Slicing
    cols = []
    curr = 0
    for l in col_lens:
        cols.append(text[curr : curr + l])
        curr += l

    # Read rows
    res = ""
    for r in range(base_len + 1):
        for c in range(width):
            if r < len(cols[c]):
                res += cols[c][r]
    return res


print(
    f"\n--- Decrypt Standard Columnar (Width 9) ---\n{decrypt_columnar_standard(9, ct)}"
)
print(
    f"\n--- Decrypt Standard Columnar (Width 5) ---\n{decrypt_columnar_standard(5, ct)}"
)
