from Crypto.PublicKey import DSA
from Crypto.PublicKey.DSA import DsaKey
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

from docx import Document


def read_from_docx(file_path: str) -> str:
    return Document(file_path).paragraphs[0].text


def export_pub_key(key: DsaKey, file_path: str = "public_key.pem") -> None:
    with open(file_path, "bw") as f:
        f.write(key.public_key().export_key())


def import_pub_key(file_path: str = "public_key.pem") -> DsaKey:
    with open(file_path, "r") as f:
        key: DsaKey = DSA.import_key(f.read())
    return key


def main():
    # user1 sends a message to user2
    msg = read_from_docx("msg1.docx").encode()

    key12 = DSA.generate(2048)
    export_pub_key(key12, file_path="public_key12.pem")
    h = SHA256.new(msg)
    signer = DSS.new(key12, "fips-186-3")
    signature = signer.sign(h)

    # user2 receives the message from user1 and verifies it
    key12 = import_pub_key(file_path="public_key12.pem")
    h = SHA256.new(msg)
    verifier = DSS.new(key12, "fips-186-3")

    try:
        verifier.verify(h, signature)
        print("The message from 1 to 2 is authentic.")
        print(f"message: {msg}\n\n")
    except ValueError:
        print("The message from 1 to 2  is not authentic.")

    # user2 sends a response to user1
    response = read_from_docx("response1.docx").encode()

    key21 = DSA.generate(2048)
    export_pub_key(key21, file_path="public_key21.pem")
    h = SHA256.new(response)
    signer = DSS.new(key21, "fips-186-3")
    signature = signer.sign(h)

    # user1 receives the response from user2 and verifies it
    key21 = import_pub_key(file_path="public_key21.pem")
    h = SHA256.new(response)
    verifier = DSS.new(key21, "fips-186-3")

    try:
        verifier.verify(h, signature)
        print("The message from 2 to 1 is authentic.")
        print(f"message: {response}")
    except ValueError:
        print("The message from 2 to 1  is not authentic.")


if __name__ == "__main__":
    main()
