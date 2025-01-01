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
    def __init__(self, key_size=256):
        """
        Initialize the AES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 32 bytes for AES-256).
        """
        self.key = get_random_bytes(key_size // 8)
        self.cipher = AES.new(self.key, AES.MODE_GCM)

    def pad(self, data):
        padding_length = 16 - (len(data) % 16)  # Calculate padding length
        return data + bytes([padding_length]) * padding_length

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using AES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')  # Convert to bytes if str
        padded_plaintext = self.pad(plaintext)  # Pad the plaintext
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(padded_plaintext)
        nonce = cipher.nonce
        return ciphertext, tag, nonce

    def unpad(self, data):
        padding_length = data[-1]  # Last byte indicates padding length
        return data[:-padding_length]

    def decrypt(self, ciphertext, tag, nonce):
        """
        Decrypt the ciphertext using AES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
        return self.unpad(decrypted_text)  # Remove padding after decryption

class DESEncryption:
    """
    Class to perform DES encryption and decryption.
    """
    def __init__(self, key_size=8):
        """
        Initialize the DES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 8 bytes for DES).
        """
        if key_size != 8:
            raise ValueError("Key size for DES must be 8bytes.")
        
        self.key = get_random_bytes(key_size)
        self.cipher = DES.new(self.key, DES.MODE_ECB)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        
        try:
            # Ensure the plaintext is in bytes
            if isinstance(plaintext, str):
                plaintext = plaintext.encode()

            # Perform encryption with padding
            padded_data = pad(plaintext, DES.block_size)
            ciphertext = self.cipher.encrypt(padded_data)

            # Encode the ciphertext in base64 and return
            return base64.b64encode(ciphertext).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using DES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        try:
            # Ensure the ciphertext is in bytes
            if isinstance(ciphertext, str):
                ciphertext = base64.b64decode(ciphertext)
            else:
                ciphertext = base64.b64decode(ciphertext.decode())

            plaintext = unpad(self.cipher.decrypt(ciphertext), DES.block_size)
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

class DES3Encryption:
    """
    Class to perform 3DES encryption and decryption.
    """
    def __init__(self, key_size=24):
        """
        Initialize the 3DES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 24 bytes for 3DES).
        """
        if key_size not in [16, 24]:
            raise ValueError("Key size for DES3 must be 16 or 24 bytes.")

        self.key = get_random_bytes(key_size)
        DES3.adjust_key_parity(self.key)
        self.cipher = DES3.new(self.key, DES3.MODE_ECB)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using 3DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

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
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

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

class RC4Encryption:
    """
    Class to perform RC4 encryption and decryption.
    """
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
        if isinstance(plaintext, str):
            plaintext = plaintext.encode() 
        ciphertext = self.cipher.encrypt(plaintext)
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
        if isinstance(plaintext, str):  # Check if it's a string
            plaintext = plaintext.encode()
        ciphertext = self.cipher.encrypt(pad(plaintext, Blowfish.block_size))
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
