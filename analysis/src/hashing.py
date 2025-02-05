"""
Implementation of hashing algorithms:
Hashing Algorithms
SHA-1 (Secure Hash Algorithm 1)
SHA-2 (Secure Hash Algorithm 2) family: including SHA-224, SHA-256, SHA-384, SHA-512
SHA-3 (Secure Hash Algorithm 3) family: including SHA3-224, SHA3-256, SHA3-384, SHA3-512
SHAKE (Secure Hash Algorithm Keccak) family: including SHAKE128, SHAKE256
MD5 (Message Digest Algorithm 5)
HMAC (Hash-based Message Authentication Code)
"""
import os
import time
import csv
import hashlib
from Crypto.Hash import SHA1, SHA224, SHA256, SHA384, SHA512, MD5, HMAC
from Crypto.Random import get_random_bytes

# Define constants
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text')
ANALYSIS_RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'hashing_analysis_results.csv')

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
        if isinstance(message, str):
            message = message.encode('utf-8')  # Convert to bytes if str
        h.update(message)
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
        if isinstance(message, str):
            message = message.encode('utf-8')  # Convert to bytes if str
        h.update(message)
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
        if isinstance(message, str):
            message = message.encode('utf-8')  # Convert to bytes if str
        h.update(message)
        return h.hexdigest()

class HMACHash:
    """
    Class to perform HMAC hashing.
    """
    def __init__(self, key=None):
        """
        Initialize the HMAC hash with the specified key.
        
        :param key: The key to use for HMAC (default is a random key).
        """
        self.key = key or get_random_bytes(16)

    def hash(self, message):
        """
        Hash the message using HMAC.
        
        :param message: The message to hash.
        :return: The hash digest.
        """
        h = HMAC.new(self.key, digestmod=SHA256)
        if isinstance(message, str):
            message = message.encode('utf-8')  # Convert to bytes if str
        h.update(message)
        return h.hexdigest()

class SHA3Hash:
    """
    Class to perform SHA-3 hashing.
    """
    def __init__(self, algorithm='SHA3-256'):
        """
        Initialize the SHA-3 hash with the specified algorithm.
        
        :param algorithm: The SHA-3 algorithm to use (default is 'SHA3-256').
        """
        self.algorithm = algorithm

    def hash(self, message):
        """
        Hash the message using SHA-3.
        
        :param message: The message to hash.
        :return: The hash digest.
        """
        if self.algorithm == 'SHA3-224':
            h = hashlib.sha3_224()
        elif self.algorithm == 'SHA3-256':
            h = hashlib.sha3_256()
        elif self.algorithm == 'SHA3-384':
            h = hashlib.sha3_384()
        elif self.algorithm == 'SHA3-512':
            h = hashlib.sha3_512()
        if isinstance(message, str):
            message = message.encode('utf-8')  # Convert to bytes if str
        h.update(message)
        return h.hexdigest()

class SHAKEHash:
    """
    Class to perform SHAKE hashing.
    """
    def __init__(self, algorithm='SHAKE128', output_length=32):
        """
        Initialize the SHAKE hash with the specified algorithm and output length.
        
        :param algorithm: The SHAKE algorithm to use (default is 'SHAKE128').
        :param output_length: The length of the output hash.
        """
        self.algorithm = algorithm
        self.output_length = output_length

    def hash(self, message):
        """
        Hash the message using SHAKE.
        
        :param message: The message to hash.
        :return: The hash digest.
        """
        if self.algorithm == 'SHAKE128':
            h = hashlib.shake_128()
        elif self.algorithm == 'SHAKE256':
            h = hashlib.shake_256()
        if isinstance(message, str):
            message = message.encode('utf-8')  # Convert to bytes if str
        h.update(message)
        return h.hexdigest(self.output_length)

def calculate_mb_rate(time_taken, data_size_bytes):
    """Calculate MB/s rate from time and data size."""
    size_mb = data_size_bytes / (1024 * 1024)  # Convert bytes to MB
    return size_mb / time_taken if time_taken > 0 else 0

def save_time_result(algorithm_name, file_name, total_time):
    """Save results including calculated rate to CSV."""
    # Extract file size from filename (e.g., '10mb_text_data_faker.txt' -> 10)
    file_size_mb = float(file_name.split('mb_')[0])
    file_size_bytes = file_size_mb * 1024 * 1024  # Convert MB to bytes
    
    # Calculate rate in MB/s
    rate = calculate_mb_rate(total_time, file_size_bytes)
    
    with open(ANALYSIS_RESULTS_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([algorithm_name, file_name, total_time, rate])

def measure_hash_time(hash_function, data, algorithm_name, file_name):
    start_time = time.time()
    hash_function.hash(data)
    end_time = time.time()
    total_time = end_time - start_time
    save_time_result(algorithm_name, file_name, total_time)

def load_data(file_name):
    data_path = os.path.join(DATA_DIR, file_name)
    with open(data_path, 'r') as file:
        return file.read()

# Example usage
if __name__ == "__main__":
    # Initialize results file with updated header
    with open(ANALYSIS_RESULTS_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['algorithm', 'file_name', 'time_taken', 'rate'])  # lowercase headers

    # List of sample data files
    sample_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]

    for file_name in sample_files:
        data = load_data(file_name)
        sha1 = SHA1Hash()
        sha2_224 = SHA2Hash('SHA-224')
        sha2_256 = SHA2Hash('SHA-256')
        sha2_384 = SHA2Hash('SHA-384')
        sha2_512 = SHA2Hash('SHA-512')
        md5 = MD5Hash()
        hmac = HMACHash()
        sha3_224 = SHA3Hash('SHA3-224')
        sha3_256 = SHA3Hash('SHA3-256')
        sha3_384 = SHA3Hash('SHA3-384')
        sha3_512 = SHA3Hash('SHA3-512')
        shake128 = SHAKEHash('SHAKE128', 32)
        shake256 = SHAKEHash('SHAKE256', 64)

        measure_hash_time(sha1, data, 'SHA-1', file_name)
        measure_hash_time(sha2_224, data, 'SHA-224', file_name)
        measure_hash_time(sha2_256, data, 'SHA-256', file_name)
        measure_hash_time(sha2_384, data, 'SHA-384', file_name)
        measure_hash_time(sha2_512, data, 'SHA-512', file_name)
        measure_hash_time(md5, data, 'MD5', file_name)
        measure_hash_time(hmac, data, 'HMAC', file_name)
        measure_hash_time(sha3_224, data, 'SHA3-224', file_name)
        measure_hash_time(sha3_256, data, 'SHA3-256', file_name)
        measure_hash_time(sha3_384, data, 'SHA3-384', file_name)
        measure_hash_time(sha3_512, data, 'SHA3-512', file_name)
        measure_hash_time(shake128, data, 'SHAKE128', file_name)
        measure_hash_time(shake256, data, 'SHAKE256', file_name)