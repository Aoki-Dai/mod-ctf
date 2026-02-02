import re

file_path = "output.txt"

try:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

# 括弧 ( ) に囲まれた部分をすべて抽出する
matches = re.findall(r"\((.*?)\)", content)

print(f"Found {len(matches)} parenthesized groups.")

extracted_chars = []
for match in matches:
    # 抽出された部分から英数字とアンダースコア "_"、波括弧 "{}" のみを残す
    # 記号ノイズを除去する
    clean_match = re.sub(r"[^a-zA-Z0-9_{}]", "", match)
    if clean_match:
        extracted_chars.append(clean_match)
        print(f"Extracted: {clean_match} from ({match})")

# 連結してみる
result = "".join(extracted_chars)
print(f"\nPotential Flag String: {result}")
