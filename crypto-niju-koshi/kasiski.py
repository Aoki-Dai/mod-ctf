ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ct = ciphertext.replace(" ", "")


def kasiski(text, min_len=3):
    sequences = {}
    for i in range(len(text) - min_len + 1):
        seq = text[i : i + min_len]
        if seq in sequences:
            sequences[seq].append(i)
        else:
            sequences[seq] = [i]

    for seq, positions in sequences.items():
        if len(positions) > 1:
            diffs = []
            for k in range(len(positions) - 1):
                diffs.append(positions[k + 1] - positions[k])
            print(f"Seq: {seq}, Pos: {positions}, Diffs: {diffs}")


kasiski(ct)
