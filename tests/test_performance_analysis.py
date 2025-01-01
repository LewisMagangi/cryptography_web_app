import unittest
import os
import psutil
from src.symmetric import AESEncryption, DESEncryption, DES3Encryption, RC2Encryption, RC4Encryption, BlowfishEncryption
from src.asymmetric import RSAEncryption, DSAEncryption, DHEncryption, ECCEncryption
from src.hashing import SHA1Hash, SHA2Hash, MD5Hash, HMACHash
from src.performance_analyzer import PerformanceAnalyzer, PerformanceMetrics

class TestPerformanceAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_dir = "./data/sample_text"
        cls.results_path = "./data/results/performance_data.csv"
        cls.analyzer = PerformanceAnalyzer(data_dir=cls.data_dir, results_path=cls.results_path)
        
        # Prepare dummy data for testing
        cls.test_data = b"Sample data for encryption and hashing performance tests."

    def test_symmetric_encryption(self):
        key_size = 256
        algo = AESEncryption
        averages = self.analyzer.analyze_algorithm("AESEncryption", algo, self.test_data, key_size)
        self.assertIsInstance(averages, dict)
        self.assertIn("avg_time", averages)
        self.assertIn("avg_cpu", averages)
        self.assertIn("avg_ram", averages)

    def test_asymmetric_encryption(self):
        key_size = 2048
        algo = RSAEncryption
        averages = self.analyzer.analyze_algorithm("RSAEncryption", algo, self.test_data, key_size)
        self.assertIsInstance(averages, dict)
        self.assertIn("avg_time", averages)
        self.assertIn("avg_cpu", averages)
        self.assertIn("avg_ram", averages)

    def test_hashing_algorithm(self):
        algo = SHA1Hash
        averages = self.analyzer.analyze_algorithm("SHA1Hash", algo, self.test_data, None)
        self.assertIsInstance(averages, dict)
        self.assertIn("avg_time", averages)
        self.assertIn("avg_cpu", averages)
        self.assertIn("avg_ram", averages)

if __name__ == "__main__":
    unittest.main()
