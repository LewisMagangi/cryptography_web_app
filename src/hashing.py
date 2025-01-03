"""
Implementation of hashing algorithms:
Hashing Algorithms
SHA-1 (Secure Hash Algorithm 1)
SHA-2 (Secure Hash Algorithm 2) family: including SHA-224, SHA-256, SHA-384, SHA-512
MD5 (Message Digest Algorithm 5)
HMAC (Hash-based Message Authentication Code)
"""
import os
import time
import csv
from Crypto.Hash import SHA1, SHA224, SHA256, SHA384, SHA512, MD5, HMAC
from Crypto.Random import get_random_bytes

# Define constants
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text')
ANALYSIS_RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'analysis_performance_data.csv')

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

def save_time_result(algorithm_name, file_name, total_time):
    with open(ANALYSIS_RESULTS_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([algorithm_name, file_name, total_time])
    print(f"Time taken for {algorithm_name} with file {file_name}: {total_time:.6f} seconds")

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
    # Ensure the results file is empty before starting
    with open(ANALYSIS_RESULTS_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['algo_name', 'file_name', 'time_taken'])

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

        measure_hash_time(sha1, data, 'SHA-1', file_name)
        measure_hash_time(sha2_224, data, 'SHA-224', file_name)
        measure_hash_time(sha2_256, data, 'SHA-256', file_name)
        measure_hash_time(sha2_384, data, 'SHA-384', file_name)
        measure_hash_time(sha2_512, data, 'SHA-512', file_name)
        measure_hash_time(md5, data, 'MD5', file_name)
        measure_hash_time(hmac, data, 'HMAC', file_name)