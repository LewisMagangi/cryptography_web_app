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
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class AESEncryption:
    """
    Class to perform AES encryption and decryption.
    """
    def __init__(self, key_size=32):
        """
        Initialize the AES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 32 bytes for AES-256).
        """
        self.key = get_random_bytes(key_size)
        self.cipher = AES.new(self.key, AES.MODE_GCM)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using AES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        ciphertext, tag = self.cipher.encrypt_and_digest(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(self.cipher.nonce + tag + ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using AES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        data = base64.b64decode(ciphertext)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        plaintext = unpad(cipher.decrypt_and_verify(ciphertext, tag), AES.block_size)
        return plaintext.decode('utf-8')

class DESEncryption:
    """
    Class to perform DES encryption and decryption.
    """
    def __init__(self, key_size=8):
        """
        Initialize the DES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 8 bytes for DES).
        """
        self.key = get_random_bytes(key_size)
        self.cipher = DES.new(self.key, DES.MODE_ECB)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        ciphertext = self.cipher.encrypt(pad(plaintext.encode(), DES.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using DES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        data = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(data), DES.block_size)
        return plaintext.decode('utf-8')

class DES3Encryption:
    """
    Class to perform 3DES encryption and decryption.
    """
    def __init__(self, key_size=24):
        """
        Initialize the 3DES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 24 bytes for 3DES).
        """
        self.key = get_random_bytes(key_size)
        self.cipher = DES3.new(self.key, DES3.MODE_ECB)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using 3DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        ciphertext = self.cipher.encrypt(pad(plaintext.encode(), DES3.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using 3DES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        data = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(data), DES3.block_size)
        return plaintext.decode('utf-8')

class RC2Encryption:
    """
    Class to perform RC2 encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the RC2 cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for RC2).
        """
        self.key = get_random_bytes(key_size)
        self.cipher = ARC2.new(self.key, ARC2.MODE_ECB)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using RC2.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        ciphertext = self.cipher.encrypt(pad(plaintext.encode(), ARC2.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using RC2.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        data = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(data), ARC2.block_size)
        return plaintext.decode('utf-8')

class RC4Encryption:
    """
    Class to perform RC4 encryption and decryption.
    """
    '''
    def __init__(self, key_size=16):
        """
        Initialize the RC4 cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for RC4).
        """
        self.key = get_random_bytes(key_size)
        self.cipher = ARC4.new(self.key)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using RC4.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        ciphertext = self.cipher.encrypt(plaintext.encode())
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using RC4.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        data = base64.b64decode(ciphertext)
        plaintext = self.cipher.decrypt(data)
        return plaintext.decode('utf-8')
        '''
    pass

class BlowfishEncryption:
    """
    Class to perform Blowfish encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the Blowfish cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for Blowfish).
        """
        self.key = get_random_bytes(key_size)
        self.cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using Blowfish.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        ciphertext = self.cipher.encrypt(pad(plaintext.encode(), Blowfish.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using Blowfish.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        data = base64.b64decode(ciphertext)
        plaintext = unpad(self.cipher.decrypt(data), Blowfish.block_size)
        return plaintext.decode('utf-8')
