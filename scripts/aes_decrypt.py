#!/usr/bin/env python3
"""
aes_decrypt.py

Decrypts a Base64 ciphertext produced by CryptoJS's default
`CryptoJS.AES.encrypt(text, passphrase)` call. CryptoJS uses an
OpenSSL-compatible format: the raw bytes are `"Salted__" + 8-byte
salt + ciphertext`, and the AES key/IV are derived from the
passphrase and salt using OpenSSL's EVP_BytesToKey (MD5-based) KDF.

Requires: pycryptodome
    pip install pycryptodome

Usage:
    python3 aes_decrypt.py "<base64 ciphertext>" "<passphrase>"
"""

import argparse
import base64
import hashlib

from Crypto.Cipher import AES


def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16) -> tuple[bytes, bytes]:
    """Re-implements OpenSSL's EVP_BytesToKey (MD5 digest), matching CryptoJS defaults."""
    derived = b""
    block = b""
    while len(derived) < key_len + iv_len:
        block = hashlib.md5(block + password + salt).digest()
        derived += block
    return derived[:key_len], derived[key_len:key_len + iv_len]


def decrypt(ciphertext_b64: str, passphrase: str) -> bytes:
    raw = base64.b64decode(ciphertext_b64)
    if raw[:8] != b"Salted__":
        raise ValueError("Ciphertext does not look like OpenSSL/CryptoJS format (missing 'Salted__' header).")

    salt = raw[8:16]
    ciphertext = raw[16:]

    key, iv = evp_bytes_to_key(passphrase.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ciphertext)

    pad_len = padded[-1]
    if not (1 <= pad_len <= 16) or padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Decryption failed or passphrase is incorrect (bad padding).")

    return padded[:-pad_len]


def main():
    parser = argparse.ArgumentParser(description="Decrypt a CryptoJS AES-encrypted Base64 string.")
    parser.add_argument("ciphertext", help="Base64-encoded ciphertext (CryptoJS/OpenSSL format)")
    parser.add_argument("passphrase", help="Passphrase/key used for encryption")
    args = parser.parse_args()

    try:
        result = decrypt(args.ciphertext, args.passphrase)
        print(result.decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
