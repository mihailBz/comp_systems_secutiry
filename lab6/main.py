from typing import List
import time

from docx import Document
import pandas as pd


def ksa(key: str) -> List[int]:
    """Key Scheduling Algorithm"""
    s = list(range(256))

    j = 0
    for i in range(256):
        j = (j + s[i] + ord(key[i % len(key)])) % 256
        s[i], s[j] = s[j], s[i]
    return s


def prga(s: List[int], data_len: int) -> List[int]:
    """Pseudo-Random Generation Algorithm"""
    ks = []
    j = 0
    i = 0
    for _ in range(data_len):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        ks.append(s[(s[i] + s[j]) % 256])
    return ks


def encrypt(msg: str, key: str) -> List[int]:
    s = ksa(key)
    ks = prga(s, len(msg))
    out = []
    for char, k in zip(msg, ks):
        out.append(ord(char) ^ k)
    return out


def decrypt(msg: List[int], key: str) -> List[int]:
    S = ksa(key)
    ks = prga(S, len(msg))
    out = []
    for char, k in zip(msg, ks):
        out.append(char ^ k)
    return out


def main():
    key = "7179875849"

    document = Document("medium.docx")
    with open("medium.txt", mode="w") as f:
        f.write(document.paragraphs[0].text)

    stats = {}
    for file_path in ("short.txt", "medium.txt", "long.txt"):
        stats[file_path] = {}
        stats[file_path][key] = {}

        with open(file_path, mode="r") as f:
            msg = f.read()

        print(f"Original message:\n{msg}")
        encryption_start = time.perf_counter()
        encrypted_msg = encrypt(msg, key)
        stats[file_path][key]["Encryption time"] = (
            time.perf_counter() - encryption_start
        )
        print(f"Encrypted message:\n{''.join([chr(i) for i in encrypted_msg])}")

        decryption_start = time.perf_counter()
        decrypted_msg = decrypt(encrypted_msg, key)
        stats[file_path][key]["Decryption time"] = (
            time.perf_counter() - decryption_start
        )
        print(f"Decrypted message:\n{''.join([chr(i) for i in decrypted_msg])}")
    df = pd.concat(
        {k: pd.DataFrame.from_dict(v, "index") for k, v in stats.items()}, axis=0
    )
    df.round(6).to_csv("df.csv")


if __name__ == "__main__":
    main()
