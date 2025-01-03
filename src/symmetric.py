"""
Implementation of symmetric encryption and decryption of the following algorithms:
Symmetric Algorithms
AES (Advanced Encryption Standard)
DES (Data Encryption Standard)
3DES (Triple Data Encryption Standard)
RC2
RC4
Blowfish
"""
from Crypto.Cipher import AES, DES, DES3, ARC2, ARC4, Blowfish
from Crypto.Util.Padding import pad, unpad
import base64
import time
import os
import csv

# Define constants
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text')
ANALYSIS_RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'symmetric_analysis_results.csv')

class AESEncryption:
    """
    Class to perform AES encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the AES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for AES-128).
        """
        self.key = b'Sixteen byte key'
        self.name = "AESEncryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using AES-GCM.
        
        :param plaintext: The plaintext to encrypt.
        :return: The ciphertext, tag, and nonce.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(tag).decode('utf-8'), base64.b64encode(cipher.nonce).decode('utf-8')

    def decrypt(self, ciphertext, tag, nonce):
        """
        Decrypt the ciphertext using AES-GCM.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :param tag: The base64 encoded tag.
        :param nonce: The base64 encoded nonce.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        if isinstance(tag, str):
            tag = base64.b64decode(tag)
        if isinstance(nonce, str):
            nonce = base64.b64decode(nonce)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')

    def run(self, data, key_size):
        """
        Run the AES encryption and decryption process separately and combine the results.
        
        :param data: The data to encrypt and decrypt.
        :param key_size: Size of the key in bytes.
        """
        # Encryption
        start_time = time.time()
        ciphertext, tag, nonce = self.encrypt(data)
        encryption_time = time.time() - start_time

        # Decryption
        start_time = time.time()
        self.decrypt(ciphertext, tag, nonce)
        decryption_time = time.time() - start_time

        self.execution_time = encryption_time + decryption_time

class DESEncryption:
    """
    Class to perform DES encryption and decryption.
    """
    def __init__(self, key_size=8):
        """
        Initialize the DES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 8 bytes for DES).
        """
        self.key = b'EightKey'
        self.cipher = DES.new(self.key, DES.MODE_ECB)
        self.name = "DESEncryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        ciphertext = self.cipher.encrypt(pad(plaintext, DES.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using DES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode()
        data = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(data), DES.block_size)
        return plaintext.decode('utf-8')

    def run(self, data, key_size):
        """
        Run the DES encryption and decryption process separately and combine the results.
        
        :param data: The data to encrypt and decrypt.
        :param key_size: Size of the key in bytes.
        """
        # Encryption
        start_time = time.time()
        ciphertext = self.encrypt(data)
        encryption_time = time.time() - start_time

        # Decryption
        start_time = time.time()
        self.decrypt(ciphertext)
        decryption_time = time.time() - start_time

        self.execution_time = encryption_time + decryption_time

class DES3Encryption:
    """
    Class to perform 3DES encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the 3DES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for 3DES).
        """
        self.key = b'Sixteen byte key'
        self.cipher = DES3.new(self.key, DES3.MODE_ECB)
        self.name = "DES3Encryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using 3DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        ciphertext = self.cipher.encrypt(pad(plaintext, DES3.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using 3DES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode()
        data = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(data), DES3.block_size)
        return plaintext.decode('utf-8')

    def run(self, data, key_size):
        """
        Run the 3DES encryption and decryption process separately and combine the results.
        
        :param data: The data to encrypt and decrypt.
        :param key_size: Size of the key in bytes.
        """
        # Encryption
        start_time = time.time()
        ciphertext = self.encrypt(data)
        encryption_time = time.time() - start_time

        # Decryption
        start_time = time.time()
        self.decrypt(ciphertext)
        decryption_time = time.time() - start_time

        self.execution_time = encryption_time + decryption_time

class RC2Encryption:
    """
    Class to perform RC2 encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the RC2 cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for RC2).
        """
        self.key = b'Sixteen byte key'
        self.cipher = ARC2.new(self.key, ARC2.MODE_ECB)
        self.name = "RC2Encryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using RC2.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        ciphertext = self.cipher.encrypt(pad(plaintext, ARC2.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using RC2.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode()
        data = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(data), ARC2.block_size)
        return plaintext.decode('utf-8')

    def run(self, data, key_size):
        """
        Run the RC2 encryption and decryption process separately and combine the results.
        
        :param data: The data to encrypt and decrypt.
        :param key_size: Size of the key in bytes.
        """
        # Encryption
        start_time = time.time()
        ciphertext = self.encrypt(data)
        encryption_time = time.time() - start_time

        # Decryption
        start_time = time.time()
        self.decrypt(ciphertext)
        decryption_time = time.time() - start_time

        self.execution_time = encryption_time + decryption_time

class RC4Encryption:
    """
    Class to perform RC4 encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the RC4 cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for RC4).
        """
        self.key = b'Sixteen byte key'
        #self.cipher = ARC4.new(self.key)
        self.name = "RC4Encryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using RC4.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        cipher = ARC4.new(self.key)   
        ciphertext = cipher.encrypt(plaintext)
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using RC4.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        cipher = ARC4.new(self.key)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8')

    def run(self, data, key_size):
        """
        Run the RC4 encryption and decryption process separately and combine the results.
        
        :param data: The data to encrypt and decrypt.
        :param key_size: Size of the key in bytes.
        """
        # Encryption
        start_time = time.time()
        ciphertext = self.encrypt(data)
        encryption_time = time.time() - start_time

        # Decryption
        start_time = time.time()
        self.decrypt(ciphertext)
        decryption_time = time.time() - start_time

        self.execution_time = encryption_time + decryption_time

class BlowfishEncryption:
    """
    Class to perform Blowfish encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the Blowfish cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for Blowfish).
        """
        self.key = b'Sixteen byte key'
        self.cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)
        self.name = "BlowfishEncryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using Blowfish.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        ciphertext = self.cipher.encrypt(pad(plaintext, Blowfish.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using Blowfish.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(ciphertext), Blowfish.block_size)
        return plaintext.decode('utf-8')

    def run(self, data, key_size):
        """
        Run the Blowfish encryption and decryption process separately and combine the results.
        
        :param data: The data to encrypt and decrypt.
        :param key_size: Size of the key in bytes.
        """
        # Encryption
        start_time = time.time()
        ciphertext = self.encrypt(data)
        encryption_time = time.time() - start_time

        # Decryption
        start_time = time.time()
        self.decrypt(ciphertext)
        decryption_time = time.time() - start_time

        self.execution_time = encryption_time + decryption_time
