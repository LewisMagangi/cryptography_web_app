"""
Implementation of hashing algorithms:
Hashing Algorithms
SHA-1 (Secure Hash Algorithm 1)
SHA-2 (Secure Hash Algorithm 2) family: including SHA-224, SHA-256, SHA-384, SHA-512
MD5 (Message Digest Algorithm 5)
HMAC (Hash-based Message Authentication Code)
"""
from Crypto.Hash import SHA1, SHA224, SHA256, SHA384, SHA512, MD5, HMAC
from Crypto.Random import get_random_bytes

class SHA1Hash:
    """
    Class to perform SHA-1 hashing.
    """
    def hash(self, message):
        """
        Hash the message using SHA-1.
        
        :param message: The message to hash.
        :return: The hash digest.
        """
        h = SHA1.new()
        h.update(message.encode())
        return h.hexdigest()

class SHA2Hash:
    """
    Class to perform SHA-2 hashing.
    """
    def __init__(self, algorithm='SHA-256'):
        """
        Initialize the SHA-2 hash with the specified algorithm.
        
        :param algorithm: The SHA-2 algorithm to use (default is 'SHA-256').
        """
        self.algorithm = algorithm

    def hash(self, message):
        """
        Hash the message using SHA-2.
        
        :param message: The message to hash.
        :return: The hash digest.
        """
        if self.algorithm == 'SHA-224':
            h = SHA224.new()
        elif self.algorithm == 'SHA-256':
            h = SHA256.new()
        elif self.algorithm == 'SHA-384':
            h = SHA384.new()
        elif self.algorithm == 'SHA-512':
            h = SHA512.new()
        else:
            raise ValueError("Unsupported SHA-2 algorithm")
        
        h.update(message.encode())
        return h.hexdigest()

class MD5Hash:
    """
    Class to perform MD5 hashing.
    """
    def hash(self, message):
        """
        Hash the message using MD5.
        
        :param message: The message to hash.
        :return: The hash digest.
        """
        h = MD5.new()
        h.update(message.encode())
        return h.hexdigest()

class HMACHash:
    """
    Class to perform HMAC hashing.
    """
    def __init__(self, key=None, algorithm='SHA-256'):
        """
        Initialize the HMAC with a random key and the specified algorithm.
        
        :param key: The key to use for HMAC (default is a random key).
        :param algorithm: The hash algorithm to use for HMAC (default is 'SHA-256').
        """
        self.key = key or get_random_bytes(16)
        self.algorithm = algorithm

    def hash(self, message):
        """
        Hash the message using HMAC.
        
        :param message: The message to hash.
        :return: The HMAC digest.
        """
        if self.algorithm == 'SHA-1':
            h = HMAC.new(self.key, digestmod=SHA1)
        elif self.algorithm == 'SHA-224':
            h = HMAC.new(self.key, digestmod=SHA224)
        elif self.algorithm == 'SHA-256':
            h = HMAC.new(self.key, digestmod=SHA256)
        elif self.algorithm == 'SHA-384':
            h = HMAC.new(self.key, digestmod=SHA384)
        elif self.algorithm == 'SHA-512':
            h = HMAC.new(self.key, digestmod=SHA512)
        elif self.algorithm == 'MD5':
            h = HMAC.new(self.key, digestmod=MD5)
        else:
            raise ValueError("Unsupported HMAC algorithm")
        
        h.update(message.encode())
        return h.hexdigest()