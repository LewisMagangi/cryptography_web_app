import unittest
import os
import time
import csv
from src.hashing import SHA1Hash, SHA2Hash, MD5Hash, HMACHash

class TestHashingAlgorithms(unittest.TestCase):
    """
    Test cases for hashing algorithms.
    """

    def setUp(self):
        """
        Set up the data for all tests.
        """
        self.data_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text')
        self.data_files = [os.path.join(self.data_folder, f) for f in os.listdir(self.data_folder) if f.endswith('.txt')]
        self.results_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'analysis_performance_data.csv')

        # Ensure the results file is empty before starting
        with open(self.results_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['algo_name', 'data_size', 'file_name', 'time_taken'])

    def load_data(self, file_path):
        """
        Load data from the specified file.
        
        :param file_path: Path to the data file.
        :return: The data read from the file.
        """
        with open(file_path, 'r') as file:
            return file.read()

    def measure_hash_time(self, hash_function, data):
        """
        Measure the time taken to hash the data using the specified hash function.
        
        :param hash_function: The hash function to use.
        :param data: The data to hash.
        :return: The time taken to hash the data.
        """
        start_time = time.time()
        hash_function.hash(data)
        end_time = time.time()
        return end_time - start_time

    def save_time_result(self, algo_name, data_size, file_name, time_taken):
        """
        Save the time taken for hashing to the CSV file.
        
        :param algo_name: The name of the hashing algorithm.
        :param data_size: The size of the data.
        :param file_name: The name of the file.
        :param time_taken: The time taken to hash the data.
        """
        with open(self.results_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([algo_name, data_size, file_name, time_taken])

    def test_sha1_hash(self):
        """
        Test SHA-1 hashing and measure the time taken.
        """
        sha1 = SHA1Hash()
        for file_path in self.data_files:
            data = self.load_data(file_path)
            time_taken = self.measure_hash_time(sha1, data)
            file_name = os.path.basename(file_path)
            data_size = os.path.getsize(file_path)
            self.save_time_result('SHA-1', data_size, file_name, time_taken)
            print(f"SHA-1: {file_name} - Time taken: {time_taken:.6f} seconds")
            self.assertIsNotNone(sha1.hash(data))

    def test_sha2_hash(self):
        """
        Test SHA-2 hashing with different algorithms and measure the time taken.
        """
        sha2_algorithms = {
            'SHA-224': SHA2Hash('SHA-224'),
            'SHA-256': SHA2Hash('SHA-256'),
            'SHA-384': SHA2Hash('SHA-384'),
            'SHA-512': SHA2Hash('SHA-512')
        }
        for algo_name, sha2 in sha2_algorithms.items():
            for file_path in self.data_files:
                data = self.load_data(file_path)
                time_taken = self.measure_hash_time(sha2, data)
                file_name = os.path.basename(file_path)
                data_size = os.path.getsize(file_path)
                self.save_time_result(algo_name, data_size, file_name, time_taken)
                print(f"{algo_name}: {file_name} - Time taken: {time_taken:.6f} seconds")
                self.assertIsNotNone(sha2.hash(data))

    def test_md5_hash(self):
        """
        Test MD5 hashing and measure the time taken.
        """
        md5 = MD5Hash()
        for file_path in self.data_files:
            data = self.load_data(file_path)
            time_taken = self.measure_hash_time(md5, data)
            file_name = os.path.basename(file_path)
            data_size = os.path.getsize(file_path)
            self.save_time_result('MD5', data_size, file_name, time_taken)
            print(f"MD5: {file_name} - Time taken: {time_taken:.6f} seconds")
            self.assertIsNotNone(md5.hash(data))

    def test_hmac_hash(self):
        """
        Test HMAC hashing and measure the time taken.
        """
        hmac = HMACHash()
        for file_path in self.data_files:
            data = self.load_data(file_path)
            time_taken = self.measure_hash_time(hmac, data)
            file_name = os.path.basename(file_path)
            data_size = os.path.getsize(file_path)
            self.save_time_result('HMAC', data_size, file_name, time_taken)
            print(f"HMAC: {file_name} - Time taken: {time_taken:.6f} seconds")
            self.assertIsNotNone(hmac.hash(data))

if __name__ == '__main__':
    unittest.main()