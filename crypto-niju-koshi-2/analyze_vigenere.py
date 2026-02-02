ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ciphertext = ciphertext.replace(" ", "")

def kasiski_examination(ciphertext):
    min_len = 3
    max_len = 6
    sequences = {}
    for i in range(len(ciphertext) - min_len):
        for seq_len in range(min_len, min(max_len + 1, len(ciphertext) - i)):
            seq = ciphertext[i:i + seq_len]
            if seq not in sequences:
                sequences[seq] = []
            sequences[seq].append(i)
    
    repeated = {k: v for k, v in sequences.items() if len(v) > 1}
    
    distances = []
    for seq, positions in repeated.items():
        for i in range(len(positions) - 1):
            distances.append(positions[i+1] - positions[i])
            
    print(f"Repeated sequences: {repeated}")
    print(f"Distances: {distances}")
    
    # GCC (Greatest Common Divisor) of distances? 
    # Or just factor the distances.
    from math import gcd
    if distances:
        # Simple frequency of factors
        factors = {}
        for d in distances:
            for i in range(2, d + 1):
                if d % i == 0:
                    factors[i] = factors.get(i, 0) + 1
        print("Factor counts:", sorted(factors.items(), key=lambda x: x[1], reverse=True))

kasiski_examination(ciphertext)

# Also let's try to calculate Index of Coincidence for various key lengths
def calculate_ic(text):
    n = len(text)
    if n <= 1: return 0
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    numerator = sum(v * (v - 1) for v in counts.values())
    return numerator / (n * (n - 1))

print("\nIndex of Coincidence for different key lengths:")
for k in range(1, 20):
    avg_ic = 0
    for i in range(k):
        subtext = ciphertext[i::k]
        avg_ic += calculate_ic(subtext)
    avg_ic /= k
    print(f"Key length {k}: {avg_ic:.4f}")
