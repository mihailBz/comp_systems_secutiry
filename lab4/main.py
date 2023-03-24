import random
import time

import numpy as np
import pandas as pd
from typing import Tuple


def encrypt(msg: str, key: int) -> str:
    m = key
    n = (len(msg) // m) + 1

    fillers = (m * n - len(msg)) * "_"
    matrix = np.reshape(np.array(list(msg + fillers)), (m, n))
    return "".join(matrix.flatten("F"))


def decrypt(msg: str, key: int) -> str:
    m = key
    n = len(msg) // m

    matrix = np.reshape(np.array(list(msg)), (n, m))
    return "".join(matrix.flatten("F"))


def bruteforce(msg: str, original_msg: str) -> Tuple[str, int]:
    for i in range(1, 100):
        m = i
        n = len(msg) // m
        if len(msg) > m * n:
            continue
        matrix = np.reshape(np.array(list(msg)), (n, m))
        bruteforced_msg = "".join(matrix.flatten("F"))
        if bruteforced_msg == original_msg:
            return bruteforced_msg, i
    print()


def main():
    stats = {}
    for file_path in ("short.txt", "medium.txt", "long.txt"):
        stats[file_path] = {}
        for key in random.choices(range(1, 100), k=5):
            stats[file_path][key] = {}
            with open(file_path, mode="r") as f:
                msg = f.read()
            print(f"Original message:\n{msg}")
            encryption_start = time.perf_counter()
            encrypted_msg = encrypt(msg, key)
            stats[file_path][key]["Encryption time"] = (
                time.perf_counter() - encryption_start
            )
            print(f"Encrypted message:\n{encrypted_msg}")

            decryption_start = time.perf_counter()
            decrypted_msg = decrypt(encrypted_msg, key)
            stats[file_path][key]["Decryption time"] = (
                time.perf_counter() - decryption_start
            )
            print(f"Decrypted message:\n{decrypted_msg}")

            bruteforce_start = time.perf_counter()
            bruteforced_msg = bruteforce(encrypted_msg, decrypted_msg)[0]
            stats[file_path][key]["Bruteforce time"] = (
                time.perf_counter() - bruteforce_start
            )
            print(f"Bruteforced message:\n{bruteforced_msg}")

    df = pd.concat(
        {k: pd.DataFrame.from_dict(v, "index") for k, v in stats.items()}, axis=0
    )
    df.round(6).to_csv("df.csv")


if __name__ == "__main__":
    main()
