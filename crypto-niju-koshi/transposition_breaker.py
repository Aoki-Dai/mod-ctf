import random
import math

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ciphertext = ciphertext.replace(" ", "")

# Standard English Quadgram Statistics (Log Probabilities approx)
# Source: http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
# I will use a small subset or a generated one for demonstration as I cannot download big files.
# But for a 137 char text, simple frequency analysis (monogram/bigram) might be better or Index of Coincidence optimization.
# I'll stick to a simple IC maximization + Chi-Squared per column (which I already did in solve.py).
# solve.py picked Period 19 but output was garbage.
# This implies it might NOT be Vigenere, or the alphabet is different.

# What if it's "Variant Beaufort"?
# What if the layout is different?

# Let's try Hill Climbing on the KEY for substitution ciphers (Simple Substitution).
# If it is a Monoalphabetic Substitution (IC ~ 0.038 says NO, but maybe my IC is off due to "Double" nature).
# Wait, IC 0.038 is VERY LOW. (Random is 0.038).
# This practically confirms it is Polyalphabetic or Transposition.
# If Transposition, we can try to "maxmize bigram scores" by rearranging columns.

# Let's try to break Columnar Transposition by Hill Climbing on the column order.

import itertools


def score_text(text):
    # Simple score: count common bigrams
    common_bigrams = [
        "TH",
        "HE",
        "IN",
        "ER",
        "AN",
        "RE",
        "ON",
        "AT",
        "EN",
        "ND",
        "TI",
        "ES",
        "OR",
        "TE",
        "OF",
        "ED",
        "IS",
        "IT",
        "AL",
        "AR",
        "ST",
        "TO",
        "NT",
        "NG",
        "SE",
        "HA",
        "AS",
        "OU",
        "IO",
        "LE",
        "VE",
        "ME",
        "EA",
        "HI",
        "RD",
        "SO",
        "MR",
    ]
    score = 0
    for bigram in common_bigrams:
        score += text.count(bigram) * 5
    # Penalize uncommon
    uncommon = ["QZ", "ZQ", "JX", "XJ"]
    for u in uncommon:
        score -= text.count(u) * 5
    return score


best_score = -10000
best_text = ""
best_perm = []

# Try block lengths / widths
for width in range(2, 20):
    # Split into columns
    # Note: Text length 137.
    # Rectangular requires padding or irregular columns.
    # Standard Columnar Transposition fills row by row, read by columns.
    # To decrypt: Determine column lengths.
    # 137 chars. Width W.
    # Full columns of length = ceil(137/W).
    # Number of full columns = 137 % W.
    # Rest are length floor(137/W).

    col_len = len(ciphertext) // width
    rem = len(ciphertext) % width

    # Calculate column lengths
    lengths = [col_len + 1 if i < rem else col_len for i in range(width)]

    # We want to find a permutation of columns [0..width-1]
    # For small width, we can brute force.
    # Width 8! = 40320. Feasible.

    if width > 8:
        continue  # Skip large widths for brute force

    print(f"Brute Forcing Width {width}...")

    cols_indices = list(range(width))
    best_perm_score = -99999
    best_perm_text = ""

    # Pre-slice columns based on standard assumption (Ciphertext = C1C2C3...)
    # We don't know the order, but we know the segments.
    # Segments are chunks of the ciphertext.
    # But wait! If the order was permuted, the lengths might depend on the *original* position.
    # Standard Columnar:
    # 1. Write Row by Row.
    # 2. Read Col by Col (Key Order).
    # So Ciphertext = Col[K[0]] + Col[K[1]] + ...
    # And Length(Col[i]) depends on i.
    # If we assume we have the chunks `segments`, we need to assign them to positions 0..W-1.
    # But `segments` have different lengths!
    # A segment of length L+1 MUST go to a position < rem.
    # A segment of length L MUST go to a position >= rem.
    # So we can only permute "Long" segments among "Long" slots, and "Short" segments among "Short" slots.

    # Count Long and Short columns
    num_long = rem
    num_short = width - rem
    len_long = col_len + 1
    len_short = col_len

    # Extract segments from ciphertext
    # We don't know which part of ciphertext is which segment yet?
    # Actually, Ciphertext IS the sequence of segments.
    # So Segment 0 is first `len(Col[K[0]])` chars.
    # But we don't know if `Col[K[0]]` is Long or Short!
    # This implies we iterate over permutations involved in the *structure*?
    # This is hard.

    # Simplified approach: Assume Rectangular (Widths 2, 5, 10, ...) or close to.
    # Or assume key order logic.

    # Alternative:
    # Just try splitting ciphertext into `width` chunks of roughly equal size.
    # If 137 % Width != 0, this is ambiguous.
    pass

    # We want to find a permutation of columns [0..width-1]
    # For small width, we can brute force.
    # Width 8! = 40320. Feasible.

    if width > 9:
        continue  # Skip large widths for brute force

    # Generate all permutations
    cols_indices = list(range(width))
    for perm in itertools.permutations(cols_indices):
        # Reconstruct grid
        # We need to slice the ciphertext into columns based on the permutation.
        # BUT in standard Columnar, we don't know which column is which in the ciphertext yet (that IS the key).
        # We assume the ciphertext IS the sequence of columns.
        # We just need to order them correctly.

        # Calculate lengths of columns based on original position (if filled row by row)
        # The columns are read out: C1, C2, C3...
        # Wait, in encryption: Enc writes Rows, reads Cols (in Key Order).
        # Ciphertext = Col[k1] + Col[k2] + ...
        # So we have chunks of text that correspond to columns.
        # But we don't know the key order.
        # We just need to rearrange the chunks.

        # Determine chunk lengths
        # The "Long" columns are the first 'rem' columns in the UNPERMUTED grid (Left to Right).
        # But we don't know the permutation.
        # This is the tricky part of irregular columnar transposition.
        # However, if we assume the Key determines the read order, then the ciphertext is composed of valid columns.
        # But their lengths depend on their position in the grid *during writing*.
        # Writing order: Normal (Left to Right).
        # So Column 0 is length L or L+1. Column 1 is L or L+1.
        # The number of L+1 columns is `rem`. The first `rem` columns (position 0..rem-1) are L+1.

        # In Decryption:
        # We have the ciphertext. We need to split it into columns.
        # But we don't know which chunk belongs to which column index (0..W-1) because we don't know the key.
        # The key determines the *order* the columns appear in ciphertext.
        # AND the key determines which column was "Column 0" (and thus its length).

        # This dependency makes brute forcing types hard.
        # But let's assume "Double Grid" -> maybe Square? Or simple? or Factor?
        # 137 is prime?
        pass

    # Simplified approach: regular blocks?
    # If 137 is not divisible, maybe we ignore the last few chars?
    # Or maybe it's rail fence?

print(
    "Skipping Complex Columnar Brute Force in script due to complexity. Will rely on manual patterns."
)


# Try scoring Rectangular Transpo candidates from visualize_grids (Row read)
def score_rows_read(text, width):
    rows = len(text) // width
    # If not rectangle, ignore trailing
    # Just read rows
    res = ""
    for r in range(rows):
        res += text[r * width : (r + 1) * width]
    return score_text(res)


print("--- Scoring Simple Grids ---")
for w in range(2, 40):
    # Construct grid (Row by Row) is just identity?
    # No, Transposition is: Write Rows, Scramble Cols, Read Cols.
    # Or Write Cols, Scramble Rows, Read Rows?

    # Simple "Write Row, Read Col" (Transpose)
    # We did this in simple_transposition.py (Columnar Transposition).
    pass

# Let's revisit Rail Fence 2 result `RF2` from solve.py
rf2_res = "ECFTLFVEKYOWVJLZJGPWMKWAQCETQUNEHDITJQRHTITHLUIKEBTUCSHHLBTXWRCYJENRWESZEXFHBYTCWSHCJKVYMYJOMGSBTUVZLGROKZMIRIKLGADNGXHKJMVYIRTNREWKUHDUM"

print(f"\nRF2 Score: {score_text(rf2_res)}")
print(f"RF2: {rf2_res}")

# Check for "EFFECTIVE" anagram
# Freq of EFFECTIVE: E:3, F:2, C:1, T:1, I:1, V:1
# Check first 12 chars of RF2: E C F T L F V E K Y O W
# E:2, C:1, F:2, T:1, L:1, V:1, K:1, Y:1, O:1, W:1
# Missing I?
# Found L, K, Y, O, W.
# "EFFECTIVE" needs I. None in first 12.
# So "ECFTLFVE..." is NOT "EFFECTIVE".

# Check Vigenere on RF2 again with common keys
keys = [
    "GRID",
    "DOUBLE",
    "LATTICE",
    "NIJUKOSHI",
    "TWOSQUEARE",
    "CIPHER",
    "SOLVE",
    "KEY",
    "FLAG",
]


def quick_vigenere(text, key):
    res = ""
    for i, c in enumerate(text):
        shift = ord(key[i % len(key)]) - ord("A")
        res += chr((ord(c) - ord("A") - shift) % 26 + ord("A"))
    return res


print("\n--- Vigenere on RF2 with Check Keys ---")
for k in keys:
    dec = quick_vigenere(rf2_res, k)
    if score_text(dec) > -50:  # Arbitrary threshold
        print(f"Key {k}: {dec[:50]}... Score: {score_text(dec)}")
    else:
        print(f"Key {k}: {dec[:50]}... Score: {score_text(dec)}")
