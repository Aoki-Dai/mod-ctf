ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
clean_text = ciphertext.replace(" ", "")

print(f"Len: {len(clean_text)}")

# 1. Simple Columnar Transposition (Write Row, Read Col)
print("\n--- Columnar Transposition (Width 2-20) ---")
for width in range(2, 21):
    # Columns
    cols = ["" for _ in range(width)]
    for i, c in enumerate(clean_text):
        cols[i % width] += c
    res = "".join(cols)
    if "THE" in res or "KEY" in res or "FLAG" in res:
        print(f"Width {width}: {res[:60]}...")

# 2. Scytale / Block Transposition (Write Col, Read Row) -> Equivalent to re-reading the above?
# Actually Scytale is: Write around stick (rows), read along stick (cols).
# So it's the same as above.

# 3. Rail Fence (Check KEY again)
print("\n--- Rail Fence ---")


def rail_fence(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1

    return "".join("".join(row) for row in fence)


for r in range(2, 10):
    res = rail_fence(clean_text, r)
    print(f"Rails {r}: {res[:100]}...")
