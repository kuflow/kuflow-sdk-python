#
# MIT License
#
# Copyright (c) 2022 KuFlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
from abc import ABC, abstractmethod

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Cipher(ABC):
    @property
    @abstractmethod
    def algorithm(self) -> str:
        """Name of the encryption algorithm."""
        pass

    @abstractmethod
    async def encrypt(self, key: bytes, plain_text: bytes) -> bytes:
        """Encrypts the plain text using the given key."""
        pass

    @abstractmethod
    async def decrypt(self, key: bytes, cipher_text: bytes) -> bytes:
        """Decrypts the cipher text using the given key."""
        pass


class CipherAes256GCM(Cipher):
    @property
    def algorithm(self) -> str:
        return "AES-256-GCM"

    async def encrypt(self, key: bytes, plain_text: bytes) -> bytes:
        encryptor = AESGCM(key)
        nonce = os.urandom(12)

        return nonce + encryptor.encrypt(nonce, plain_text, None)

    async def decrypt(self, key: bytes, cipher_text: bytes) -> bytes:
        encryptor = AESGCM(key)

        return encryptor.decrypt(cipher_text[:12], cipher_text[12:], None)


class CIPHERS:
    AES_256_GCM = CipherAes256GCM()
