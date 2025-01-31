"""
Implementation of asymmetric algorithms:
Asymmetric Algorithms
RSA (Rivest-Shamir-Adleman)
DSA (Digital Signature Algorithm)
DH (Diffie-Hellman)
ECC (Elliptic Curve Cryptography)
"""
import os
import time
import csv
from Crypto.PublicKey import RSA, DSA, ECC
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15, DSS
from Crypto.Hash import SHA256
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Define constants
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'smaller_sample_text')
ANALYSIS_RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'asymmetric_analysis_results.csv')

class RSAEncryption:
    """
    Class to perform RSA encryption, decryption, signing, and verification.
    """
    def __init__(self, key_size=2048):
        """
        Initialize the RSA encryption with the specified key size.
        
        :param key_size: Size of the RSA key in bits (default is 2048).
        """
        self.key_size = key_size
        self.key = RSA.generate(key_size)
        self.cipher = PKCS1_OAEP.new(self.key)

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

    def sign(self, message):
        """
        Sign the message using RSA.
        
        :param message: The message to sign.
        :return: The signature.
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        h = SHA256.new(message)
        signature = pkcs1_15.new(self.key).sign(h)
        return signature

    def verify(self, message, signature):
        """
        Verify the signature using RSA.
        
        :param message: The message to verify.
        :param signature: The signature to verify.
        :return: True if the signature is valid, False otherwise.
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        h = SHA256.new(message)
        try:
            pkcs1_15.new(self.key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

class DSAEncryption:
    """
    Class to perform DSA signing and verification.
    """
    def __init__(self, key_size=2048):
        """
        Initialize the DSA signing with the specified key size.
        
        :param key_size: Size of the DSA key in bits (default is 2048).
        """
        self.key_size = key_size
        self.key = DSA.generate(key_size)

    def sign(self, message):
        """
        Sign the message using DSA.
        
        :param message: The message to sign.
        :return: The signature.
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        h = SHA256.new(message)
        signer = DSS.new(self.key, 'fips-186-3')
        return signer.sign(h)

    def verify(self, message, signature):
        """
        Verify the signature using DSA.
        
        :param message: The message to verify.
        :param signature: The signature to verify.
        :return: True if the signature is valid, False otherwise.
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        h = SHA256.new(message)
        verifier = DSS.new(self.key, 'fips-186-3')
        try:
            verifier.verify(h, signature)
            return True
        except ValueError:
            return False

class DiffieHellmanEncryption:
    """
    Class to perform Diffie-Hellman key exchange.
    """
    def __init__(self, key_size=2048):
        """
        Initialize the Diffie-Hellman parameters and generate a key pair.
        
        :param key_size: Size of the key in bits (default is 2048 bits).
        """
        self.parameters = dh.generate_parameters(generator=2, key_size=key_size, backend=default_backend())
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()
        self.name = "DiffieHellmanEncryption"
        self.execution_time = 0

    def generate_shared_key(self, peer_public_key):
        """
        Generate a shared key using the peer's public key.
        
        :param peer_public_key: The peer's public key.
        :return: The derived shared key.
        """
        shared_key = self.private_key.exchange(peer_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'dh_key_exchange',
            backend=default_backend()
        ).derive(shared_key)
        return derived_key

    def run(self, key_size):
        """
        Run the Diffie-Hellman key exchange process.
        
        :param key_size: Size of the key in bits.
        """
        # Generate the other party's Diffie-Hellman key pair
        other_party_private_key = self.parameters.generate_private_key()
        other_party_public_key = other_party_private_key.public_key()

        # Generate shared keys
        start_time = time.time()
        self.generate_shared_key(other_party_public_key)
        self.execution_time = time.time() - start_time

class ECCEncryption:
    """
    Class to perform ECC signing and verification.
    """
    def __init__(self, curve='P-256'):
        """
        Initialize the ECC signing with the specified curve.
        
        :param curve: The ECC curve to use (default is 'P-256').
        """
        self.curve = curve
        self.key = ECC.generate(curve=curve)

    def sign(self, message):
        """
        Sign the message using ECC.
        
        :param message: The message to sign.
        :return: The signature.
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        h = SHA256.new(message)
        signer = DSS.new(self.key, 'fips-186-3')
        return signer.sign(h)

    def verify(self, message, signature):
        """
        Verify the signature using ECC.
        
        :param message: The message to verify.
        :param signature: The signature to verify.
        :return: True if the signature is valid, False otherwise.
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        h = SHA256.new(message)
        verifier = DSS.new(self.key.public_key(), 'fips-186-3')
        try:
            verifier.verify(h, signature)
            return True
        except ValueError:
            return False

def measure_time(func):
    """
    Decorator to measure the time taken by a function.
    
    :param func: The function to measure.
    :return: The time taken and the function's result.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time, result
    return wrapper

def save_results(algorithm, operation, key_size, file_name, time_taken, rate):
    """
    Save the time taken for an operation to a CSV file.
    
    :param algorithm: The name of the algorithm.
    :param operation: The operation performed (e.g., encryption, signing).
    :param key_size: The size of the key or curve.
    :param file_name: The name of the file used.
    :param time_taken: The time taken for the operation.
    :param rate: The bytes/s rate for the operation.
    """
    with open(ANALYSIS_RESULTS_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([algorithm, operation, key_size, file_name, time_taken, rate])

def calculate_bytes_rate(time_taken, filename):
    """Calculate bytes/s rate from time and filename."""
    try:
        size_bytes = int(filename.split('bytes')[0])
        return size_bytes / time_taken if time_taken > 0 else 0
    except:
        return 0

if __name__ == "__main__":
    # Initialize results file
    with open(ANALYSIS_RESULTS_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['algorithm', 'operation', 'key_size', 'file_name', 'time_taken', 'rate'])

    # Test data files
    sample_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    key_sizes = {
        'RSA': [2048, 3072, 4096],
        'DSA': [1024, 2048, 3072],
        'DH': [2048, 3072, 4096],
        'ECC': ['P-256', 'P-384', 'P-521']
    }

    for file_name in sample_files:
        with open(os.path.join(DATA_DIR, file_name), 'r') as file:
            data = file.read()

        # RSA Tests
        for key_size in key_sizes['RSA']:
            rsa = RSAEncryption(key_size)
            
            # Encryption/Decryption
            enc_time, ciphertext = measure_time(rsa.encrypt)(data)
            rate = calculate_bytes_rate(enc_time, file_name)
            save_results('RSA', 'encryption', key_size, file_name, enc_time, rate)
            
            dec_time, _ = measure_time(rsa.decrypt)(ciphertext)
            rate = calculate_bytes_rate(dec_time, file_name)
            save_results('RSA', 'decryption', key_size, file_name, dec_time, rate)
            
            # Signing/Verification
            sign_time, signature = measure_time(rsa.sign)(data)
            rate = calculate_bytes_rate(sign_time, file_name)
            save_results('RSA', 'signing', key_size, file_name, sign_time, rate)
            
            verify_time, _ = measure_time(rsa.verify)(data, signature)
            rate = calculate_bytes_rate(verify_time, file_name)
            save_results('RSA', 'verification', key_size, file_name, verify_time, rate)

        # DSA Tests
        for key_size in key_sizes['DSA']:
            dsa = DSAEncryption(key_size)
            
            sign_time, signature = measure_time(dsa.sign)(data)
            rate = calculate_bytes_rate(sign_time, file_name)
            save_results('DSA', 'signing', key_size, file_name, sign_time, rate)
            
            verify_time, _ = measure_time(dsa.verify)(data, signature)
            rate = calculate_bytes_rate(verify_time, file_name)
            save_results('DSA', 'verification', key_size, file_name, verify_time, rate)

        # DH Tests
        for key_size in key_sizes['DH']:
            dhe = DiffieHellmanEncryption(key_size)
            
            dhe.run(key_size)
            exchange_time = dhe.execution_time
            rate = calculate_bytes_rate(exchange_time, file_name)
            save_results('DH', 'key_exchange', key_size, file_name, exchange_time, rate)

        # ECC Tests
        for curve in key_sizes['ECC']:
            ecc = ECCEncryption(curve)
            
            # Signing/Verification
            sign_time, signature = measure_time(ecc.sign)(data)
            rate = calculate_bytes_rate(sign_time, file_name)
            save_results('ECC', 'signing', curve, file_name, sign_time, rate)
            
            verify_time, _ = measure_time(ecc.verify)(data, signature)
            rate = calculate_bytes_rate(verify_time, file_name)
            save_results('ECC', 'verification', curve, file_name, verify_time, rate)

        print(f"Completed analysis for {file_name}")