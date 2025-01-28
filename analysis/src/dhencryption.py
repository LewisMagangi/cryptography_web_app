import time
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

class DHEncryption:
    """
    Class to perform Diffie-Hellman key exchange.
    """

    def __init__(self, key_size=2048):
        """
        Initialize the Diffie-Hellman parameters and generate a key pair.

        :param key_size: Size of the key in bits (default is 2048 bits).
        """
        print("Initializing DHEncryption...")
        print(f"Key size provided: {key_size}")

        # Attempt to generate parameters
        try:
            print("Attempting to generate parameters...")
            self.parameters = dh.generate_parameters(generator=2, key_size=key_size, backend=default_backend())
            print("Parameters generated successfully.")
        except Exception as e:
            print(f"Error generating parameters: {e}")
            raise

        # Generate private and public keys
        try:
            print("Generating private key...")
            self.private_key = self.parameters.generate_private_key()
            print("Private key generated successfully.")
            print("Generating public key...")
            self.public_key = self.private_key.public_key()
            print("Public key generated successfully.")
        except Exception as e:
            print(f"Error generating keys: {e}")
            raise

        self.name = "DHEncryption"
        self.execution_time = 0

    def generate_shared_key(self, peer_public_key):
        """
        Generate a shared key using the peer's public key.

        :param peer_public_key: The peer's public key.
        :return: The shared key.
        """
        print("Generating shared key...")
        try:
            shared_key = self.private_key.exchange(peer_public_key)
            print("Shared key generated successfully.")
            return shared_key
        except Exception as e:
            print(f"Error generating shared key: {e}")
            raise

    def run(self, data, key_size):
        """
        Run the Diffie-Hellman key exchange process.

        :param data: Not used in this context.
        :param key_size: Size of the key in bits.
        """
        print(f"Running Diffie-Hellman exchange with key size: {key_size}")
        try:
            # Generate the other party's Diffie-Hellman key pair
            print("Generating other party's private key...")
            other_party_private_key = self.parameters.generate_private_key()
            print("Other party's private key generated.")
            other_party_public_key = other_party_private_key.public_key()
            print("Other party's public key generated.")

            # Generate shared keys
            start_time = time.time()
            self.generate_shared_key(other_party_public_key)
            self.execution_time = time.time() - start_time
            print(f"Shared key exchange completed in {self.execution_time:.4f} seconds.")
        except Exception as e:
            print(f"Error during Diffie-Hellman exchange: {e}")
            raise


if __name__ == "__main__":
    print("Starting DHEncryption test...")
    try:
        key_size = 2048
        print(f"Initializing DHEncryption with key size: {key_size}...")
        dh = DHEncryption(key_size)
        print("DHEncryption object initialized successfully.")

        print("Running DH key exchange...")
        dh.run(None, key_size)
        print(f"Execution time: {dh.execution_time:.4f} seconds.")
    except Exception as e:
        print(f"Error during execution: {e}")
