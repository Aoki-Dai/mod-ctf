ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
clean_text = ciphertext.replace(" ", "")

mid = (len(clean_text) + 1) // 2
first = clean_text[:mid]
second = clean_text[mid:]

print(f"Total: {len(clean_text)}")
print(f"Mid: {mid}")
print(f"First Part (End): ...{first[-5:]}")
print(f"Second Part (Start): {second[:5]}...")

rf2_res = ""
for i in range(len(second)):
    rf2_res += first[i] + second[i]
if len(first) > len(second):
    rf2_res += first[-1]

print(f"RF2: {rf2_res[:20]}...")
