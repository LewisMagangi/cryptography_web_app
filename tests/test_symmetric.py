import unittest
from analysis.src.symmetric import AESEncryption, DESEncryption, DES3Encryption, RC2Encryption, RC4Encryption, BlowfishEncryption

class TestSymmetricEncryption(unittest.TestCase):
    """
    Test cases for symmetric encryption and decryption classes.
    """

    def setUp(self):
        """
        Set up a common plaintext message for all tests.
        """
        self.plaintext = "This is a test message."
        self.plaintext_bytes = self.plaintext.encode('utf-8')

    def test_aes_encryption(self):
        """
        Test AES encryption and decryption.
        """
        aes = AESEncryption()
        ciphertext, tag, nonce = aes.encrypt(self.plaintext)
        decrypted_text = aes.decrypt(ciphertext, tag, nonce)
        self.assertEqual(self.plaintext, decrypted_text)

    def test_des_encryption(self):
        """
        Test DES encryption and decryption.
        """
        des = DESEncryption()
        ciphertext, iv = des.encrypt(self.plaintext)
        decrypted_text = des.decrypt(ciphertext, iv)
        self.assertEqual(self.plaintext, decrypted_text)

    def test_des3_encryption(self):
        """
        Test 3DES encryption and decryption.
        """
        des3 = DES3Encryption()
        ciphertext, iv = des3.encrypt(self.plaintext)
        decrypted_text = des3.decrypt(ciphertext, iv)
        self.assertEqual(self.plaintext, decrypted_text)

    def test_rc2_encryption(self):
        """
        Test RC2 encryption and decryption.
        """
        rc2 = RC2Encryption()
        ciphertext, iv = rc2.encrypt(self.plaintext)
        decrypted_text = rc2.decrypt(ciphertext, iv)
        self.assertEqual(self.plaintext, decrypted_text)

    def test_rc4_encryption(self):
        """
        Test RC4 encryption and decryption.
        """
        rc4 = RC4Encryption()
        ciphertext = rc4.encrypt(self.plaintext)
        decrypted_text = rc4.decrypt(ciphertext)
        self.assertEqual(self.plaintext, decrypted_text)

    def test_blowfish_encryption(self):
        """
        Test Blowfish encryption and decryption.
        """
        blowfish = BlowfishEncryption()
        ciphertext, iv = blowfish.encrypt(self.plaintext)
        decrypted_text = blowfish.decrypt(ciphertext, iv)
        self.assertEqual(self.plaintext, decrypted_text)

if __name__ == '__main__':
    unittest.main()