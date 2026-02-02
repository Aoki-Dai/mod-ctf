import itertools

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ct = ciphertext.replace(" ", "")


def rail_fence_decrypt(text, num_rails):
    rail_len = len(text)
    cycle = 2 * (num_rails - 1)

    indexes = sorted(
        list(range(rail_len)),
        key=lambda i: (i % cycle if i % cycle < num_rails else cycle - (i % cycle), i),
    )

    result = [""] * rail_len
    for i, char in zip(indexes, text):
        result[i] = char
    return "".join(result)


def columnar_transposition_decrypt(text, width):
    # Standard: Write in columns, Read in rows?
    # Or Encrypt: Write Rows, Read Cols.
    # Decrypt: Write Cols, Read Rows.

    # Assume ciphertext is columns concatenated.
    # Col lengths:
    n = len(text)
    col_len = n // width
    rem = n % width

    # Calculate column lengths
    lengths = [col_len + 1 if i < rem else col_len for i in range(width)]

    # Split text into columns
    cols = []
    curr = 0
    for l in lengths:
        cols.append(text[curr : curr + l])
        curr += l

    # Read row by row
    res = ""
    for r in range(col_len + 1):
        for i in range(width):
            if r < lengths[i]:
                res += cols[i][r]
    return res


print("--- Searching for 'KEY' or 'FLAG' in Transposition Decryptions ---")

# Rail Fence
for r in range(2, 20):
    dec = rail_fence_decrypt(ct, r)
    if "KEY" in dec or "FLAG" in dec:
        print(f"[Rail Fence {r}] Found keyword: {dec}")
    # Also check small segments
    # print(f"[Rail Fence {r}] {dec[:20]}...")

# Columnar
for w in range(2, 20):
    dec = columnar_transposition_decrypt(ct, w)
    if "KEY" in dec or "FLAG" in dec:
        print(f"[Columnar Width {w}] Found keyword: {dec}")
    # print(f"[Columnar {w}] {dec[:20]}...")

# Scytale (Simple Skip)
# Reading every Nth char
for n in range(2, 20):
    dec = ""
    for i in range(n):
        dec += ct[i::n]
    if "KEY" in dec or "FLAG" in dec:
        print(f"[Skip {n}] Found keyword: {dec}")

print("Done.")
