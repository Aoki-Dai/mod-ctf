import binascii

hex_strings = [
    "7b22757365726e616d65223a2261646d696e222c2270617373776f7264223a225255675357536e454e6b47774635587870594a444e33546b504156457345694f6d5338797336746a227d",
    "7b22636f6d6d616e64223a22737461747573227d",
    "7b22636f6d6d616e64223a2274656d70227d",
    "7b22636f6d6d616e64223a227175657279227d",
]

print("Decoded POST bodies:")
for h in hex_strings:
    try:
        print(binascii.unhexlify(h).decode("utf-8"))
    except Exception as e:
        print(f"Error decoding {h}: {e}")
