import string

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
clean_text = ciphertext.replace(" ", "")

# Standard Polybius Square (I=J)
polybius = [
    ["A", "B", "C", "D", "E"],
    [
        "F",
        "G",
        "H",
        "I",
        "K",
    ],  # Note J is usually omitted or merged with I. Let's assume I/J merge, so K follows I.
    ["L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"],
]

# Map Char to (Row, Col)
char_map = {}
rev_map = {}
for r in range(5):
    for c in range(5):
        char = polybius[r][c]
        char_map[char] = (r, c)
        rev_map[(r, c)] = char


# Handle J -> I
def get_coords(char):
    if char == "J":
        char = "I"
    return char_map.get(char, (0, 0))  # Default to A if error


def bifid_decrypt(text, period):
    pt = ""
    # Process in blocks of size 'period'
    for i in range(0, len(text), period):
        block = text[i : i + period]
        bg_len = len(block)

        # Convert block to list of coordinates
        # Flattened list of coordinates from Ciphertext
        # In Bifid Encrypt:
        # P -> Coords (Row1, Col1), (Row2, Col2)...
        # Sep Row and Col lists.
        # Concat Row || Col -> Stream.
        # Stream read in pairs -> Ciphertext.

        # In Decrypt:
        # Ciphertext -> Coords -> Stream.
        # Split Stream into two halves (Row-part, Col-part).
        # Combine Row[i], Col[i] -> P[i].

        stream = []
        for c in block:
            r, c_idx = get_coords(c)
            stream.append(r)
            stream.append(c_idx)

        # Stream length = 2 * bg_len
        # Split into Row coords and Col coords
        row_coords = stream[:bg_len]
        col_coords = stream[bg_len:]

        for j in range(bg_len):
            r = row_coords[j]
            c_idx = col_coords[j]
            pt += rev_map[(r, c_idx)]

    return pt


print("--- Bifid Decrypt (Standard Square) ---")
for p in range(1, 40):
    try:
        dec = bifid_decrypt(clean_text, p)
        # Check for Englishness
        if "THE" in dec or "KEY" in dec or "FLAG" in dec:
            print(f"Period {p}: {dec[:60]}...")
    except Exception as e:
        pass
