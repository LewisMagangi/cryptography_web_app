"""
Implementation of asymmetric encryption and decryption of the following algorithms:
Asymmetric Algorithms
RSA (Rivest-Shamir-Adleman)
DSA (Digital Signature Algorithm)
DH (Diffie-Hellman)
ECC (Elliptic Curve Cryptography)
"""
from Crypto.PublicKey import RSA, DSA, ECC
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import time

class RSAEncryption:
    """
    Class to perform RSA encryption and decryption.
    """
    def __init__(self, key_size=2048):
        """
        Initialize the RSA with a random key pair.
        
        :param key_size: Size of the key in bits (default is 2048 bits).
        """
        self.key = RSA.generate(key_size)
        self.cipher = PKCS1_OAEP.new(self.key)
        self.name = "RSAEncryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using RSA.
        
        :param plaintext: The plaintext to encrypt.
        :return: The encrypted ciphertext.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')  # Convert to bytes
        ciphertext = self.cipher.encrypt(plaintext)
        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using RSA.
        
        :param ciphertext: The ciphertext to decrypt.
        :return: The decrypted plaintext.
        """
        plaintext = self.cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8')

    def run(self, data, key_size):
        """
        Run the RSA encryption and decryption process separately and combine the results.
        
        :param data: The data to encrypt and decrypt.
        :param key_size: Size of the key in bits.
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

class DSAEncryption:
    """
    Class to perform DSA signing and verification.
    """
    def __init__(self, key_size=2048):
        """
        Initialize the DSA with a random key pair.
        
        :param key_size: Size of the key in bits (default is 2048 bits).
        """
        self.key = DSA.generate(key_size)
        self.public_key = self.key.publickey()
        self.name = "DSAEncryption"
        self.execution_time = 0

    def sign(self, message):
        """
        Sign the message using DSA.
        
        :param message: The message to sign.
        :return: The signature.
        """
        h = SHA256.new(message.encode())
        signer = DSS.new(self.key, 'fips-186-3')
        signature = signer.sign(h)
        return signature

    def verify(self, message, signature):
        """
        Verify the signature using DSA.
        
        :param message: The message to verify.
        :param signature: The signature to verify.
        :return: True if the signature is valid, False otherwise.
        """
        h = SHA256.new(message.encode())
        verifier = DSS.new(self.public_key, 'fips-186-3')
        try:
            verifier.verify(h, signature)
            return True
        except ValueError:
            return False

    def run(self, data, key_size):
        """
        Run the DSA signing and verification process separately and combine the results.
        
        :param data: The data to sign and verify.
        :param key_size: Size of the key in bits.
        """
        # Signing
        start_time = time.time()
        signature = self.sign(data)
        signing_time = time.time() - start_time

        # Verification
        start_time = time.time()
        self.verify(data, signature)
        verification_time = time.time() - start_time

        self.execution_time = signing_time + verification_time

class ECCEncryption:
    """
    Class to perform ECC signing and verification.
    """
    def __init__(self, curve='P-256'):
        """
        Initialize the ECC with a random key pair.
        
        :param curve: The elliptic curve to use (default is 'P-256').
        """
        self.key = ECC.generate(curve=curve)
        self.public_key = self.key.public_key()
        self.name = "ECCEncryption"
        self.execution_time = 0

    def sign(self, message):
        """
        Sign the message using ECC.
        
        :param message: The message to sign.
        :return: The signature.
        """
        h = SHA256.new(message.encode())
        signer = DSS.new(self.key, 'fips-186-3')
        signature = signer.sign(h)
        return signature

    def verify(self, message, signature):
        """
        Verify the signature using ECC.
        
        :param message: The message to verify.
        :param signature: The signature to verify.
        :return: True if the signature is valid, False otherwise.
        """
        h = SHA256.new(message.encode())
        verifier = DSS.new(self.public_key, 'fips-186-3')
        try:
            verifier.verify(h, signature)
            return True
        except ValueError:
            return False

    def run(self, data, key_size):
        """
        Run the ECC signing and verification process separately and combine the results.
        
        :param data: The data to sign and verify.
        :param key_size: Size of the key in bits.
        """
        # Signing
        start_time = time.time()
        signature = self.sign(data)
        signing_time = time.time() - start_time

        # Verification
        start_time = time.time()
        self.verify(data, signature)
        verification_time = time.time() - start_time

        self.execution_time = signing_time + verification_time

class DHEncryption:
    """
    Class to perform Diffie-Hellman key exchange.
    """
    def __init__(self, key_size=2048):
        """
        Initialize the Diffie-Hellman parameters and generate a key pair.
        
        :param key_size: Size of the key in bits (default is 2048 bits).
        """
        self.parameters = dh.generate_parameters(generator=2, key_size=key_size)
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()
        self.name = "DHEncryption"
        self.execution_time = 0

    def generate_shared_key(self, peer_public_key):
        """
        Generate a shared key using the peer's public key.
        
        :param peer_public_key: The peer's public key.
        :return: The shared key.
        """
        shared_key = self.private_key.exchange(peer_public_key)
        return shared_key

    def run(self, data, key_size):
        """
        Run the Diffie-Hellman key exchange process.
        
        :param data: Not used in this context.
        :param key_size: Size of the key in bits.
        """
        # Generate the other party's Diffie-Hellman key pair
        other_party_private_key = self.parameters.generate_private_key()
        other_party_public_key = other_party_private_key.public_key()

        # Generate shared keys
        start_time = time.time()
        self.generate_shared_key(other_party_public_key)
        self.execution_time = time.time() - start_time