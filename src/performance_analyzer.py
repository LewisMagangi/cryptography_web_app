import os
import csv
import sys
import psutil
import time
import pandas as pd

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import specific algorithms directly
from src.symmetric import AESEncryption, DESEncryption, DES3Encryption, RC2Encryption, RC4Encryption, BlowfishEncryption
from src.asymmetric import RSAEncryption, DSAEncryption, DHEncryption, ECCEncryption
from src.hashing import SHA1Hash, SHA2Hash, MD5Hash, HMACHash

# Define constants
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text')
SMALLER_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'smaller_sample_text')
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'results', 'performance_data.csv')
DEFAULT_ITERATIONS = 2
DEFAULT_KEYSIZE = None 

class PerformanceMetrics:
    """Class to calculate and store performance metrics."""

    def __init__(self, iterations=DEFAULT_ITERATIONS):
        """
        Initialize the PerformanceMetrics object.

        Args:
            iterations (int): Number of iterations to measure performance over.
        """
        self.iterations = iterations
        self.total_time = 0
        self.total_cpu = 0
        self.total_ram = 0

    def record_iteration(self, start_time, start_cpu, start_ram):
        """
        Record performance metrics for a single iteration.

        Args:
            start_time (float): Start time of the iteration.
            start_cpu (float): CPU usage percentage at the start.
            start_ram (float): RAM usage percentage at the start.
        """
        end_time = time.time()
        end_cpu = psutil.cpu_percent(interval=None)
        end_ram = psutil.virtual_memory().percent

        self.total_time += (end_time - start_time)
        self.total_cpu += (end_cpu - start_cpu)
        self.total_ram += (end_ram - start_ram)

    def get_averages(self):
        """
        Calculate average metrics over all iterations.

        Returns:
            dict: A dictionary containing average time, CPU usage, and RAM usage.
        """
        return {
            "avg_time": self.total_time / self.iterations,
            "avg_cpu": self.total_cpu / self.iterations,
            "avg_ram": self.total_ram / self.iterations,
        }


class PerformanceAnalyzer:
    """Class to manage the performance analysis process."""

    def __init__(self, data_dir=DATA_DIR, results_path=RESULTS_PATH):
        """
        Initialize the PerformanceAnalyzer object.

        Args:
            data_dir (str): Path to the directory containing data files.
            results_path (str): Path to the CSV file for saving results.
        """
        self.data_dir = data_dir  # Default to the regular data directory
        self.results_path = results_path
        self.encryption_algorithms = {
            "AESEncryption", "DESEncryption", "DES3Encryption", 
            "RC2Encryption", "RC4Encryption", "BlowfishEncryption", 
            "RSAEncryption", 
        }
        self.signing_algorithms = {
            "DSAEncryption", "ECCEncryption"
        }
        self.key_exchange_algorithms = {
            "DHEncryption"
        }
        self.algorithms = {
            "AESEncryption": AESEncryption,
            "DESEncryption": DESEncryption,
            "DES3Encryption": DES3Encryption,
            "RC2Encryption": RC2Encryption,
            "RC4Encryption": RC4Encryption,
            "BlowfishEncryption": BlowfishEncryption,
            "RSAEncryption": RSAEncryption,
            "DSAEncryption": DSAEncryption,
            "DHEncryption": DHEncryption,
            "ECCEncryption": ECCEncryption,
            "SHA1Hash": SHA1Hash,
            "SHA2Hash": SHA2Hash,
            "MD5Hash": MD5Hash,
            "HMACHash": HMACHash,
        }

    def get_data_files(self, algo_name):
        """
        Fetch all text files from the data directory.

        Returns:
            list: A list of file paths for data files in the data directory.
        """
         # Use SMALLER_DATA_DIR for asymmetric algorithms, otherwise use the regular DATA_DIR
        if algo_name in ["RSAEncryption", "DSAEncryption", "DHEncryption", "ECCEncryption"]:
            data_dir = SMALLER_DATA_DIR
        else:
            data_dir = self.data_dir

        return [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".txt")]

    
    def analyze_algorithm(self, algo_name, algo_class, data, key_size=None):
        """
        Analyze the performance of a specific algorithm with given data.

        Args:
            algo_name (str): Name of the algorithm.
            algo_class (class): The class representing the algorithm.
            data (bytes): The input data to process.
            key_size (int): The key size for encryption algorithms.

        Returns:
            dict: A dictionary containing average performance metrics.
        """
        metrics = PerformanceMetrics()
        for _ in range(metrics.iterations):
            start_time = time.time()
            start_cpu = psutil.cpu_percent(interval=None)
            start_ram = psutil.virtual_memory().percent

            # Execute algorithm functions
            no_key_size_algorithms = ["DESEncryption"]
            if algo_class.__name__ in no_key_size_algorithms:
                algo_instance = algo_class()
            else:
                algo_instance = algo_class(key_size) if key_size else algo_class()

            if algo_name in self.encryption_algorithms:
                encrypted_data = algo_instance.encrypt(data)  # For encryption algorithms
            elif algo_name in self.signing_algorithms:
                signed_data = algo_instance.sign(data.decode())
            elif algo_name in self.key_exchange_algorithms:
                # Generate the other party's Diffie-Hellman key pair
                other_party_private_key = algo_instance.parameters.generate_private_key()
                other_party_public_key = other_party_private_key.public_key()

                # Pass the other party's public key (which is a DHPublicKey object) to generate the shared key
                shared_key = algo_instance.generate_shared_key(other_party_public_key)
                # Ensure shared_key is not returned here, as it's not needed for performance metrics

            metrics.record_iteration(start_time, start_cpu, start_ram)

        # Return the averages as a dictionary
        return metrics.get_averages()


    def analyze_performance(self, iterations=DEFAULT_ITERATIONS, key_size=DEFAULT_KEYSIZE):
        """
        Perform the full performance analysis.

        Args:
            iterations (int): Number of iterations to measure performance.
            key_size (int): Key size for encryption algorithms.
        """
        results = []

        for algo_name, algo_class in self.algorithms.items():
            data_files = self.get_data_files(algo_name)
            for data_path in data_files:
                with open(data_path, "rb") as file:
                    data = file.read()

                averages = self.analyze_algorithm(algo_name, algo_class, data, key_size)
                # Make sure to include the required performance data along with the averages
                results.append({
                    "algorithm": algo_name,
                    "data_size": os.path.basename(data_path),
                    "iterations": iterations,
                    "key_size": key_size,
                    **averages,
                })

            self.save_results(results)

    def save_results(self, results):
        """
        Save the performance results to a CSV file, updating existing entries if necessary.

        Args:
            results (list): A list of result dictionaries containing algorithm, data_size, key_size, iterations, cpu_usage, and time_usage.
        """
        output_path = "./data/results/performance_data.csv"
        updated_data = []

        # Load existing data
        if os.path.isfile(output_path):
            with open(output_path, mode="r", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                updated_data = list(reader)

        # Convert existing data into a dictionary for easy lookup
        existing_data = {
            (row["algorithm"], row["data_size"], row["key_size"], row["iterations"]): row
            for row in updated_data
        }

        # Process new results
        for result in results:
            # Extract file size without path and extension (e.g., 1MB instead of 1MB.txt)
            data_size = os.path.splitext(os.path.basename(result["data_size"]))[0]  # Remove extension

            unique_key = (
                result["algorithm"],
                data_size,
                str(result["key_size"]),
                str(result["iterations"]),
            )

            if unique_key in existing_data:
                # Update existing entry with the new average metrics
                existing_data[unique_key].update({
                    "avg_cpu": result["avg_cpu"],
                    "avg_time": result["avg_time"],
                    "avg_ram": result["avg_ram"],
                })
            else:
                # Add new entry
                existing_data[unique_key] = {
                    "algorithm": result["algorithm"],
                    "data_size": data_size,
                    "iterations": result["iterations"],
                    "key_size": result["key_size"],
                    "avg_cpu": result["avg_cpu"],
                    "avg_time": result["avg_time"],
                    "avg_ram": result["avg_ram"],
                }

        # Write back to the CSV file
        with open(RESULTS_PATH, mode="w", newline="") as csv_file:
            fieldnames = ["algorithm", "data_size", "iterations", "key_size", "avg_cpu", "avg_time", "avg_ram"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_data.values())

# Main execution
if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()
    analyzer.analyze_performance()
