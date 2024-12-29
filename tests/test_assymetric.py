import unittest
from src.assymetric import RSAEncryption, DSAEncryption, DHEncryption, ECCEncryption

class TestAsymmetricEncryption(unittest.TestCase):
    """
    Test cases for asymmetric encryption and decryption classes.
    """

    def setUp(self):
        """
        Set up a common plaintext message for all tests.
        """
        self.plaintext = "This is a test message."

    def test_rsa_encryption(self):
        """
        Test RSA encryption and decryption.
        """
        rsa = RSAEncryption()
        ciphertext = rsa.encrypt(self.plaintext)
        decrypted_text = rsa.decrypt(ciphertext)
        self.assertEqual(self.plaintext, decrypted_text)

    def test_dsa_signing(self):
        """
        Test DSA signing and verification.
        """
        dsa = DSAEncryption()
        signature = dsa.sign(self.plaintext)
        is_valid = dsa.verify(self.plaintext, signature)
        self.assertTrue(is_valid)

    def test_dh_key_exchange(self):
        """
        Test Diffie-Hellman key exchange.
        """
        dh1 = DHEncryption()
        dh2 = DHEncryption()
        shared_key1 = dh1.generate_shared_key(dh2.public_key)
        shared_key2 = dh2.generate_shared_key(dh1.public_key)
        self.assertEqual(shared_key1, shared_key2)

    def test_ecc_signing(self):
        """
        Test ECC signing and verification.
        """
        ecc = ECCEncryption()
        signature = ecc.sign(self.plaintext)
        is_valid = ecc.verify(self.plaintext, signature)
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()