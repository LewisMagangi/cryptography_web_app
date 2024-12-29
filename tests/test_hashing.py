import unittest
from src.hashing import SHA1Hash, SHA2Hash, MD5Hash, HMACHash

class TestHashingAlgorithms(unittest.TestCase):
    """
    Test cases for hashing algorithms.
    """

    def setUp(self):
        """
        Set up a common message for all tests.
        """
        self.message = "This is a test message."

    def test_sha1_hash(self):
        """
        Test SHA-1 hashing.
        """
        sha1 = SHA1Hash()
        digest = sha1.hash(self.message)
        self.assertIsNotNone(digest)

    def test_sha2_hash(self):
        """
        Test SHA-2 hashing with different algorithms.
        """
        for algorithm in ['SHA-224', 'SHA-256', 'SHA-384', 'SHA-512']:
            sha2 = SHA2Hash(algorithm)
            digest = sha2.hash(self.message)
            self.assertIsNotNone(digest)

    def test_md5_hash(self):
        """
        Test MD5 hashing.
        """
        md5 = MD5Hash()
        digest = md5.hash(self.message)
        self.assertIsNotNone(digest)

    def test_hmac_hash(self):
        """
        Test HMAC hashing with different algorithms.
        """
        for algorithm in ['SHA-1', 'SHA-224', 'SHA-256', 'SHA-384', 'SHA-512', 'MD5']:
            hmac = HMACHash(algorithm=algorithm)
            digest = hmac.hash(self.message)
            self.assertIsNotNone(digest)

if __name__ == '__main__': 
    unittest.main()