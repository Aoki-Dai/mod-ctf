import collections
import string

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ct = ciphertext.replace(" ", "")

c = collections.Counter(ct)
total = len(ct)

print("--- Frequency ---")
for char in string.ascii_uppercase:
    print(f"{char}: {c[char]} ({c[char] / total * 100:.2f}%)")

# Common in English: E (12%), T (9%), A (8%), O (8%), I (7%), N (7%).
# Here:
