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
from Crypto.Random import get_random_bytes
import base64
import time
import os
import csv

# Define constants
DATA_DIR = os.path.join(os.path.dirname(__file__),  '..', 'data', 'sample_text')
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
        self.key = get_random_bytes(key_size)
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
        self.iv = get_random_bytes(DES.block_size)
        self.name = "DESEncryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext and IV.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        cipher = DES.new(self.key, DES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))
        return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(self.iv).decode('utf-8')

    def decrypt(self, ciphertext, iv):
        """
        Decrypt the ciphertext using DES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :param iv: The base64 encoded IV.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        if isinstance(iv, str):
            iv = base64.b64decode(iv)
        cipher = DES.new(self.key, DES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
        return plaintext.decode('utf-8')

class DES3Encryption:
    """
    Class to perform 3DES encryption and decryption.
    """
    def __init__(self, key_size=16):
        """
        Initialize the 3DES cipher with a random key.
        
        :param key_size: Size of the key in bytes (default is 16 bytes for 3DES).
        """
        self.key = get_random_bytes(key_size)
        self.iv = get_random_bytes(DES3.block_size)
        self.name = "DES3Encryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using 3DES.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext and IV.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(plaintext, DES3.block_size))
        return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(self.iv).decode('utf-8')

    def decrypt(self, ciphertext, iv):
        """
        Decrypt the ciphertext using 3DES.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :param iv: The base64 encoded IV.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        if isinstance(iv, str):
            iv = base64.b64decode(iv)
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)
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
        self.iv = get_random_bytes(ARC2.block_size)
        self.name = "RC2Encryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using RC2.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext and IV.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        cipher = ARC2.new(self.key, ARC2.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(plaintext, ARC2.block_size))
        return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(self.iv).decode('utf-8')

    def decrypt(self, ciphertext, iv):
        """
        Decrypt the ciphertext using RC2.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :param iv: The base64 encoded IV.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        if isinstance(iv, str):
            iv = base64.b64decode(iv)
        cipher = ARC2.new(self.key, ARC2.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), ARC2.block_size)
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
        self.iv = get_random_bytes(Blowfish.block_size)
        self.name = "BlowfishEncryption"
        self.execution_time = 0

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using Blowfish.
        
        :param plaintext: The plaintext to encrypt.
        :return: The base64 encoded ciphertext and IV.
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(plaintext, Blowfish.block_size))
        return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(self.iv).decode('utf-8')

    def decrypt(self, ciphertext, iv):
        """
        Decrypt the ciphertext using Blowfish.
        
        :param ciphertext: The base64 encoded ciphertext to decrypt.
        :param iv: The base64 encoded IV.
        :return: The decrypted plaintext.
        """
        if isinstance(ciphertext, str):
            ciphertext = base64.b64decode(ciphertext)
        if isinstance(iv, str):
            iv = base64.b64decode(iv)
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), Blowfish.block_size)
        return plaintext.decode('utf-8')

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

def calculate_mb_rate(time_taken, filename):
    """Calculate MB/s rate from time and filename."""
    try:
        size_mb = int(filename.split('_')[0].replace('mb', ''))
        return size_mb / time_taken if time_taken > 0 else 0
    except:
        return 0

def save_results(algorithm, operation, key_size, file_name, time_taken, rate):
    """
    Save the time taken and rate for an operation to a CSV file.
    
    :param algorithm: The name of the algorithm
    :param operation: The operation performed
    :param key_size: The size of the key
    :param file_name: The name of the file used
    :param time_taken: The time taken for the operation
    :param rate: Processing rate in MB/s
    """
    with open(ANALYSIS_RESULTS_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([algorithm, operation, key_size, file_name, time_taken, rate])

if __name__ == "__main__":
    # Initialize results file
    with open(ANALYSIS_RESULTS_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['algorithm', 'operation', 'key_size', 'file_name', 'time_taken', 'rate'])

    # Test data files
    sample_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    key_sizes = {
        'AES': [16, 24, 32],  # Correct key sizes for AES
        'DES': [8],
        '3DES': [16, 24],  # Correct key sizes for 3DES
        'RC2': [5, 8, 16],
        'RC4': [5, 8, 16],
        'Blowfish': [4, 8, 16, 24, 32]  # Correct key sizes for Blowfish
    }

    for file_name in sample_files:
        with open(os.path.join(DATA_DIR, file_name), 'r') as file:
            data = file.read()

        # AES Tests
        for key_size in key_sizes['AES']:
            aes = AESEncryption(key_size)
            
            try:
                # Encryption
                enc_time, (ciphertext, tag, nonce) = measure_time(aes.encrypt)(data)
                rate = calculate_mb_rate(enc_time, file_name)
                save_results('AES', 'encryption', key_size, file_name, enc_time, rate)
                
                # Decryption
                dec_time, _ = measure_time(aes.decrypt)(ciphertext, tag, nonce)
                rate = calculate_mb_rate(dec_time, file_name)
                save_results('AES', 'decryption', key_size, file_name, dec_time, rate)
            except Exception as e:
                print(f"Error during AES operation with key size {key_size} and file {file_name}: {e}")

        # DES Tests
        des = DESEncryption()
        
        try:
            # Encryption
            enc_time, (ciphertext, iv) = measure_time(des.encrypt)(data)
            rate = calculate_mb_rate(enc_time, file_name)
            save_results('DES', 'encryption', 8, file_name, enc_time, rate)
            
            # Decryption
            dec_time, _ = measure_time(des.decrypt)(ciphertext, iv)
            rate = calculate_mb_rate(dec_time, file_name)
            save_results('DES', 'decryption', 8, file_name, dec_time, rate)
        except Exception as e:
            print(f"Error during DES operation with file {file_name}: {e}")

        # 3DES Tests
        for key_size in key_sizes['3DES']:
            triple_des = DES3Encryption(key_size)
            
            try:
                # Encryption
                enc_time, (ciphertext, iv) = measure_time(triple_des.encrypt)(data)
                rate = calculate_mb_rate(enc_time, file_name)
                save_results('3DES', 'encryption', key_size, file_name, enc_time, rate)
                
                # Decryption
                dec_time, _ = measure_time(triple_des.decrypt)(ciphertext, iv)
                rate = calculate_mb_rate(dec_time, file_name)
                save_results('3DES', 'decryption', key_size, file_name, dec_time, rate)
            except Exception as e:
                print(f"Error during 3DES operation with key size {key_size} and file {file_name}: {e}")

        # RC2 Tests
        for key_size in key_sizes['RC2']:
            rc2 = RC2Encryption(key_size)
            
            try:
                # Encryption
                enc_time, (ciphertext, iv) = measure_time(rc2.encrypt)(data)
                rate = calculate_mb_rate(enc_time, file_name)
                save_results('RC2', 'encryption', key_size, file_name, enc_time, rate)
                
                # Decryption
                dec_time, _ = measure_time(rc2.decrypt)(ciphertext, iv)
                rate = calculate_mb_rate(dec_time, file_name)
                save_results('RC2', 'decryption', key_size, file_name, dec_time, rate)
            except Exception as e:
                print(f"Error during RC2 operation with key size {key_size} and file {file_name}: {e}")

        # RC4 Tests
        for key_size in key_sizes['RC4']:
            rc4 = RC4Encryption(key_size)
            
            try:
                # Encryption
                enc_time, ciphertext = measure_time(rc4.encrypt)(data)
                rate = calculate_mb_rate(enc_time, file_name)
                save_results('RC4', 'encryption', key_size, file_name, enc_time, rate)
                
                # Decryption
                dec_time, _ = measure_time(rc4.decrypt)(ciphertext)
                rate = calculate_mb_rate(dec_time, file_name)
                save_results('RC4', 'decryption', key_size, file_name, dec_time, rate)
            except Exception as e:
                print(f"Error during RC4 operation with key size {key_size} and file {file_name}: {e}")

        # Blowfish Tests
        for key_size in key_sizes['Blowfish']:
            blowfish = BlowfishEncryption(key_size)
            
            try:
                # Encryption
                enc_time, (ciphertext, iv) = measure_time(blowfish.encrypt)(data)
                rate = calculate_mb_rate(enc_time, file_name)
                save_results('Blowfish', 'encryption', key_size, file_name, enc_time, rate)
                
                # Decryption
                dec_time, _ = measure_time(blowfish.decrypt)(ciphertext, iv)
                rate = calculate_mb_rate(dec_time, file_name)
                save_results('Blowfish', 'decryption', key_size, file_name, dec_time, rate)
            except Exception as e:
                print(f"Error during Blowfish operation with key size {key_size} and file {file_name}: {e}")

        print(f"Completed analysis for {file_name}")
