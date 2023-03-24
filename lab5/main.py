import random
import time
from math import gcd

import pandas as pd
from typing import Tuple

ALPHABET = """1234567890«»АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюяXVI.,!?;:-()[]{}""''— """


def is_coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


def e(x: int, a: int, b: int, m: int) -> int:
    return (a * x + b) % m


def d(x: int, a: int, b: int, m: int) -> int:
    return (pow(a, -1, m) * (x - b)) % m


def encrypt(msg: str, a: int, b: int, m: int) -> str:
    return "".join(
        [ALPHABET[i] for i in map(lambda x: e(ALPHABET.index(x), a, b, m), msg)]
    )


def decrypt(msg: str, a: int, b: int, m: int) -> str:
    return "".join(
        [ALPHABET[i] for i in map(lambda x: d(ALPHABET.index(x), a, b, m), msg)]
    )


def bruteforce(msg: str, original_msg: str) -> Tuple[str, int, int]:
    m = len(ALPHABET)

    for a in range(2, m):
        if not is_coprime(a, m):
            continue
        for b in range(1, m):
            bruteforced_msg = "".join(
                [ALPHABET[i] for i in map(lambda x: d(ALPHABET.index(x), a, b, m), msg)]
            )
            if bruteforced_msg == original_msg:
                return bruteforced_msg, a, b


def main():
    m = len(ALPHABET)

    a = random.randint(2, m)
    while not is_coprime(a, m):
        a = random.randint(1, m)
    b = random.randint(1, 1000)

    stats = {}
    for file_path in ("short.txt", "medium.txt", "long.txt"):
        stats[file_path] = {}

        stats[file_path][(a, b)] = {}
        with open(file_path, mode="r") as f:
            msg = f.read()
        print(f"Original message:\n{msg}")
        encryption_start = time.perf_counter()
        encrypted_msg = encrypt(msg, a, b, m)
        stats[file_path][(a, b)]["Encryption time"] = (
            time.perf_counter() - encryption_start
        )
        print(f"Encrypted message:\n{encrypted_msg}")

        decryption_start = time.perf_counter()
        decrypted_msg = decrypt(encrypted_msg, a, b, m)
        stats[file_path][(a, b)]["Decryption time"] = (
            time.perf_counter() - decryption_start
        )
        print(f"Decrypted message:\n{decrypted_msg}")

        bruteforce_start = time.perf_counter()
        bruteforced_msg = bruteforce(encrypted_msg, decrypted_msg)[0]
        stats[file_path][(a, b)]["Bruteforce time"] = (
            time.perf_counter() - bruteforce_start
        )
        print(f"Bruteforced message:\n{bruteforced_msg}")

    df = pd.concat(
        {k: pd.DataFrame.from_dict(v, "index") for k, v in stats.items()}, axis=0
    )
    df.round(6).to_csv("df.csv")


if __name__ == "__main__":
    main()
